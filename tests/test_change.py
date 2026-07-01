from cognis_harvest import synth
from cognis_harvest.change import detect_change
from cognis_harvest.classify import NearestCentroid


def test_detects_new_cultivation():
    clf = NearestCentroid(synth.BANDS).fit(synth.generate_training())
    s1, _ = synth.generate_scene(seed=11, profile="clean", width=32, height=32,
                                 patches=[("coca", 4, 4, 10, 10)])
    s2, _ = synth.generate_scene(seed=11, profile="clean", width=32, height=32)
    ch = detect_change(s1, s2, clf)
    # poppy + cannabis patches (2 x 6x6 = 72 px) should appear as new cultivation
    assert len(ch["new_cultivation"]) >= 60
    assert len(ch["removed_cultivation"]) <= 5
