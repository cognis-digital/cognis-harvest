"""End-to-end example. Run from repo root:  python examples/run_demo.py"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cognis_harvest import synth  # noqa: E402
from cognis_harvest.area import estimate_area  # noqa: E402
from cognis_harvest.classify import NearestCentroid  # noqa: E402
from cognis_harvest.detect import classify_scene  # noqa: E402
from cognis_harvest.report import render_text  # noqa: E402
from cognis_harvest.yield_model import estimate_yield  # noqa: E402

clf = NearestCentroid(synth.BANDS).fit(synth.generate_training())
scene, _ = synth.generate_scene(profile="clean")
classified = classify_scene(scene, clf)
area = estimate_area(classified["counts"], scene["pixel_area_ha"], accuracy=0.95)
coeffs = {"climate_factor": 1.0, "soil_factor": 1.0,
          "crops": {"coca": {"yield_kg_per_ha": 1200, "price_per_kg": 1.5},
                    "poppy": {"yield_kg_per_ha": 20, "price_per_kg": 200},
                    "cannabis": {"yield_kg_per_ha": 1000, "price_per_kg": 2.0}}}
product = {"scene_id": scene["id"], "total_pixels": len(scene["pixels"]),
           "cloud_pixels": 0, "class_counts": classified["counts"],
           "area": area, "yield": estimate_yield(area, coeffs)}
print(render_text(product))
