import threading
import time
from pathlib import Path

import numpy as np
from PIL import Image

from app.core.embedder import embed_images
from app.data.models import ImageInfo
from app.services.exporter import export_unique


class FakeModel:
    dim = 4

    def __init__(self):
        self.calls = 0

    def encode(self, imgs, batch_size=8):
        self.calls += 1
        return np.ones((len(imgs), 4), np.float32) / 2


def _imgs(tmp_path, n):
    out = []
    for i in range(n):
        p = tmp_path / f"{i}.png"
        Image.new("RGB", (32, 32), (i * 5 % 255, 0, 0)).save(p)
        out.append(ImageInfo(p, p.stat().st_size, 0.0))
    return out


def test_cancel_stops_embedding_and_drops_partial_batch(tmp_path):
    infos, model, seen = _imgs(tmp_path, 40), FakeModel(), {"stop": False}

    def progress(d, t):
        if d >= 16:
            seen["stop"] = True

    kept, emb = embed_images(model, infos, True, 8, progress, lambda: seen["stop"])
    assert 16 <= len(kept) < 40 and emb.shape[0] == len(kept) and emb.shape[1] == 4


def test_pause_blocks_until_resumed(tmp_path):
    infos, model = _imgs(tmp_path, 16), FakeModel()
    gate = threading.Event()
    result = {}

    def work():
        result["r"] = embed_images(model, infos, False, 4, checkpoint=lambda: gate.wait(5))

    t = threading.Thread(target=work)
    t.start()
    time.sleep(0.3)
    assert model.calls == 0 and t.is_alive()  # на паузе ничего не посчитано
    gate.set()
    t.join(10)
    assert len(result["r"][0]) == 16


def test_export_cancel_keeps_copied_and_rerun_finishes(tmp_path):
    srcs = []
    for i in range(6):
        p = tmp_path / "s" / f"{i}.jpg"
        p.parent.mkdir(exist_ok=True)
        p.write_bytes(bytes([i]) * 10)
        srcs.append(ImageInfo(p, 10, 0.0))
    out = tmp_path / "o"
    n_done = {"n": 0}

    def progress(d, t):
        n_done["n"] = d

    export_unique(out, [], srcs, progress=progress, should_stop=lambda: n_done["n"] >= 3)
    assert len(list(out.iterdir())) == 3  # остановились, ничего не потеряно
    export_unique(out, [], srcs)           # повторный запуск докопирует остальное без дублей
    assert len(list(out.iterdir())) == 6
