import os
from datetime import datetime
from pathlib import Path

from PIL import Image

from app.data.models import ImageInfo
from app.services.exporter import export_unique
from app.services.naming import NamingOptions, file_date, format_date, resolve


def _file(p: Path, data: bytes, mtime=None) -> Path:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data)
    if mtime:
        os.utime(p, (mtime, mtime))
    return p


def _info(p: Path) -> ImageInfo:
    st = p.stat()
    return ImageInfo(p, st.st_size, st.st_mtime)


def test_formats():
    d = datetime(2024, 5, 1, 12, 30, 45)
    assert format_date(d, "dash", "") == "2024-05-01_12-30-45"
    assert format_date(d, "compact", "") == "20240501_123045"
    assert format_date(d, "ts", "") == str(int(d.timestamp()))
    assert format_date(d, "ts_ms", "") == str(int(d.timestamp() * 1000))
    assert format_date(d, "custom", "IMG_%d.%m.%Y_{ts}") == f"IMG_01.05.2024_{int(d.timestamp())}"


def test_exif_date_preferred_over_file_date(tmp_path):
    p = tmp_path / "a.jpg"
    im = Image.new("RGB", (10, 10))
    ex = Image.Exif()
    ex.get_ifd(0x8769)[36867] = "2019:07:04 08:09:10"
    im.save(p, exif=ex)
    os.utime(p, (1_700_000_000, 1_700_000_000))
    assert file_date(p, "exif") == datetime(2019, 7, 4, 8, 9, 10)
    assert file_date(p, "modified") == datetime.fromtimestamp(1_700_000_000)


def test_exif_falls_back_to_file_date(tmp_path):
    p = tmp_path / "b.png"
    Image.new("RGB", (5, 5)).save(p)
    os.utime(p, (1_600_000_000, 1_600_000_000))
    assert file_date(p, "exif") == datetime.fromtimestamp(1_600_000_000)


def test_keep_names_conflict_counter_never_overwrites(tmp_path):
    a = _file(tmp_path / "s/Holiday/a.jpg", b"AAA")
    b = _file(tmp_path / "s/Work/a.jpg", b"BBBB")
    out = tmp_path / "o"
    export_unique(out, [], [_info(a), _info(b)], NamingOptions())
    assert sorted(x.name for x in out.iterdir()) == ["a.jpg", "a_1.jpg"]
    assert (out / "a.jpg").read_bytes() == b"AAA" and (out / "a_1.jpg").read_bytes() == b"BBBB"


def test_keep_names_conflict_prefix(tmp_path):
    a = _file(tmp_path / "s/Holiday/a.jpg", b"AAA")
    b = _file(tmp_path / "s/Work/a.jpg", b"BBBB")
    c = _file(tmp_path / "s2/Work/a.jpg", b"CCCCC")  # такая же папка-источник -> ещё и счётчик
    out = tmp_path / "o"
    export_unique(out, [], [_info(a), _info(b), _info(c)], NamingOptions(conflict="prefix"))
    assert sorted(x.name for x in out.iterdir()) == ["Work_a.jpg", "Work_a_1.jpg", "a.jpg"]


def test_date_names_same_second_conflict(tmp_path):
    t = 1_700_000_000
    a = _file(tmp_path / "s/Holiday/x.jpg", b"1", t)
    b = _file(tmp_path / "s/Work/y.jpg", b"22", t)
    out = tmp_path / "o"
    o = NamingOptions(mode="date", date_source="modified", date_format="compact", conflict="prefix")
    export_unique(out, [], [_info(a), _info(b)], o)
    stamp = datetime.fromtimestamp(t).strftime("%Y%m%d_%H%M%S")
    assert {x.name for x in out.iterdir()} == {f"Work_{stamp}.jpg", f"{stamp}.jpg"}


def test_date_names_counter_and_extension_kept(tmp_path):
    t = 1_700_000_000
    a = _file(tmp_path / "s/x.PNG", b"1", t)
    b = _file(tmp_path / "s/y.PNG", b"22", t)
    out = tmp_path / "o"
    export_unique(out, [], [_info(a), _info(b)], NamingOptions(mode="date", date_source="modified", date_format="ts"))
    assert sorted(x.name for x in out.iterdir()) == [f"{t}.PNG", f"{t}_1.PNG"]


def test_rerun_skips_identical_and_resolve_is_pure(tmp_path):
    a = _file(tmp_path / "s/a.jpg", b"AAA")
    out = tmp_path / "o"
    export_unique(out, [], [_info(a)], NamingOptions())
    export_unique(out, [], [_info(a)], NamingOptions())
    assert [x.name for x in out.iterdir()] == ["a.jpg"]
    dst, copy = resolve(out, a, NamingOptions())
    assert dst == out / "a.jpg" and copy is False
    assert a.read_bytes() == b"AAA"


def test_forbidden_characters_are_replaced(tmp_path):
    a = _file(tmp_path / "s/a.jpg", b"A", 1_700_000_000)
    out = tmp_path / "o"
    export_unique(out, [], [_info(a)], NamingOptions(mode="date", date_source="modified", date_format="custom", custom="%Y/%m/%d %H:%M"))
    names = [x.name for x in out.iterdir()]
    assert len(names) == 1 and "/" not in names[0] and ":" not in names[0]
