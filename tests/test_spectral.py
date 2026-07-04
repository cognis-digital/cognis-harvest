from terravue import spectral


def test_ndvi_vegetation_high():
    veg = {"nir": 0.45, "red": 0.05, "green": 0.05, "swir1": 0.2}
    soil = {"nir": 0.25, "red": 0.20, "green": 0.15, "swir1": 0.3}
    assert spectral.ndvi(veg) > spectral.ndvi(soil)


def test_indices_keys():
    v = {"blue": .04, "green": .07, "red": .06, "nir": .38, "swir1": .22}
    idx = spectral.indices(v)
    assert set(idx) == {"ndvi", "savi", "ndwi", "nbr"}


def test_ndvi_zero_safe():
    assert spectral.ndvi({"nir": 0.0, "red": 0.0}) == 0.0
