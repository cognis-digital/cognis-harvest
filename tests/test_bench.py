"""Gate the verification claims in RESULTS.md."""

from bench import evaluate


def test_clean_classification_strong():
    r = evaluate.evaluate()
    assert r["classification_clean"]["overall_accuracy"] >= 0.97
    for c in ("coca", "poppy", "cannabis"):
        assert r["classification_clean"]["per_class"][c]["f1"] >= 0.9


def test_area_mape_low_on_clean():
    assert evaluate.evaluate()["area_mape_clean"] <= 0.1


def test_cloud_degrades_below_clear():
    r = evaluate.evaluate()
    # honest degradation: SAR-only cloud pixels classify worse than clear pixels
    assert r["accuracy_cloud_pixels"] < r["accuracy_clear_pixels"]


def test_change_detection_recall():
    r = evaluate.evaluate()
    assert r["change_detection"]["recall"] >= 0.9


def test_determinism():
    assert evaluate.evaluate()["determinism"] is True
