from collections import Counter

from bench.metrics import confusion_matrix, macro_f1
from terravue import synth
from terravue.classify import NearestCentroid
from terravue.detect import classify_scene
from terravue.trends import area_series, expansion_alerts, growth


def _counts():
    clf = NearestCentroid(synth.BANDS).fit(synth.generate_training())
    scenes = synth.growth_series(steps=4)
    return [Counter(classify_scene(s, clf)["counts"]) for s in scenes], scenes[0]["pixel_area_ha"]


def test_area_series_increases_for_expanding_crop():
    counts, pa = _counts()
    series = area_series(counts, pa)
    coca = series["coca"]
    assert coca[-1] > coca[0]  # expanding patch -> growing area


def test_growth_rate_positive_and_alert():
    counts, pa = _counts()
    series = area_series(counts, pa)
    g = growth(series)
    assert g["coca"]["rate_ha_per_step"] > 0
    assert g["coca"]["change_pct"] > 0
    alerts = expansion_alerts(series, min_change_pct=20.0)
    assert any(a["crop"] == "coca" for a in alerts)


def test_confusion_matrix_and_macro_f1():
    clf = NearestCentroid(synth.BANDS).fit(synth.generate_training())
    scene, truth = synth.generate_scene(profile="clean", width=24, height=24)
    pred = {(p["row"], p["col"]): p["label"] for p in classify_scene(scene, clf)["pixels"]}
    classes = list(synth.CENTROIDS.keys())
    cm = confusion_matrix(pred, truth, classes)
    # diagonal dominates on clean data
    assert cm["coca"]["coca"] >= sum(cm["coca"][o] for o in classes if o != "coca")
    assert macro_f1(pred, truth, classes) >= 0.9
