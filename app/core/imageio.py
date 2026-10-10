"""Чтение изображений: обычные форматы через Pillow, RAW камер через rawpy (LibRaw)."""
import io
import logging
from pathlib import Path

from PIL import Image, ImageOps

log = logging.getLogger(__name__)

STANDARD_EXT = {".jpg", ".jpeg", ".png", ".webp"}
RAW_EXT = {".cr2", ".cr3", ".crw", ".nef", ".nrw", ".arw", ".srf", ".sr2", ".dng", ".orf", ".raf", ".rw2", ".rwl",
           ".pef", ".srw", ".raw", ".3fr", ".erf", ".kdc", ".mrw", ".mef", ".mos", ".iiq", ".x3f"}
SUPPORTED_EXT = STANDARD_EXT | RAW_EXT
MIN_THUMB_SIDE = 512  # если встроенное превью меньше — проявляем RAW (быстрый режим half_size)


def is_raw(path: Path) -> bool:
    return Path(path).suffix.lower() in RAW_EXT


def _raw_flip(raw) -> int:
    try:
        return int(raw.sizes.flip)
    except Exception:
        return 0


def _apply_flip(im: Image.Image, flip: int) -> Image.Image:
    return {3: im.transpose(Image.ROTATE_180), 5: im.transpose(Image.ROTATE_90), 6: im.transpose(Image.ROTATE_270)}.get(flip, im)


def _open_raw(path: Path) -> Image.Image:
    import rawpy

    with rawpy.imread(str(path)) as raw:
        flip = _raw_flip(raw)
        try:
            t = raw.extract_thumb()
            if t.format == rawpy.ThumbFormat.JPEG:
                im = Image.open(io.BytesIO(t.data))
                has_orientation = bool(im.getexif().get(274))
                im = ImageOps.exif_transpose(im).convert("RGB")
                if not has_orientation:
                    im = _apply_flip(im, flip)
            else:
                im = _apply_flip(Image.fromarray(t.data).convert("RGB"), flip)
            if min(im.size) >= MIN_THUMB_SIDE:
                return im
        except (rawpy.LibRawNoThumbnailError, rawpy.LibRawUnsupportedThumbnailError, rawpy.LibRawFileUnsupportedError):
            pass
        rgb = raw.postprocess(half_size=True, use_camera_wb=True, output_bps=8)  # уже с учётом поворота
        return Image.fromarray(rgb).convert("RGB")


def open_image(path: Path) -> Image.Image:
    """RGB-изображение с учётом поворота из EXIF; для RAW — встроенное превью или быстрая проявка."""
    path = Path(path)
    if is_raw(path):
        return _open_raw(path)
    with Image.open(path) as im:
        return ImageOps.exif_transpose(im).convert("RGB")


def image_size(path: Path) -> tuple[int, int]:
    """Размер в пикселях (для RAW — полный размер кадра)."""
    path = Path(path)
    if is_raw(path):
        import rawpy

        with rawpy.imread(str(path)) as raw:
            return int(raw.sizes.width), int(raw.sizes.height)
    with Image.open(path) as im:
        return im.size


def exif_datetime(path: Path):
    """Дата съёмки (datetime) или None."""
    from datetime import datetime

    path = Path(path)
    try:
        if is_raw(path):
            import rawpy

            with rawpy.imread(str(path)) as raw:
                t = raw.extract_thumb()
            if t.format != rawpy.ThumbFormat.JPEG:
                return None
            ex = Image.open(io.BytesIO(t.data)).getexif()
        else:
            with Image.open(path) as im:
                ex = im.getexif()
        sub = ex.get_ifd(0x8769)
        raw_value = sub.get(36867) or sub.get(36868) or ex.get(306)
        if raw_value:
            return datetime.strptime(str(raw_value).strip()[:19], "%Y:%m:%d %H:%M:%S")
    except Exception:
        pass
    return None
