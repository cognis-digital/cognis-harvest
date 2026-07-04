"""Terravue CLI."""

from __future__ import annotations

import argparse
import json
import os
import sys

from . import __version__, synth
from .area import estimate_area
from .change import detect_change
from .classify import NearestCentroid, load_training
from .detect import classify_scene
from .geojson import to_geojson, to_json
from .report import render_json, render_text
from .yield_model import estimate_yield, load_coefficients

_HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.normpath(os.path.join(_HERE, "..", "data"))


def _load(p):
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def _clf_from(training):
    return NearestCentroid(synth.BANDS).fit(training)


def _product(scene, clf, coefficients, accuracy=0.95):
    classified = classify_scene(scene, clf)
    area = estimate_area(classified["counts"], scene["pixel_area_ha"], accuracy=accuracy)
    yld = estimate_yield(area, coefficients)
    return {
        "scene_id": scene.get("id"),
        "total_pixels": len(scene["pixels"]),
        "cloud_pixels": sum(1 for p in scene["pixels"] if p.get("cloud")),
        "class_counts": classified["counts"],
        "area": area,
        "yield": yld,
    }, classified


def cmd_demo(args):
    clf = _clf_from(synth.generate_training())
    scene, _ = synth.generate_scene(profile=args.profile)
    coeffs = _load(os.path.join(DATA_DIR, "coefficients.json"))
    product, classified = _product(scene, clf, coeffs)
    print(render_text(product))
    if args.geojson:
        with open(args.geojson, "w", encoding="utf-8") as f:
            f.write(to_json(to_geojson(scene, classified)))
        print(f"\n[+] GeoJSON -> {args.geojson}")
    return 0


def cmd_estimate(args):
    clf = _clf_from(load_training(args.training))
    scene = _load(args.scene)
    coeffs = _load(args.coefficients) if args.coefficients else _load(os.path.join(DATA_DIR, "coefficients.json"))
    product, _ = _product(scene, clf, coeffs)
    print(render_json(product) if args.json else render_text(product))
    return 0


def cmd_classify(args):
    clf = _clf_from(load_training(args.training))
    print(json.dumps(classify_scene(_load(args.scene), clf)["counts"], indent=2))
    return 0


def cmd_change(args):
    clf = _clf_from(load_training(args.training))
    print(json.dumps(detect_change(_load(args.scene1), _load(args.scene2), clf), indent=2))
    return 0


def cmd_geojson(args):
    clf = _clf_from(load_training(args.training))
    scene = _load(args.scene)
    classified = classify_scene(scene, clf)
    print(to_json(to_geojson(scene, classified)))
    return 0


def cmd_trend(args):
    """Cultivation-trend demo: area over time, growth rate, expansion alerts."""
    from collections import Counter
    from . import synth
    from .classify import NearestCentroid
    from .detect import classify_scene
    from .trends import area_series, expansion_alerts, growth
    clf = NearestCentroid(synth.BANDS).fit(synth.generate_training())
    scenes = synth.growth_series(steps=args.steps)
    counts = [Counter(classify_scene(s, clf)["counts"]) for s in scenes]
    series = area_series(counts, scenes[0]["pixel_area_ha"])
    g = growth(series)
    print(f"COGNIS HARVEST | cultivation trend over {len(scenes)} time steps")
    for crop, ys in series.items():
        if any(ys):
            print(f"  {crop:9} area (ha): {ys}  rate {g[crop]['rate_ha_per_step']}/step  "
                  f"({g[crop]['change_pct']:+.0f}%)")
    for a in expansion_alerts(series):
        print(f"  ALERT expanding cultivation: {a['crop']} +{a['change_pct']:.0f}% "
              f"({a['change_ha']} ha)")
    return 0


def build_parser():
    p = argparse.ArgumentParser(prog="terravue",
                                description="Terravue — illicit-crop detection & yield estimation")
    p.add_argument("--version", action="version", version=f"terravue {__version__}")
    sub = p.add_subparsers(dest="command", required=True)

    d = sub.add_parser("demo", help="end-to-end demo on synthetic scene")
    d.add_argument("--profile", choices=["clean", "cloudy"], default="clean")
    d.add_argument("--geojson")
    d.set_defaults(func=cmd_demo)

    e = sub.add_parser("estimate", help="full detection + area + yield on a scene")
    e.add_argument("--scene", required=True)
    e.add_argument("--training", required=True)
    e.add_argument("--coefficients")
    e.add_argument("--json", action="store_true")
    e.set_defaults(func=cmd_estimate)

    c = sub.add_parser("classify", help="per-class pixel counts for a scene")
    c.add_argument("--scene", required=True)
    c.add_argument("--training", required=True)
    c.set_defaults(func=cmd_classify)

    ch = sub.add_parser("change", help="change detection between two scenes")
    ch.add_argument("--scene1", required=True)
    ch.add_argument("--scene2", required=True)
    ch.add_argument("--training", required=True)
    ch.set_defaults(func=cmd_change)

    g = sub.add_parser("geojson", help="export detected cultivation as GeoJSON")
    g.add_argument("--scene", required=True)
    g.add_argument("--training", required=True)
    g.set_defaults(func=cmd_geojson)

    t = sub.add_parser("trend", help="cultivation-area trend + expansion alerts (time series)")
    t.add_argument("--steps", type=int, default=4)
    t.set_defaults(func=cmd_trend)
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
