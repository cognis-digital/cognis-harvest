"""Terravue — AI/ML multi-modal illicit-crop detection & yield estimation.

A self-hostable pipeline that turns multispectral (and SAR-fallback) pixel data
into crop classifications, cultivation-area estimates with confidence intervals,
and multi-source yield/market-value estimates, exportable as GeoJSON.

HONEST SCOPE: the analytics are real and measurable, but this is an
early-prototype that operates on supplied or synthetic spectral data — it is not
a fielded satellite pipeline, and synthetic separability overstates real-world
crop-spectra overlap. See docs/LIMITATIONS.md.

(c) 2026 Cognis Digital LLC (Wyoming, USA). Source-available under COCL-1.0.
"""

__version__ = "0.2.0"
__all__ = ["spectral", "classify", "detect", "area", "yield_model", "trends",
           "change", "geojson", "report", "synth"]
