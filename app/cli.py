"""Режим без окна: AI-Anti-Duplicate --cli <папка_с_фото> <папка_для_уникальных> [--rule newest|largest|resolution]
[--model fast|accurate] [--device auto|cpu|gpu] [--sensitivity 0..100]. Только копирует файлы."""
import argparse
from pathlib import Path

from .core.clustering import cluster
from .core.embedder import embed_images
from .core.model_manager import MODELS, is_downloaded, load_model
from .data.models import DuplicateGroup
from .data.scanner import scan_folder
from .services.exporter import export_unique
from .services.selection import RULES


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(prog="AI-Anti-Duplicate --cli")
    ap.add_argument("src", type=Path)
    ap.add_argument("dst", type=Path)
    ap.add_argument("--rule", choices=[r for r in RULES if RULES[r]], default="newest")
    ap.add_argument("--model", choices=list(MODELS), default="fast")
    ap.add_argument("--device", choices=["auto", "cpu", "gpu"], default="auto")
    ap.add_argument("--sensitivity", type=int, default=33)
    a = ap.parse_args(argv)

    print(f"model={a.model} downloaded={is_downloaded(a.model)}")
    model = load_model(a.model, a.device, lambda f, m: print(f"\r{m}", end="", flush=True))
    print(f"\ndevice={model.device_name}")
    infos = [i for i in scan_folder(a.src) if not i.path.is_relative_to(a.dst)]
    kept, emb = embed_images(model, infos)
    thr = 0.98 - a.sensitivity * 0.0018 + MODELS[a.model].threshold_shift
    groups = []
    for idx in cluster(emb, thr):
        g = DuplicateGroup([kept[i] for i in idx])
        g.keep = RULES[a.rule](g)
        groups.append(g)
    n = export_unique(a.dst, groups, kept)
    print(f"images={len(kept)} groups={len(groups)} copied={n} threshold={thr:.3f}")
    for g in groups:
        print("GROUP", [i.path.name for i in g.images], "-> keep", g.images[g.keep].path.name)
    return 0
