import numpy as np


def _pair_sims(emb: np.ndarray, idx: list[int]) -> np.ndarray:
    """Матрица сходства внутри набора: max по поворотам, симметричная."""
    sub = emb[idx]
    k, r, _ = sub.shape
    s = (sub[:, 0, :] @ sub.reshape(k * r, -1).T).reshape(k, k, r).max(axis=2)
    return np.maximum(s, s.T)


def _split_complete(emb: np.ndarray, comp: list[int], threshold: float) -> list[list[int]]:
    """Разбивает связную компоненту так, чтобы КАЖДАЯ пара в группе была похожа (без «цепочек» A~B, B~C)."""
    if len(comp) <= 2:
        return [comp] if len(comp) == 2 else []
    s = _pair_sims(emb, comp)
    ok = s >= threshold
    left = set(range(len(comp)))
    groups = []
    while left:
        seed = max(left, key=lambda i: int(sum(ok[i, j] for j in left)))
        group = [seed]
        for c in sorted(left - {seed}, key=lambda j: -s[seed, j]):
            if all(ok[c, g] for g in group):
                group.append(c)
        left -= set(group)
        if len(group) > 1:
            groups.append([comp[i] for i in sorted(group)])
    return groups


def cluster(emb: np.ndarray, threshold: float = 0.92, block: int = 512) -> list[list[int]]:
    """Группы индексов (размер >= 2). emb: [N, R, D]; сходство = max по поворотам второго изображения.

    Сначала находим связные компоненты (быстро, блоками), затем внутри каждой требуем,
    чтобы все пары были похожи: так разные снимки не склеиваются цепочкой."""
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
    comps: dict[int, list[int]] = {}
    for i in range(n):
        comps.setdefault(find(i), []).append(i)
    out: list[list[int]] = []
    for comp in comps.values():
        if len(comp) > 1:
            out.extend(_split_complete(emb, comp, threshold))
    return out
