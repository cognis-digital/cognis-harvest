"""Deterministic synthetic multispectral data generator (with planted ground
truth). Used by the CLI demo and the verification harness.

SYNTHETIC ONLY: signatures are drawn from fixed class centroids with small
Gaussian noise. Real crop spectra overlap far more; synthetic separability is a
correctness lower bound, not a real-world accuracy claim.
"""

from __future__ import annotations

import random

BANDS = ["blue", "green", "red", "nir", "swir1", "sar"]

# Optical reflectance [0,1] + normalized SAR backscatter. SAR centroids for the
# crop classes are deliberately close (SAR separates vegetation structure, not
# species) so cloud-obscured (SAR-only) classification degrades realistically.
CENTROIDS = {
    "forest":   {"blue": .03, "green": .05, "red": .04, "nir": .45, "swir1": .18, "sar": .58},
    "soil":     {"blue": .12, "green": .15, "red": .20, "nir": .25, "swir1": .30, "sar": .22},
    "coca":     {"blue": .04, "green": .07, "red": .06, "nir": .38, "swir1": .22, "sar": .47},
    "poppy":    {"blue": .05, "green": .10, "red": .09, "nir": .30, "swir1": .25, "sar": .44},
    "cannabis": {"blue": .04, "green": .08, "red": .05, "nir": .42, "swir1": .20, "sar": .49},
}

DEFAULT_PATCHES = [("coca", 4, 4, 10, 10), ("poppy", 18, 6, 24, 12), ("cannabis", 8, 20, 14, 26)]


def _sample(rng, cls, noise):
    return {b: round(max(0.0, CENTROIDS[cls][b] + rng.gauss(0, noise)), 4) for b in BANDS}


def generate_training(seed: int = 7, per_class: int = 40, noise: float = 0.01) -> list:
    rng = random.Random(seed)
    out = []
    for cls in CENTROIDS:
        for _ in range(per_class):
            out.append({"class": cls, "values": _sample(rng, cls, noise)})
    return out


def generate_scene(seed: int = 11, profile: str = "clean", width: int = 32, height: int = 32,
                   noise: float = 0.012, patches=None, cloud_frac: float = 0.0):
    rng = random.Random(seed)
    patches = DEFAULT_PATCHES if patches is None else patches
    truth = [["forest" if (r + c) % 5 else "soil" for c in range(width)] for r in range(height)]
    for cls, r0, c0, r1, c1 in patches:
        for r in range(max(0, r0), min(height, r1)):
            for c in range(max(0, c0), min(width, c1)):
                truth[r][c] = cls
    if profile == "cloudy":
        cloud_frac = max(cloud_frac, 0.25)
    pixels = []
    for r in range(height):
        for c in range(width):
            cls = truth[r][c]
            v = _sample(rng, cls, noise)
            cloud = (cloud_frac > 0) and (rng.random() < cloud_frac)
            if cloud:
                for b in BANDS:
                    if b != "sar":
                        v[b] = round(min(1.0, 0.75 + rng.gauss(0, 0.03)), 4)
            pixels.append({"row": r, "col": c, "values": v, "cloud": cloud})
    scene = {
        "id": f"scene-{profile}", "pixel_area_ha": 0.09, "width": width, "height": height,
        "bands": BANDS,
        "geotransform": {"origin_lat": 9.5, "origin_lon": -79.9, "dlat": -0.001, "dlon": 0.001},
        "pixels": pixels,
    }
    flat_truth = {(r, c): truth[r][c] for r in range(height) for c in range(width)}
    return scene, flat_truth
