import numpy as np

from app.core.clustering import cluster


def test_cluster_with_rotation():
    rng = np.random.default_rng(0)
    a = rng.normal(size=(3, 4, 8)).astype("float32")
    a /= np.linalg.norm(a, axis=2, keepdims=True)
    b = a[0].copy()[[1, 0, 2, 3]]  # "повёрнутая" копия: b[0] == a[0][1]
    emb = np.stack([a[0], b, a[1], a[2]])
    assert cluster(emb, 0.99) == [[0, 1]]
