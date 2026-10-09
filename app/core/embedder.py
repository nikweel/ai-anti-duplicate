import logging
from collections.abc import Callable

import numpy as np
from PIL import Image, ImageOps

from ..data.models import ImageInfo

log = logging.getLogger(__name__)
ROTATIONS = (0, 90, 180, 270)


def _load(info: ImageInfo) -> Image.Image | None:
    try:
        with Image.open(info.path) as im:
            im = ImageOps.exif_transpose(im).convert("RGB")
            im.thumbnail((256, 256))  # CLIP всё равно уменьшает до 224
            return im.copy()
    except Exception as e:  # битый файл не должен ронять сканирование
        log.warning("Пропущен %s: %s", info.path, e)
        return None


def embed_images(
    model,
    infos: list[ImageInfo],
    rotations: bool = True,
    batch_size: int = 32,
    progress: Callable[[int, int], None] = lambda d, t: None,
    should_stop: Callable[[], bool] = lambda: False,
) -> tuple[list[ImageInfo], np.ndarray]:
    """Возвращает (успешные файлы, эмбеддинги формы [N, R, D]), L2-нормированные."""
    angles = ROTATIONS if rotations else (0,)
    kept: list[ImageInfo] = []
    chunks: list[np.ndarray] = []
    for start in range(0, len(infos), batch_size):
        if should_stop():
            break
        batch = [(i, im) for i in infos[start:start + batch_size] if (im := _load(i)) is not None]
        if batch:
            imgs = [im for _, im in batch]
            per_angle = [model.encode(imgs if a == 0 else [im.rotate(-a, expand=True) for im in imgs], batch_size) for a in angles]
            chunks.append(np.stack(per_angle, axis=1).astype(np.float32))
            kept.extend(i for i, _ in batch)
        progress(min(start + batch_size, len(infos)), len(infos))
    emb = np.concatenate(chunks) if chunks else np.zeros((0, len(angles), 1), np.float32)
    return kept, emb
