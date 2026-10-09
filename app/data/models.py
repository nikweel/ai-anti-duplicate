from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class ImageInfo:
    path: Path
    size: int
    mtime: float


@dataclass
class DuplicateGroup:
    images: list[ImageInfo]
    keep: int = 0  # индекс сохраняемого файла
    members: list[int] = field(default_factory=list)
