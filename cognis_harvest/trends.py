"""Cultivation trend analysis over a time series of scenes.

Turns a sequence of classified scenes into per-crop cultivation-area time series,
a least-squares growth rate (ha per time step), and expansion alerts — the
"is cultivation growing, and how fast?" question that drives interdiction
prioritization. Pure stdlib.
"""

from __future__ import annotations

CROP_CLASSES = {"coca", "poppy", "cannabis"}


def area_series(counts_by_step: list, pixel_area_ha: float, crop_classes=None) -> dict:
    """counts_by_step: list of {class: pixel_count} per time step.
    Returns {crop: [area_ha per step]}."""
    crop_classes = crop_classes or CROP_CLASSES
    return {c: [round(step.get(c, 0) * pixel_area_ha, 4) for step in counts_by_step]
            for c in sorted(crop_classes)}


def _slope(ys: list) -> float:
    """Least-squares slope over unit-spaced steps (ha per step)."""
    n = len(ys)
    if n < 2:
        return 0.0
    xm = (n - 1) / 2.0
    ym = sum(ys) / n
    num = sum((i - xm) * (y - ym) for i, y in enumerate(ys))
    den = sum((i - xm) ** 2 for i in range(n))
    return num / den if den else 0.0


def growth(series: dict) -> dict:
    """Per-crop growth rate (ha/step) and total change over the window."""
    out = {}
    for crop, ys in series.items():
        out[crop] = {
            "start_ha": ys[0] if ys else 0.0,
            "end_ha": ys[-1] if ys else 0.0,
            "rate_ha_per_step": round(_slope(ys), 4),
            "change_ha": round((ys[-1] - ys[0]) if ys else 0.0, 4),
            "change_pct": round(((ys[-1] - ys[0]) / ys[0] * 100) if ys and ys[0] else 0.0, 1),
        }
    return out


def expansion_alerts(series: dict, min_change_pct: float = 20.0) -> list:
    """Flag crops whose area grew by more than min_change_pct over the window."""
    alerts = []
    for crop, g in growth(series).items():
        if g["change_pct"] >= min_change_pct and g["change_ha"] > 0:
            alerts.append({"crop": crop, "change_pct": g["change_pct"],
                           "change_ha": g["change_ha"], "rate_ha_per_step": g["rate_ha_per_step"]})
    alerts.sort(key=lambda a: -a["change_pct"])
    return alerts
