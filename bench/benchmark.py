"""Performance benchmark: pixel classification throughput at increasing scene
sizes."""

from __future__ import annotations

import json
import time

from terravue import synth
from terravue.classify import NearestCentroid
from terravue.detect import classify_scene


def benchmark(sizes=(48, 96, 160)) -> list:
    clf = NearestCentroid(synth.BANDS).fit(synth.generate_training())
    rows = []
    for w in sizes:
        scene, _ = synth.generate_scene(profile="clean", width=w, height=w)
        n = len(scene["pixels"])
        t0 = time.perf_counter()
        classify_scene(scene, clf)
        dt = time.perf_counter() - t0
        rows.append({"scene": f"{w}x{w}", "pixels": n, "classify_s": round(dt, 4),
                     "pixels_per_s": int(n / dt) if dt > 0 else None})
    return rows


def main():
    print(json.dumps(benchmark(), indent=2))


if __name__ == "__main__":
    main()
