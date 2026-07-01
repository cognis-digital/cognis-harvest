"""Human-readable and JSON estimation products."""

from __future__ import annotations

import json


def render_json(product) -> str:
    return json.dumps(product, indent=2)


def render_text(product) -> str:
    L = []
    L.append("=" * 72)
    L.append("  COGNIS HARVEST  |  Illicit-Crop Detection & Yield Estimate")
    L.append("  Cognis Digital LLC - estimates with confidence intervals, not certainties")
    L.append("=" * 72)
    L.append(f"Scene        : {product['scene_id']}")
    L.append(f"Cloud pixels : {product['cloud_pixels']} / {product['total_pixels']}")
    L.append("")
    L.append("Cultivation area (95% CI from classifier accuracy):")
    for c, a in sorted(product["area"].items()):
        ci = a["ci95_ha"]
        ci_s = f"  CI[{ci[0]}, {ci[1]}] ha" if ci else ""
        L.append(f"   {c:>9}: {a['area_ha']:.2f} ha ({a['pixels']} px){ci_s}")
    L.append("")
    L.append("Yield & market value (ILLUSTRATIVE coefficients):")
    for c, y in sorted(product["yield"].items()):
        L.append(f"   {c:>9}: {y['production_kg']:,.0f} kg  ~${y['market_value_usd']:,.0f}")
    L.append("")
    L.append("NOTE: Early-prototype on supplied/synthetic spectral data. Coefficients")
    L.append("illustrative; operational use needs calibrated region-specific inputs.")
    return "\n".join(L)
