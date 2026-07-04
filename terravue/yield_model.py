"""Multi-source yield & market-value estimation.

production = area_ha x yield_kg_per_ha x climate_factor x soil_factor
market_value = production x price_per_kg

Coefficients are ILLUSTRATIVE (see data/coefficients.json and docs). Real
estimates require calibrated, region-specific agronomic inputs.
"""

from __future__ import annotations

import json


def load_coefficients(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def estimate_yield(area_by_class: dict, coefficients: dict) -> dict:
    cf = coefficients.get("climate_factor", 1.0)
    sf = coefficients.get("soil_factor", 1.0)
    crops = coefficients.get("crops", {})
    out = {}
    for c, info in area_by_class.items():
        coef = crops.get(c)
        if not coef:
            continue
        ah = info["area_ha"]
        production = ah * coef["yield_kg_per_ha"] * cf * sf
        value = production * coef["price_per_kg"]
        out[c] = {"area_ha": ah,
                  "production_kg": round(production, 2),
                  "market_value_usd": round(value, 2)}
    return out
