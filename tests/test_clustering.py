import numpy as np

from app.core.clustering import cluster


def test_cluster_with_rotation():
    rng = np.random.default_rng(0)
    a = rng.normal(size=(3, 4, 8)).astype("float32")
    a /= np.linalg.norm(a, axis=2, keepdims=True)
    b = a[0].copy()[[1, 0, 2, 3]]  # "повёрнутая" копия: b[0] == a[0][1]
    emb = np.stack([a[0], b, a[1], a[2]])
    assert cluster(emb, 0.99) == [[0, 1]]


def _unit(v):
    v = np.asarray(v, "float32")
    return v / np.linalg.norm(v)


def test_chain_is_not_merged():
    # A~B и B~C похожи, но A и C — разные кадры: в одну группу их склеивать нельзя
    a, c = _unit([1, 0, 0]), _unit([0, 1, 0])
    b = _unit([1, 1, 0])  # ~0.707 к обоим
    emb = np.stack([a, b, c])[:, None, :]  # один «поворот»
    groups = cluster(emb, 0.7)
    assert all(len(g) == 2 for g in groups) and not any({0, 2} <= set(g) for g in groups)


def test_real_duplicates_stay_together():
    a = _unit([1, 0.02, 0])
    emb = np.stack([a, _unit([1, 0, 0.02]), _unit([1, 0.01, 0.01]), _unit([0, 0, 1])])[:, None, :]
    assert cluster(emb, 0.95) == [[0, 1, 2]]
