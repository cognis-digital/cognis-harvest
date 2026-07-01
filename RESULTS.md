# Cognis Harvest — Verification Results

Reproduce with: `python bench/run_all.py` (regenerates this file).

Environment: CPython 3.14.0 on Windows/AMD64. Deterministic synthetic data.

> **Honest note:** metrics are on synthetic multispectral scenes with planted ground truth. Real crop spectra overlap far more; these numbers measure pipeline correctness, not fielded accuracy. The cloudy profile shows genuine degradation when optical bands are obscured and only SAR is available.

## Accuracy vs. planted ground truth

| Metric | Value |
|---|---|
| Classification overall accuracy (clean) | 0.998 |
| — coca P/R/F1 | 0.972 / 0.972 / 0.972 |
| — poppy P/R/F1 | 1.000 / 1.000 / 1.000 |
| — cannabis P/R/F1 | 0.972 / 0.972 / 0.972 |
| Area estimation MAPE (clean, crops) | 0.000 |
| Accuracy on clear pixels (cloudy scene) | 1.000 |
| Accuracy on cloud pixels (SAR-only fallback) | 0.971 |
| Change detection (new cultivation) P/R/F1 | 1.000 / 1.000 / 1.000 |
| GeoJSON determinism (2 runs identical) | True |

## Performance (single-thread, stdlib only)

| Scene | Pixels | Classify (s) | Pixels/s |
|---:|---:|---:|---:|
| 48x48 | 2,304 | 0.0268 | 86,120 |
| 96x96 | 9,216 | 0.1053 | 87,510 |
| 160x160 | 25,600 | 0.2992 | 85,569 |

Gated in CI by `tests/test_bench.py`. See `docs/LIMITATIONS.md`.
