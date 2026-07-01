# Architecture

```
 multispectral scene ─► spectral (indices)
                     └─► classify (nearest-centroid) ─► detect (per-pixel + SAR fallback)
                                                          ├─► area (ha + CI)
                                                          ├─► yield_model (production/value)
                                                          ├─► change (t1 vs t2)
                                                          └─► geojson (export)
```

| Module | Responsibility |
|---|---|
| `spectral` | NDVI / SAVI / NDWI / NBR indices. |
| `classify` | Nearest-centroid classifier; subset-band (SAR-only) support. |
| `detect` | Scene classification + cloud→SAR fallback; per-class counts. |
| `area` | Area estimation with confidence intervals. |
| `yield_model` | Production & market-value estimation. |
| `change` | New/removed cultivation between scenes. |
| `geojson` | Geolocated export via scene geotransform. |
| `synth` | Deterministic synthetic scenes + ground truth (demo/bench). |
| `report`, `cli` | Products and command-line entry. |

## Principles
1. **Honest uncertainty** — area estimates carry confidence intervals; cloud
   degradation is measured, not hidden.
2. **Multi-phenomenology** — optical primary, SAR fallback under cloud.
3. **Offline / zero-dependency** — deployable in restricted environments.
4. **Deterministic & reproducible** — fixed synthetic generation; stable GeoJSON.
