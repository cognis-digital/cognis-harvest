"""Export detected cultivation as GeoJSON (pixel row/col -> lat/lon via the
scene geotransform) for partner-nation and analyst platforms."""

from __future__ import annotations

import json

from .detect import CROP_CLASSES


def to_geojson(scene: dict, classified: dict, crop_classes=None) -> dict:
    crop = crop_classes or CROP_CLASSES
    gt = scene["geotransform"]
    feats = []
    for p in classified["pixels"]:
        if p["label"] in crop:
            lat = gt["origin_lat"] + p["row"] * gt["dlat"]
            lon = gt["origin_lon"] + p["col"] * gt["dlon"]
            feats.append({
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [round(lon, 6), round(lat, 6)]},
                "properties": {"class": p["label"], "confidence": p["confidence"]},
            })
    return {"type": "FeatureCollection", "features": feats}


def to_json(fc: dict, indent: int = 2) -> str:
    return json.dumps(fc, indent=indent)
