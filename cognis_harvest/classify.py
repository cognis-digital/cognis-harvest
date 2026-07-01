"""Spectral classifier (nearest-centroid, stdlib).

Trains per-class centroids from labeled spectral samples and classifies pixels
by minimum Euclidean distance over the available bands, returning a softmax
confidence. Supports classifying over a subset of bands (multi-phenomenology
fallback, e.g. SAR-only when optical is cloud-obscured).
"""

from __future__ import annotations

import json
import math


class NearestCentroid:
    def __init__(self, bands):
        self.bands = list(bands)
        self.centroids: dict = {}

    def fit(self, samples: list) -> "NearestCentroid":
        acc: dict = {}
        cnt: dict = {}
        for s in samples:
            c = s["class"]
            v = s["values"]
            acc.setdefault(c, [0.0] * len(self.bands))
            cnt[c] = cnt.get(c, 0) + 1
            for i, b in enumerate(self.bands):
                acc[c][i] += float(v.get(b, 0.0))
        self.centroids = {c: [x / cnt[c] for x in vec] for c, vec in acc.items()}
        return self

    def predict(self, values: dict, available=None, scale: float = 0.08) -> dict:
        avail = set(available or self.bands)
        idxs = [i for i, b in enumerate(self.bands) if b in avail]
        dists = {}
        for c, cen in self.centroids.items():
            d = 0.0
            for i in idxs:
                d += (float(values.get(self.bands[i], 0.0)) - cen[i]) ** 2
            dists[c] = math.sqrt(d)
        exps = {c: math.exp(-d / scale) for c, d in dists.items()}
        Z = sum(exps.values()) or 1.0
        label = min(dists, key=dists.get)
        return {"label": label, "confidence": round(exps[label] / Z, 4),
                "distances": {c: round(d, 4) for c, d in dists.items()}}


def load_training(path: str) -> list:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
