"""Run accuracy + performance and write bench/results.json and RESULTS.md."""

from __future__ import annotations

import json
import os
import platform
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bench import benchmark, evaluate  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def build_results():
    return {
        "accuracy": evaluate.evaluate(),
        "performance": benchmark.benchmark(),
        "environment": {
            "python": platform.python_version(),
            "implementation": platform.python_implementation(),
            "system": platform.system(),
            "machine": platform.machine(),
        },
    }


def render_md(res) -> str:
    a = res["accuracy"]
    cc = a["classification_clean"]
    ch = a["change_detection"]
    env = res["environment"]
    L = []
    L.append("# Terravue — Verification Results\n")
    L.append("Reproduce with: `python bench/run_all.py` (regenerates this file).\n")
    L.append(f"Environment: {env['implementation']} {env['python']} on "
             f"{env['system']}/{env['machine']}. Deterministic synthetic data.\n")
    L.append("> **Honest note:** metrics are on synthetic multispectral scenes with planted "
             "ground truth. Real crop spectra overlap far more; these numbers measure pipeline "
             "correctness, not fielded accuracy. The cloudy profile shows genuine degradation "
             "when optical bands are obscured and only SAR is available.\n")
    L.append("## Accuracy vs. planted ground truth\n")
    L.append("| Metric | Value |")
    L.append("|---|---|")
    L.append(f"| Classification overall accuracy (clean) | {cc['overall_accuracy']:.3f} |")
    for c in ("coca", "poppy", "cannabis"):
        m = cc["per_class"][c]
        L.append(f"| — {c} P/R/F1 | {m['precision']:.3f} / {m['recall']:.3f} / {m['f1']:.3f} |")
    L.append(f"| Area estimation MAPE (clean, crops) | {a['area_mape_clean']:.3f} |")
    L.append(f"| Accuracy on clear pixels (cloudy scene) | {a['accuracy_clear_pixels']:.3f} |")
    L.append(f"| Accuracy on cloud pixels (SAR-only fallback) | {a['accuracy_cloud_pixels']:.3f} |")
    L.append(f"| Change detection (new cultivation) P/R/F1 | "
             f"{ch['precision']:.3f} / {ch['recall']:.3f} / {ch['f1']:.3f} |")
    L.append(f"| GeoJSON determinism (2 runs identical) | {a['determinism']} |")
    L.append("")
    L.append("## Performance (single-thread, stdlib only)\n")
    L.append("| Scene | Pixels | Classify (s) | Pixels/s |")
    L.append("|---:|---:|---:|---:|")
    for r in res["performance"]:
        L.append(f"| {r['scene']} | {r['pixels']:,} | {r['classify_s']} | {r['pixels_per_s']:,} |")
    L.append("")
    L.append("Gated in CI by `tests/test_bench.py`. See `docs/LIMITATIONS.md`.\n")
    return "\n".join(L)


def main():
    res = build_results()
    with open(os.path.join(HERE, "results.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2)
    with open(os.path.join(ROOT, "RESULTS.md"), "w", encoding="utf-8") as f:
        f.write(render_md(res))
    print("[+] wrote bench/results.json and RESULTS.md")
    print(render_md(res))


if __name__ == "__main__":
    main()
