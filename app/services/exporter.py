import csv
import shutil
from datetime import datetime
from pathlib import Path

from ..data.models import DuplicateGroup, ImageInfo
from ..utils.paths import LOG_DIR
from .naming import NamingOptions, resolve


def export_unique(
    out_dir: Path, groups: list[DuplicateGroup], all_images: list[ImageInfo], naming: NamingOptions | None = None
) -> int:
    """Копирует по одному файлу из каждой группы + все изображения без дубликатов.

    Исходные файлы не меняются и ничего не перезаписывается: идентичный файл в папке назначения
    пропускается, при конфликте имён подбирается свободное имя (см. naming.resolve).
    Возвращает число файлов, которые теперь есть в папке назначения из этого прогона.
    Соответствие «исходный -> результат» пишется в data/logs/last_export.csv."""
    naming = naming or NamingOptions()
    out_dir.mkdir(parents=True, exist_ok=True)
    grouped = {i.path for g in groups for i in g.images}
    to_copy = [i.path for i in all_images if i.path not in grouped]
    to_copy += [g.images[g.keep].path for g in groups]
    rows = []
    for src in to_copy:
        dst, need_copy = resolve(out_dir, src, naming)
        if need_copy:
            shutil.copy2(src, dst)
        rows.append((str(src), str(dst), "copied" if need_copy else "already_present"))
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        with open(LOG_DIR / "last_export.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["source", "destination", "status", "time"])
            now = datetime.now().isoformat(timespec="seconds")
            w.writerows((*r, now) for r in rows)
    except OSError:
        pass
    return len(rows)
