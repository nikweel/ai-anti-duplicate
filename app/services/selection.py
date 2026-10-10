from ..data.models import DuplicateGroup


def pick_newest(g: DuplicateGroup) -> int:
    return max(range(len(g.images)), key=lambda i: g.images[i].mtime)


def pick_largest(g: DuplicateGroup) -> int:
    return max(range(len(g.images)), key=lambda i: g.images[i].size)


def _pixels(path) -> int:
    from ..core.imageio import image_size

    try:
        w, h = image_size(path)
        return w * h
    except Exception:
        return 0


def pick_resolution(g: DuplicateGroup) -> int:
    return max(range(len(g.images)), key=lambda i: (_pixels(g.images[i].path), g.images[i].size))


RULES = {  # id -> функция выбора (None = вручную)
    "newest": pick_newest,
    "largest": pick_largest,
    "resolution": pick_resolution,
    "manual": None,
}
