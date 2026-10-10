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
    keep: list[int] = field(default_factory=lambda: [0])  # индексы сохраняемых файлов (можно несколько)
    members: list[int] = field(default_factory=list)
