import logging
import urllib.request
from collections.abc import Callable

import numpy as np
from PIL import Image

from ..utils.paths import MODELS_DIR

log = logging.getLogger(__name__)
MODEL_FILE = MODELS_DIR / "clip_vision.onnx"
# Адрес, откуда модель скачивается при первом запуске, если файла нет (задаётся при публикации).
MODEL_URL = ""
Progress = Callable[[float, str], None]

_MEAN = np.array([0.48145466, 0.4578275, 0.40821073], np.float32)
_STD = np.array([0.26862954, 0.26130258, 0.27577711], np.float32)


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


class ClipOnnx:
    def __init__(self, path):
        import onnxruntime as ort

        self.session = ort.InferenceSession(str(path), providers=["CPUExecutionProvider"])

    def encode(self, images: list[Image.Image], batch_size: int = 16) -> np.ndarray:
        """L2-нормированные эмбеддинги [N, 512]."""
        out = []
        for i in range(0, len(images), batch_size):
            x = np.stack([preprocess(im) for im in images[i:i + batch_size]])
            e = self.session.run(None, {"pixel_values": x})[0]
            out.append(e / np.linalg.norm(e, axis=1, keepdims=True))
        return np.concatenate(out).astype(np.float32) if out else np.zeros((0, 512), np.float32)


def _download(progress: Progress) -> None:
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    tmp = MODEL_FILE.with_suffix(".part")

    def hook(blocks, bs, total):
        if total > 0:
            progress(min(1.0, blocks * bs / total), f"Загрузка модели: {min(blocks * bs, total) / 1e6:.0f}/{total / 1e6:.0f} МБ")

    urllib.request.urlretrieve(MODEL_URL, tmp, hook)
    tmp.replace(MODEL_FILE)


def load_model(progress: Progress = lambda f, m: None) -> ClipOnnx:
    if not MODEL_FILE.exists():
        if not MODEL_URL:
            raise FileNotFoundError(f"Не найден файл модели {MODEL_FILE}")
        _download(progress)
    progress(1.0, "Загрузка модели в память...")
    return ClipOnnx(MODEL_FILE)
