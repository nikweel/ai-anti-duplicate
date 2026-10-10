import logging
from collections.abc import Callable

import numpy as np
from PIL import Image

from ..data.models import ImageInfo
from .imageio import open_image

log = logging.getLogger(__name__)
ROTATIONS = (0, 90, 180, 270)


def _load(info: ImageInfo) -> Image.Image | None:
    try:
        im = open_image(info.path)
        im.thumbnail((256, 256))  # модель всё равно уменьшает до 224
        return im
    except Exception as e:  # битый файл или RAW без поддержки не должен ронять сканирование
        log.warning("Пропущен %s: %s", info.path, e)
        return None


def embed_images(
    model,
    infos: list[ImageInfo],
    rotations: bool = True,
    batch_size: int = 8,
    progress: Callable[[int, int], None] = lambda d, t: None,
    should_stop: Callable[[], bool] = lambda: False,
    checkpoint: Callable[[], None] = lambda: None,
) -> tuple[list[ImageInfo], np.ndarray]:
    """Возвращает (успешные файлы, эмбеддинги формы [N, R, D]), L2-нормированные.

    checkpoint() вызывается между шагами: там программа может стоять на паузе;
    should_stop() — запрос отмены (недосчитанная порция отбрасывается)."""
    angles = ROTATIONS if rotations else (0,)
    kept: list[ImageInfo] = []
    chunks: list[np.ndarray] = []
    for start in range(0, len(infos), batch_size):
        checkpoint()
        if should_stop():
            break
        batch = [(i, im) for i in infos[start:start + batch_size] if (im := _load(i)) is not None]
        if batch:
            imgs = [im for _, im in batch]
            per_angle = []
            for a in angles:
                checkpoint()
                if should_stop():
                    break
                per_angle.append(model.encode(imgs if a == 0 else [im.rotate(-a, expand=True) for im in imgs], batch_size))
            if len(per_angle) < len(angles):  # отмена в середине порции
                break
            chunks.append(np.stack(per_angle, axis=1).astype(np.float32))
            kept.extend(i for i, _ in batch)
        progress(min(start + batch_size, len(infos)), len(infos))
    emb = np.concatenate(chunks) if chunks else np.zeros((0, len(angles), 1), np.float32)
    return kept, emb
