"""Change detection between two classified scenes of the same grid.

Flags pixels that transitioned into cultivation (new) or out of it (removed),
the signal for catching crop-cycle changes within a growing season.
"""

from __future__ import annotations

from .detect import CROP_CLASSES, classify_scene


def detect_change(scene_t1: dict, scene_t2: dict, clf, crop_classes=None) -> dict:
    crop = crop_classes or CROP_CLASSES
    c1 = {(p["row"], p["col"]): p for p in classify_scene(scene_t1, clf)["pixels"]}
    new, removed = [], []
    for p in classify_scene(scene_t2, clf)["pixels"]:
        key = (p["row"], p["col"])
        prev = c1.get(key)
        was_crop = bool(prev) and prev["label"] in crop
        now_crop = p["label"] in crop
        if now_crop and not was_crop:
            new.append({"row": key[0], "col": key[1], "class": p["label"]})
        elif was_crop and not now_crop:
            removed.append({"row": key[0], "col": key[1]})
    return {"new_cultivation": new, "removed_cultivation": removed}
