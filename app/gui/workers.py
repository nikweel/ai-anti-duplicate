import logging
import threading
from pathlib import Path

from PySide6.QtCore import QThread, Signal

from ..i18n import tr
from ..core.clustering import cluster
from ..core.embedder import embed_images
from ..core.model_manager import load_model
from ..data.models import DuplicateGroup, ImageInfo
from ..data.scanner import scan_folder
from ..services.exporter import export_unique
from ..services.naming import NamingOptions
from ..services.selection import pick_newest

log = logging.getLogger(__name__)


class ModelWorker(QThread):
    progress = Signal(float, str)
    loaded = Signal(object)
    failed = Signal(str)

    def __init__(self, model_id: str = "light", device: str = "auto"):
        super().__init__()
        self.model_id, self.device = model_id, device

    def run(self):
        try:
            self.loaded.emit(load_model(self.model_id, self.device, lambda f, m: self.progress.emit(f, m)))
        except Exception as e:
            log.exception("Ошибка загрузки модели")
            self.failed.emit(tr("model_fail", e=e))


class Controllable(QThread):
    """Поток с паузой и отменой. Пауза действует между небольшими шагами работы."""

    def __init__(self):
        super().__init__()
        self._resume = threading.Event()
        self._resume.set()

    def pause(self) -> None:
        self._resume.clear()

    def resume(self) -> None:
        self._resume.set()

    @property
    def paused(self) -> bool:
        return not self._resume.is_set()

    def cancel(self) -> None:
        self.requestInterruption()
        self._resume.set()  # снять паузу, чтобы поток увидел отмену

    def checkpoint(self) -> None:
        while not self._resume.is_set() and not self.isInterruptionRequested():
            self._resume.wait(0.1)


class ScanWorker(Controllable):
    progress = Signal(float, str)
    done = Signal(list, list)  # all_images, groups
    failed = Signal(str)
    cancelled = Signal()

    def __init__(self, model, folder: Path, exclude: Path, threshold: float = 0.92, rotations: bool = True, recursive: bool = True):
        super().__init__()
        self.model, self.folder, self.exclude = model, folder, exclude
        self.threshold, self.rotations, self.recursive = threshold, rotations, recursive

    def run(self):
        try:
            self.progress.emit(0, tr("scanning"))
            infos = [i for i in scan_folder(self.folder, self.isInterruptionRequested, self.recursive) if not i.path.is_relative_to(self.exclude)]
            kept, emb = embed_images(
                self.model, infos, self.rotations,
                progress=lambda d, t: self.progress.emit(d / max(t, 1), tr("analysis", d=d, t=t)),
                should_stop=self.isInterruptionRequested,
                checkpoint=self.checkpoint,
            )
            if self.isInterruptionRequested():
                self.cancelled.emit()
                return
            self.progress.emit(1, tr("grouping"))
            groups = []
            for idx in cluster(emb, self.threshold):
                g = DuplicateGroup([kept[i] for i in idx])
                g.keep = [pick_newest(g)]
                groups.append(g)
            self.done.emit(kept, groups)
        except Exception as e:
            log.exception("Ошибка сканирования")
            self.failed.emit(str(e))


class ExportWorker(Controllable):
    """Копирование результата в отдельном потоке: с прогрессом, паузой и отменой."""

    progress = Signal(float, str)
    done = Signal(int)
    failed = Signal(str)
    cancelled = Signal()

    def __init__(self, dst: Path, groups, images, naming: NamingOptions):
        super().__init__()
        self.dst, self.groups, self.images, self.naming = dst, groups, images, naming

    def run(self):
        try:
            n = export_unique(
                self.dst, self.groups, self.images, self.naming,
                progress=lambda d, t: self.progress.emit(d / max(t, 1), tr("copying", d=d, t=t)),
                should_stop=self.isInterruptionRequested, checkpoint=self.checkpoint,
            )
            if self.isInterruptionRequested():
                self.cancelled.emit()
            else:
                self.done.emit(n)
        except Exception as e:
            log.exception("Ошибка копирования")
            self.failed.emit(str(e))
