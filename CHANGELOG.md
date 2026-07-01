# Changelog

Adheres to [Semantic Versioning](https://semver.org/).

## [0.1.0] — 2026-07-01

Initial public release (early prototype).

### Added
- Spectral indices (NDVI, SAVI, NDWI, NBR) — `spectral`.
- Nearest-centroid spectral classifier with subset-band (SAR fallback) support — `classify`.
- Scene classification with cloud → SAR-only multi-phenomenology fallback — `detect`.
- Cultivation-area estimation with confidence intervals — `area`.
- Multi-source yield & market-value estimation (illustrative coefficients) — `yield_model`.
- Change detection between scenes — `change`.
- GeoJSON export via scene geotransform — `geojson`.
- Deterministic synthetic data generator with planted ground truth — `synth`.
- CLI (`cognis-harvest`) with `demo`, `estimate`, `classify`, `change`, `geojson`.
- Zero-dependency, offline.
- Verification harness (`bench/`): classification/area/change accuracy vs ground
  truth + performance; results in `RESULTS.md`.
- 15 tests (incl. verification gates); GitHub Actions CI across Python 3.9–3.13.
