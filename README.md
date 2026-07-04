<h1 align="center">🟣 Terravue</h1>
<p align="center"><b>AI/ML multi-modal illicit-crop detection &amp; yield estimation</b><br>
<i>Multispectral + SAR → crop classification, cultivation area with confidence intervals, and yield/market estimates — self-hosted, offline.</i></p>

<p align="center">
<img alt="license" src="https://img.shields.io/badge/license-COCL--1.0-6D28D9">
<img alt="python" src="https://img.shields.io/badge/python-3.9%2B-6D28D9">
<img alt="deps" src="https://img.shields.io/badge/dependencies-none%20(stdlib)-6D28D9">
<img alt="status" src="https://img.shields.io/badge/status-v0.1.0%20(prototype)-6D28D9">
</p>

---

> **Built for:** SOLIC Accelerator / ONIX OTA — **Challenge Area 4: Illicit Drug Crop Estimation.**
> Detect and map coca / opium poppy / cannabis cultivation from commercial multispectral imagery, estimate area with defensible confidence intervals, model yield & market value, and hold estimation through cloud cover via SAR fallback — at a fraction of legacy cost.

> ⚠️ **Honest maturity:** this is an **early prototype**. The analytics are real and measured, but they run on **supplied or synthetic** spectral data — not a fielded satellite pipeline. Synthetic separability overstates real crop-spectra overlap; treat metrics as pipeline-correctness, not operational accuracy. See [`docs/LIMITATIONS.md`](docs/LIMITATIONS.md).

## What it does

- 🌱 **Spectral analysis** — NDVI/SAVI/NDWI/NBR indices from multispectral bands.
- 🛰️ **Classification** — nearest-centroid crop classifier over multispectral signatures, with **SAR-only fallback** on cloud-obscured pixels (multi-phenomenology).
- 📐 **Area estimation** — cultivation hectares per crop with **95% confidence intervals** derived from classifier accuracy.
- 🌾 **Yield & value** — multi-source model (area × yield/ha × climate × soil × price); coefficients illustrative.
- 🔁 **Change detection** — new/removed cultivation between two scenes.
- 🗺️ **GeoJSON export** — detected parcels as geolocated features.
- 🔒 **Offline / zero-dependency** — pure Python stdlib.

## Quick start

```bash
git clone https://github.com/cognis-digital/terravue
cd terravue
python -m terravue demo --profile clean --geojson crops.geojson
python -m terravue demo --profile cloudy      # SAR-fallback degradation
```

```bash
terravue estimate --scene data/sample_scene.json --training data/training_samples.json
terravue change --scene1 t1.json --scene2 t2.json --training data/training_samples.json
```

## Verification & proof

Measured against **planted ground truth**, gated in CI. Reproduce with
`python bench/run_all.py` → [`RESULTS.md`](RESULTS.md).

| Metric | Value |
|---|---|
| Classification overall accuracy (clean) | **0.998** |
| Per-crop F1 (coca/poppy/cannabis) | 0.97 / 1.00 / 0.97 |
| Area estimation MAPE (clean) | **0.000** |
| Change detection (new cultivation) P/R/F1 | **1.00** |
| Cloud (SAR-only) vs clear accuracy | 0.97 vs 1.00 (honest degradation) |
| GeoJSON determinism | ✓ identical across runs |

Throughput: **~86,000 pixels/sec** single-thread (stdlib).

## License

Source-available under **COCL v1.0** (see [LICENSE](LICENSE)). Commercial use:
`licensing@cognis.digital`.

<p align="center"><sub>© 2026 Cognis Digital LLC · <a href="https://cognis.digital">cognis.digital</a></sub></p>
