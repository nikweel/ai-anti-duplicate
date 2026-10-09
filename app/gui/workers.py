import logging
from pathlib import Path

from PySide6.QtCore import QThread, Signal

from ..i18n import tr
from ..core.clustering import cluster
from ..core.embedder import embed_images
from ..core.model_manager import load_model
from ..data.models import DuplicateGroup, ImageInfo
from ..data.scanner import scan_folder
from ..services.selection import pick_newest

log = logging.getLogger(__name__)


class ModelWorker(QThread):
    progress = Signal(float, str)
    loaded = Signal(object)
    failed = Signal(str)

    def run(self):
        try:
            self.loaded.emit(load_model(lambda f, m: self.progress.emit(f, m)))
        except Exception as e:
            log.exception("Ошибка загрузки модели")
            self.failed.emit(tr("model_fail", e=e))


class ScanWorker(QThread):
    progress = Signal(float, str)
    done = Signal(list, list)  # all_images, groups
    failed = Signal(str)

    def __init__(self, model, folder: Path, exclude: Path, threshold: float = 0.92, rotations: bool = True):
        super().__init__()
        self.model, self.folder, self.exclude = model, folder, exclude
        self.threshold, self.rotations = threshold, rotations

    def run(self):
        try:
            self.progress.emit(0, tr("scanning"))
            infos = [i for i in scan_folder(self.folder, self.isInterruptionRequested) if not i.path.is_relative_to(self.exclude)]
            kept, emb = embed_images(
                self.model, infos, self.rotations,
                progress=lambda d, t: self.progress.emit(d / max(t, 1), tr("analysis", d=d, t=t)),
                should_stop=self.isInterruptionRequested,
            )
            self.progress.emit(1, tr("grouping"))
            groups = []
            for idx in cluster(emb, self.threshold):
                g = DuplicateGroup([kept[i] for i in idx])
                g.keep = pick_newest(g)
                groups.append(g)
            self.done.emit(kept, groups)
        except Exception as e:
            log.exception("Ошибка сканирования")
            self.failed.emit(str(e))
