"""Accuracy evaluation against planted ground truth (clean + cloudy + change)."""

from __future__ import annotations

import json
from collections import Counter

from cognis_harvest import synth
from cognis_harvest.change import detect_change
from cognis_harvest.classify import NearestCentroid
from cognis_harvest.detect import CROP_CLASSES, classify_scene
from cognis_harvest.geojson import to_geojson, to_json

from .metrics import area_mape, classification_metrics, confusion_matrix, macro_f1, prf

CLASSES = list(synth.CENTROIDS.keys())


def _clf():
    return NearestCentroid(synth.BANDS).fit(synth.generate_training())


def _labels(scene, clf):
    return {(p["row"], p["col"]): p["label"] for p in classify_scene(scene, clf)["pixels"]}


def evaluate() -> dict:
    clf = _clf()

    # --- Clean scene: classification + area accuracy ---
    scene, truth = synth.generate_scene(profile="clean", width=32, height=32)
    pred = _labels(scene, clf)
    clean = classification_metrics(pred, truth, CLASSES)
    clean["macro_f1"] = macro_f1(pred, truth, CLASSES)
    clean["confusion"] = confusion_matrix(pred, truth, CLASSES)
    mape = area_mape(Counter(pred.values()), Counter(truth.values()),
                     CROP_CLASSES, scene["pixel_area_ha"])

    # --- Cloudy scene: honest degradation on cloud-obscured (SAR-only) pixels ---
    scloud, tcloud = synth.generate_scene(profile="cloudy", width=32, height=32)
    predc = _labels(scloud, clf)
    cloudy = classification_metrics(predc, tcloud, CLASSES)
    cloud_keys = [(p["row"], p["col"]) for p in scloud["pixels"] if p["cloud"]]
    clear_keys = [(p["row"], p["col"]) for p in scloud["pixels"] if not p["cloud"]]
    cloud_acc = round(sum(1 for k in cloud_keys if predc[k] == tcloud[k]) / max(1, len(cloud_keys)), 4)
    clear_acc = round(sum(1 for k in clear_keys if predc[k] == tcloud[k]) / max(1, len(clear_keys)), 4)

    # --- Change detection: t1 has coca only, t2 adds poppy + cannabis ---
    s1, _ = synth.generate_scene(seed=11, profile="clean", width=32, height=32,
                                 patches=[("coca", 4, 4, 10, 10)])
    s2, _ = synth.generate_scene(seed=11, profile="clean", width=32, height=32)
    ch = detect_change(s1, s2, clf)
    truth_new = set()
    for _cls, r0, c0, r1, c1 in [("poppy", 18, 6, 24, 12), ("cannabis", 8, 20, 14, 26)]:
        for r in range(r0, r1):
            for c in range(c0, c1):
                truth_new.add((r, c))
    pred_new = {(x["row"], x["col"]) for x in ch["new_cultivation"]}
    change = prf(pred_new, truth_new)

    # --- Determinism: GeoJSON identical across runs ---
    g1 = to_json(to_geojson(scene, classify_scene(scene, clf)))
    g2 = to_json(to_geojson(scene, classify_scene(scene, clf)))
    determinism = (g1 == g2)

    return {
        "dataset": {"scene_pixels": len(scene["pixels"]), "classes": len(CLASSES)},
        "classification_clean": clean,
        "area_mape_clean": mape,
        "classification_cloudy_overall": cloudy["overall_accuracy"],
        "accuracy_clear_pixels": clear_acc,
        "accuracy_cloud_pixels": cloud_acc,
        "change_detection": change,
        "determinism": determinism,
    }


def main():
    print(json.dumps(evaluate(), indent=2))


if __name__ == "__main__":
    main()
