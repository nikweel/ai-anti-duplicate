from pathlib import Path

from app.data.models import DuplicateGroup, ImageInfo
from app.services.exporter import export_unique


def _img(p: Path, data: bytes) -> ImageInfo:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data)
    st = p.stat()
    return ImageInfo(p, st.st_size, st.st_mtime)


def test_rerun_is_idempotent_and_never_touches_sources(tmp_path):
    a, b, c = _img(tmp_path / "s/a.jpg", b"AAA"), _img(tmp_path / "s/x/a.jpg", b"BBBB"), _img(tmp_path / "s/c.jpg", b"C")
    out = tmp_path / "out"
    export_unique(out, [], [a, b, c])  # одинаковое имя, разное содержимое -> суффикс
    assert sorted(p.name for p in out.iterdir()) == ["a.jpg", "a_1.jpg", "c.jpg"]
    export_unique(out, [], [a, b, c])  # повтор: ничего нового
    assert len(list(out.iterdir())) == 3
    assert a.path.read_bytes() == b"AAA" and b.path.read_bytes() == b"BBBB"


def test_group_keeps_chosen_only(tmp_path):
    a, b = _img(tmp_path / "s/a.jpg", b"1"), _img(tmp_path / "s/b.jpg", b"22")
    g = DuplicateGroup([a, b], keep=1)
    export_unique(tmp_path / "o", [g], [a, b])
    assert [p.name for p in (tmp_path / "o").iterdir()] == ["b.jpg"]
