import numpy as np


def cluster(emb: np.ndarray, threshold: float = 0.92, block: int = 512) -> list[list[int]]:
    """Группы индексов (размер >= 2). emb: [N, R, D]; сходство = max по поворотам второго изображения."""
    n = len(emb)
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    base = emb[:, 0, :]
    rot = emb.reshape(n * emb.shape[1], -1) if n else emb
    for s in range(0, n, block):
        sims = base[s:s + block] @ rot.T  # [B, N*R]
        sims = sims.reshape(sims.shape[0], n, emb.shape[1]).max(axis=2)  # [B, N]
        rows, cols = np.nonzero(sims >= threshold)
        for r, c in zip(rows, cols):
            a, b = s + int(r), int(c)
            if a < b:
                parent[find(a)] = find(b)
    groups: dict[int, list[int]] = {}
    for i in range(n):
        groups.setdefault(find(i), []).append(i)
    return [g for g in groups.values() if len(g) > 1]
