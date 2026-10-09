import shutil
from pathlib import Path

from ..data.models import DuplicateGroup, ImageInfo


def export_unique(
    out_dir: Path, groups: list[DuplicateGroup], all_images: list[ImageInfo]
) -> int:
    """Копирует по одному файлу из каждой группы + все изображения без дубликатов."""
    out_dir.mkdir(parents=True, exist_ok=True)
    grouped = {i.path for g in groups for i in g.images}
    to_copy = [i.path for i in all_images if i.path not in grouped]
    to_copy += [g.images[g.keep].path for g in groups]
    for src in to_copy:
        dst = out_dir / src.name
        n = 1
        while dst.exists():
            dst = out_dir / f"{src.stem}_{n}{src.suffix}"
            n += 1
        shutil.copy2(src, dst)
    return len(to_copy)
