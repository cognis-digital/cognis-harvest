"""Spectral indices from multispectral reflectance bands.

Standard remote-sensing indices used as features and vegetation filters.
Bands are reflectance values in [0,1]: blue, green, red, nir, swir1 (+ sar).
"""

from __future__ import annotations


def _safe(num: float, den: float) -> float:
    return num / den if den else 0.0


def ndvi(v: dict) -> float:
    """Normalized Difference Vegetation Index."""
    return _safe(v["nir"] - v["red"], v["nir"] + v["red"])


def savi(v: dict, L: float = 0.5) -> float:
    """Soil-Adjusted Vegetation Index."""
    return _safe((v["nir"] - v["red"]) * (1 + L), v["nir"] + v["red"] + L)


def ndwi(v: dict) -> float:
    """Normalized Difference Water Index (green/nir)."""
    return _safe(v["green"] - v["nir"], v["green"] + v["nir"])


def nbr(v: dict) -> float:
    """Normalized Burn Ratio (nir/swir1) — proxy for canopy moisture/structure."""
    return _safe(v["nir"] - v["swir1"], v["nir"] + v["swir1"])


def indices(v: dict) -> dict:
    return {"ndvi": round(ndvi(v), 4), "savi": round(savi(v), 4),
            "ndwi": round(ndwi(v), 4), "nbr": round(nbr(v), 4)}
