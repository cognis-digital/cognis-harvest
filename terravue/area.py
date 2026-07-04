"""Cultivation-area estimation from classified pixel counts.

Area = crop-pixel count x pixel ground area. A 95%-style confidence interval is
derived from the classifier's per-class accuracy (when supplied): the more error
in classification, the wider the reported interval — never a bare point estimate.
"""

from __future__ import annotations

CROP_CLASSES = {"coca", "poppy", "cannabis"}


def estimate_area(counts: dict, pixel_area_ha: float, crop_classes=None, accuracy=None) -> dict:
    crop_classes = crop_classes or CROP_CLASSES
    out = {}
    for c in sorted(crop_classes):
        n = counts.get(c, 0)
        area = n * pixel_area_ha
        ci = None
        if accuracy is not None:
            acc = accuracy.get(c, 1.0) if isinstance(accuracy, dict) else accuracy
            margin = (1.0 - acc) * area
            ci = [round(max(0.0, area - margin), 4), round(area + margin, 4)]
        out[c] = {"pixels": n, "area_ha": round(area, 4), "ci95_ha": ci}
    return out
