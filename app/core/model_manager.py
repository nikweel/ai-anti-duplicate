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
    threshold_shift: float = 0.0  # поправка порога схожести (у модели свой масштаб сходства)


MODELS = {
    "fast": ModelSpec("fast", "clip_vision.onnx", 176, 512),  # CLIP ViT-B/32
    "accurate": ModelSpec("accurate", "clip_vit_l14.onnx", 608, 768, -0.02),  # CLIP ViT-L/14
}

_MEAN = np.array([0.48145466, 0.4578275, 0.40821073], np.float32)
_STD = np.array([0.26862954, 0.26130258, 0.27577711], np.float32)
_GPU = ("CUDAExecutionProvider", "DmlExecutionProvider", "CoreMLExecutionProvider")


def preprocess(im: Image.Image) -> np.ndarray:
    """Идентично CLIPImageProcessor: resize короткой стороны до 224 (bicubic), центр-кроп, нормализация."""
    im = im.convert("RGB")
    w, h = im.size
    nw, nh = (224, int(224 * h / w)) if w <= h else (int(224 * w / h), 224)
    im = im.resize((nw, nh), Image.BICUBIC)
    l, t = (nw - 224) // 2, (nh - 224) // 2
    im = im.crop((l, t, l + 224, t + 224))
    a = (np.asarray(im, np.float32) / 255 - _MEAN) / _STD
    return a.transpose(2, 0, 1)


def is_downloaded(model_id: str) -> bool:
    return (MODELS_DIR / MODELS[model_id].file).exists()


def available_gpu() -> str | None:
    """Имя доступного GPU-провайдера ONNX Runtime или None."""
    import onnxruntime as ort

    have = ort.get_available_providers()
    return next((p for p in _GPU if p in have), None)


class ClipOnnx:
    def __init__(self, path, device: str = "auto", dim: int = 512):
        import onnxruntime as ort

        self.dim = dim
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
        self.session.run(None, {"pixel_values": np.zeros((1, 3, 224, 224), np.float32)})

    def encode(self, images: list[Image.Image], batch_size: int = 16) -> np.ndarray:
        """L2-нормированные эмбеддинги [N, dim]."""
        out = []
        for i in range(0, len(images), batch_size):
            x = np.stack([preprocess(im) for im in images[i:i + batch_size]])
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
    tmp.replace(target)


def load_model(model_id: str = "fast", device: str = "auto", progress: Progress = lambda f, m: None) -> ClipOnnx:
    spec = MODELS[model_id]
    path = MODELS_DIR / spec.file
    if not path.exists():
        _download(spec, progress)
    progress(1.0, tr("model_mem"))
    return ClipOnnx(path, device, spec.dim)
