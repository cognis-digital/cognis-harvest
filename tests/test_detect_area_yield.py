from collections import Counter

from terravue import synth
from terravue.area import estimate_area
from terravue.classify import NearestCentroid
from terravue.detect import CROP_CLASSES, classify_scene
from terravue.yield_model import estimate_yield


def _clf():
    return NearestCentroid(synth.BANDS).fit(synth.generate_training())


def test_classify_scene_counts_crops():
    scene, truth = synth.generate_scene(profile="clean", width=32, height=32)
    counts = classify_scene(scene, _clf())["counts"]
    true_counts = Counter(truth.values())
    # predicted coca pixel count within 15% of truth
    assert abs(counts.get("coca", 0) - true_counts["coca"]) <= 0.15 * true_counts["coca"]


def test_area_has_confidence_interval():
    scene, _ = synth.generate_scene(profile="clean", width=24, height=24)
    counts = classify_scene(scene, _clf())["counts"]
    area = estimate_area(counts, scene["pixel_area_ha"], accuracy=0.9)
    for c in CROP_CLASSES:
        ci = area[c]["ci95_ha"]
        assert ci[0] <= area[c]["area_ha"] <= ci[1]


def test_yield_scales_with_area():
    coeffs = {"climate_factor": 1.0, "soil_factor": 1.0,
              "crops": {"coca": {"yield_kg_per_ha": 1000, "price_per_kg": 2.0}}}
    small = estimate_yield({"coca": {"area_ha": 1.0}}, coeffs)
    big = estimate_yield({"coca": {"area_ha": 10.0}}, coeffs)
    assert big["coca"]["production_kg"] == 10 * small["coca"]["production_kg"]
    assert big["coca"]["market_value_usd"] == 10 * small["coca"]["market_value_usd"]
