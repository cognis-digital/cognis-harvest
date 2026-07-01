"""Scene classification with multi-phenomenology fallback.

Classifies every pixel. When a pixel is cloud-flagged, optical bands are dropped
and classification falls back to the SAR band only (lower confidence, honest
degradation). Returns a per-pixel class map and per-class pixel counts.
"""

from __future__ import annotations

from .spectral import ndvi

CROP_CLASSES = {"coca", "poppy", "cannabis"}


def classify_scene(scene: dict, clf, optical_bands=None) -> dict:
    optical = set(optical_bands or ["blue", "green", "red", "nir", "swir1"])
    results = []
    counts: dict = {}
    for px in scene["pixels"]:
        v = px["values"]
        if px.get("cloud"):
            available = [b for b in scene["bands"] if b not in optical]  # SAR fallback
        else:
            available = list(scene["bands"])
        pred = clf.predict(v, available)
        counts[pred["label"]] = counts.get(pred["label"], 0) + 1
        results.append({
            "row": px["row"], "col": px["col"], "label": pred["label"],
            "confidence": pred["confidence"], "cloud": bool(px.get("cloud")),
            "ndvi": round(ndvi(v), 4) if not px.get("cloud") else None,
        })
    return {"scene_id": scene.get("id"), "pixels": results, "counts": counts}
