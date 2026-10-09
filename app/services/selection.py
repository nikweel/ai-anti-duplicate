from ..data.models import DuplicateGroup


def pick_newest(g: DuplicateGroup) -> int:
    return max(range(len(g.images)), key=lambda i: g.images[i].mtime)


def pick_largest(g: DuplicateGroup) -> int:
    return max(range(len(g.images)), key=lambda i: g.images[i].size)


def _pixels(path) -> int:
    from PIL import Image

    try:
        with Image.open(path) as im:
            return im.width * im.height
    except Exception:
        return 0


def pick_resolution(g: DuplicateGroup) -> int:
    return max(range(len(g.images)), key=lambda i: (_pixels(g.images[i].path), g.images[i].size))


RULES = {
    "Оставлять самый новый": pick_newest,
    "Оставлять самый тяжёлый (вес файла)": pick_largest,
    "Оставлять самый большой по разрешению": pick_resolution,
    "Выбирать вручную для каждого кадра": None,
}
