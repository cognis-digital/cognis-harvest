# SOLIC Challenge Area 4 — Capability Mapping

| Desired capability | Cognis Harvest | Module |
|---|---|---|
| AI/ML detection of coca/poppy/cannabis from multispectral imagery | Nearest-centroid spectral classifier over multispectral signatures | `classify`, `detect` |
| Automated area estimation with confidence intervals | Pixel-count × ground-area with accuracy-derived CIs | `area` |
| Multi-source yield modeling (production + market value) | Area × yield/ha × climate × soil × price | `yield_model` |
| Performance through cloud via multi-phenomenology | Optical primary + SAR-only fallback on cloud pixels | `detect` |
| Sub-annual change detection within a growing season | New/removed cultivation between two scenes | `change` |
| Partner-nation-shareable products | GeoJSON export with geolocation | `geojson` |

## TRL posture (honest)
- **Core analytics (working, measured):** spectral indexing, classification,
  area/CI, yield, change, GeoJSON — all tested with reproducible metrics.
- **Crop-estimation application (early prototype):** real-imagery ingestion,
  calibrated coefficients, and validation against partner-nation ground truth are
  the post-award prototype scope. We would validate on a bounded pilot region and
  report accuracy with confidence intervals — and we are open to teaming with an
  imagery or agronomic-modeling partner.

This is deliberately the most exploratory of the Cognis SOLIC submissions; it is
presented as such rather than overclaimed.
