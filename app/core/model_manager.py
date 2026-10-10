import logging
import urllib.request
from collections.abc import Callable
from dataclasses import dataclass

import numpy as np
from PIL import Image

from ..i18n import tr
from ..utils.paths import MODELS_DIR

log = logging.getLogger(__name__)
Progress = Callable[[float, str], None]
RELEASE = "https://github.com/nikweel/ai-anti-duplicate/releases/download/v0.1/"


@dataclass(frozen=True)
class ModelSpec:
    id: str
    file: str
    size_mb: int
    dim: int
    size_bytes: int      # точный размер файла: защита от обрезанных/недокачанных файлов
    thr_default: float   # порог схожести при положении ползунка по умолчанию (подобран по замерам)
    thr_span: float      # на сколько порог меняется от самого строгого до самого мягкого положения
    resize: int = 256    # короткая сторона до кропа
    crop: int = 224
    mean: tuple = (0.485, 0.456, 0.406)
    std: tuple = (0.229, 0.224, 0.225)


# Семейство DINOv2: в замерах лучше CLIP различает дубли и «похожие, но другие» кадры при меньшем размере
MODELS = {
    "light": ModelSpec("light", "dinov2_small.onnx", 44, 384, 44397267, 0.955, 0.06),
    "medium": ModelSpec("medium", "dinov2_base.onnx", 174, 768, 173549573, 0.960, 0.06),
    "heavy": ModelSpec("heavy", "dinov2_large.onnx", 609, 1024, 609124541, 0.925, 0.10),
}
DEFAULT_SENSITIVITY = 33  # положение ползунка по умолчанию (0 = строго, 100 = мягко)


def threshold_for(model_id: str, sensitivity: int) -> float:
    """Порог схожести для выбранной модели и положения ползунка (0 строго ... 100 мягко)."""
    spec = MODELS.get(model_id) or MODELS["light"]
    return spec.thr_default + (DEFAULT_SENSITIVITY - sensitivity) / 100 * spec.thr_span


def preprocess(im: Image.Image, spec: ModelSpec) -> np.ndarray:
    """Как в обработке DINOv2: уменьшение короткой стороны (bicubic), центральный кроп, нормализация."""
    im = im.convert("RGB")
    w, h = im.size
    nw, nh = (spec.resize, int(spec.resize * h / w)) if w <= h else (int(spec.resize * w / h), spec.resize)
    im = im.resize((nw, nh), Image.BICUBIC)
    l, t = (nw - spec.crop) // 2, (nh - spec.crop) // 2
    im = im.crop((l, t, l + spec.crop, t + spec.crop))
    a = (np.asarray(im, np.float32) / 255 - np.array(spec.mean, np.float32)) / np.array(spec.std, np.float32)
    return a.transpose(2, 0, 1)


LEGACY_IDS = {"fast": "light", "accurate": "medium"}  # старые названия в настройках


def is_downloaded(model_id: str) -> bool:
    p = MODELS_DIR / MODELS[model_id].file
    return p.exists() and p.stat().st_size == MODELS[model_id].size_bytes  # неполный файл считается не скачанным


_GPU = ("CUDAExecutionProvider", "DmlExecutionProvider", "CoreMLExecutionProvider")


def available_gpu() -> str | None:
    """Имя доступного GPU-провайдера ONNX Runtime или None."""
    import onnxruntime as ort

    have = ort.get_available_providers()
    return next((p for p in _GPU if p in have), None)


class OnnxEmbedder:
    def __init__(self, path, device: str = "auto", spec: ModelSpec | None = None):
        import onnxruntime as ort

        self.spec = spec or MODELS["light"]
        self.dim = self.spec.dim
        gpu = available_gpu() if device in ("auto", "gpu") else None
        self.device_name = "CPU"
        self.session = None
        if gpu:
            try:
                opts = ort.SessionOptions()
                if gpu == "DmlExecutionProvider":  # требования DirectML
                    opts.enable_mem_pattern = False
                    opts.execution_mode = ort.ExecutionMode.ORT_SEQUENTIAL
                self.session = ort.InferenceSession(str(path), opts, providers=[gpu, "CPUExecutionProvider"])
                self._probe()
                self.device_name = gpu.replace("ExecutionProvider", "")
            except Exception as e:  # любая проблема с GPU -> тихий откат на процессор
                log.warning("GPU (%s) недоступен, используем CPU: %s", gpu, e)
                self.session = None
        if self.session is None:
            self.session = ort.InferenceSession(str(path), providers=["CPUExecutionProvider"])
        log.info("Устройство: %s", self.device_name)

    def _probe(self):
        self.session.run(None, {"pixel_values": np.zeros((1, 3, self.spec.crop, self.spec.crop), np.float32)})

    def encode(self, images: list[Image.Image], batch_size: int = 16) -> np.ndarray:
        """L2-нормированные эмбеддинги [N, dim]."""
        out = []
        for i in range(0, len(images), batch_size):
            x = np.stack([preprocess(im, self.spec) for im in images[i:i + batch_size]])
            e = self.session.run(None, {"pixel_values": x})[0]
            out.append(e / np.linalg.norm(e, axis=1, keepdims=True))
        return np.concatenate(out).astype(np.float32) if out else np.zeros((0, self.dim), np.float32)


def _download(spec: ModelSpec, progress: Progress) -> None:
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    target = MODELS_DIR / spec.file
    tmp = target.with_suffix(".part")
    last = [-1]

    def hook(blocks, bs, total):
        if total <= 0:
            return
        done = min(blocks * bs, total)
        pct = int(done * 100 / total)
        if pct != last[0]:  # не чаще одного раза на процент
            last[0] = pct
            progress(pct / 100, tr("model_dl", p=pct, d=f"{done / 1e6:.0f}", t=f"{total / 1e6:.0f}"))

    urllib.request.urlretrieve(RELEASE + spec.file, tmp, hook)
    if tmp.stat().st_size != spec.size_bytes:
        tmp.unlink(missing_ok=True)
        raise OSError(f"{spec.file}: файл скачан не полностью")
    tmp.replace(target)


def load_model(model_id: str = "light", device: str = "auto", progress: Progress = lambda f, m: None) -> OnnxEmbedder:
    spec = MODELS[model_id]
    path = MODELS_DIR / spec.file
    if not is_downloaded(model_id):
        _download(spec, progress)
    progress(1.0, tr("model_mem"))
    return OnnxEmbedder(path, device, spec)
