import os
from collections.abc import Callable
from pathlib import Path

from .models import ImageInfo

EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def scan_folder(root: Path, should_stop: Callable[[], bool] = lambda: False) -> list[ImageInfo]:
    result: list[ImageInfo] = []
    for dirpath, _, files in os.walk(root):
        if should_stop():
            break
        for name in files:
            if Path(name).suffix.lower() in EXTENSIONS:
                p = Path(dirpath) / name
                try:
                    st = p.stat()
                except OSError:
                    continue
                result.append(ImageInfo(p, st.st_size, st.st_mtime))
    return result
