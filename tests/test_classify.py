from cognis_harvest import synth
from cognis_harvest.classify import NearestCentroid


def _clf():
    return NearestCentroid(synth.BANDS).fit(synth.generate_training())


def test_centroids_learned_for_all_classes():
    clf = _clf()
    assert set(clf.centroids) == set(synth.CENTROIDS)


def test_predict_recovers_class():
    clf = _clf()
    coca = synth.CENTROIDS["coca"]
    assert clf.predict(coca)["label"] == "coca"
    assert 0.0 <= clf.predict(coca)["confidence"] <= 1.0


def test_sar_only_fallback_runs():
    clf = _clf()
    pred = clf.predict(synth.CENTROIDS["forest"], available=["sar"])
    assert pred["label"] in synth.CENTROIDS
