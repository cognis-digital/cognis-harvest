# Limitations & Responsible Use

**Cognis Harvest is an early prototype.** Read this before drawing conclusions.

## Scope & honesty
- **Synthetic separability ≠ real accuracy.** Bundled data and benchmarks use
  synthetic spectra drawn from fixed centroids with light noise. Real coca/poppy/
  cannabis spectra overlap heavily with each other and with background vegetation;
  operational accuracy will be materially lower and must be validated against
  region-specific ground truth.
- **No real imagery ingestion yet.** The pipeline consumes pre-formatted spectral
  pixel data. Adapters for commercial satellite/airborne products (and true SAR
  backscatter) are post-prototype work.
- **Illustrative coefficients.** Yield and price figures are placeholders, not
  authoritative agronomic or market data. Do not cite production/value outputs
  operationally without calibrated inputs.
- **Cloud handling is a fallback, not a fix.** SAR-only classification cannot
  separate crop species as well as optical; the benchmarks show this degradation
  explicitly.

## Responsible use
Use only within your lawful authority and with data you are authorized to
process. Outputs are estimates with stated uncertainty, intended to inform
analysis and resourcing — not to be treated as ground truth. You are solely
responsible for your use (LICENSE §9, NOTICE).
