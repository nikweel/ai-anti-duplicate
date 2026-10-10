from pathlib import Path

from PIL import Image

from app.core.embedder import _load
from app.core.imageio import RAW_EXT, STANDARD_EXT, SUPPORTED_EXT, image_size, is_raw, open_image
from app.data.models import ImageInfo
from app.data.scanner import scan_folder


def test_extension_sets():
    assert {".cr2", ".cr3", ".nef", ".arw", ".dng", ".raf", ".orf", ".rw2"} <= RAW_EXT
    assert STANDARD_EXT <= SUPPORTED_EXT and RAW_EXT <= SUPPORTED_EXT
    assert is_raw(Path("a/IMG_1.CR2")) and not is_raw(Path("a/b.jpg"))


def test_scanner_finds_raw_recursively_and_skips_other_files(tmp_path):
    for rel in ("a/1.CR2", "a/b/2.nef", "3.jpg", "c/4.ARW", "c/readme.txt", "c/5.mp4"):
        p = tmp_path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(b"x")
    names = sorted(i.path.name for i in scan_folder(tmp_path))
    assert names == ["1.CR2", "2.nef", "3.jpg", "4.ARW"]


def test_broken_raw_is_skipped_not_fatal(tmp_path):
    bad = tmp_path / "broken.CR2"
    bad.write_bytes(b"not a raw file at all")
    assert _load(ImageInfo(bad, bad.stat().st_size, 0.0)) is None


def test_standard_image_open_and_size(tmp_path):
    p = tmp_path / "x.png"
    Image.new("RGB", (30, 20), (1, 2, 3)).save(p)
    assert open_image(p).size == (30, 20) and image_size(p) == (30, 20)
