"""Имена файлов при копировании: как есть / по дате, и разрешение конфликтов без потери данных."""
import filecmp
import re
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path

DATE_FORMATS = {
    "dash": "%Y-%m-%d_%H-%M-%S",
    "compact": "%Y%m%d_%H%M%S",
    "ts": None,        # unix timestamp, секунды
    "ts_ms": None,     # unix timestamp, миллисекунды
    "custom": None,    # свой шаблон
}
_BAD = re.compile(r'[<>:"/\\|?*\x00-\x1f]')


@dataclass
class NamingOptions:
    mode: str = "keep"          # keep | date
    date_source: str = "exif"   # exif (дата съёмки, иначе дата файла) | created | modified
    date_format: str = "dash"   # ключ DATE_FORMATS
    custom: str = "%Y-%m-%d_%H-%M-%S"
    conflict: str = "counter"   # counter (_1, _2) | prefix (имя папки-источника, затем счётчик)

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(d: dict | None) -> "NamingOptions":
        o = NamingOptions()
        for k, v in (d or {}).items():
            if hasattr(o, k):
                setattr(o, k, v)
        return o


def _exif_date(path: Path) -> datetime | None:
    from ..core.imageio import exif_datetime

    return exif_datetime(path)


def file_date(path: Path, source: str) -> datetime:
    st = path.stat()
    if source == "exif":
        d = _exif_date(path)
        if d:
            return d
    if source in ("exif", "created"):  # дата создания; на Linux её нет у многих ФС -> дата изменения
        ts = getattr(st, "st_birthtime", None) or st.st_mtime
    else:
        ts = st.st_mtime
    return datetime.fromtimestamp(ts)


def format_date(d: datetime, fmt: str, custom: str) -> str:
    ts = d.timestamp()
    if fmt == "ts":
        return str(int(ts))
    if fmt == "ts_ms":
        return str(int(ts * 1000))
    pattern = custom if fmt == "custom" else DATE_FORMATS[fmt]
    pattern = pattern.replace("{ts}", str(int(ts))).replace("{ms}", str(int(ts * 1000)))
    return d.strftime(pattern)


def clean(name: str) -> str:
    name = _BAD.sub("_", name).strip(" .")
    return name or "file"


def base_name(src: Path, o: NamingOptions) -> str:
    if o.mode == "date":
        return clean(format_date(file_date(src, o.date_source), o.date_format, o.custom))
    return clean(src.stem)


def resolve(dst_dir: Path, src: Path, o: NamingOptions) -> tuple[Path, bool]:
    """Возвращает (путь назначения, нужно_копировать). Существующие файлы не перезаписываются:
    идентичный файл пропускается, при другом содержимом подбирается свободное имя."""
    ext = src.suffix
    base = base_name(src, o)

    def free_or_same(p: Path) -> tuple[bool, bool]:  # (можно использовать, копировать)
        if not p.exists():
            return True, True
        return (True, False) if filecmp.cmp(src, p, shallow=False) else (False, False)

    ok, copy = free_or_same(dst_dir / f"{base}{ext}")
    if ok:
        return dst_dir / f"{base}{ext}", copy
    if o.conflict == "prefix":
        prefix = clean(src.parent.name)
        base = f"{prefix}_{base}"
        ok, copy = free_or_same(dst_dir / f"{base}{ext}")
        if ok:
            return dst_dir / f"{base}{ext}", copy
    n = 1
    while True:
        p = dst_dir / f"{base}_{n}{ext}"
        ok, copy = free_or_same(p)
        if ok:
            return p, copy
        n += 1
