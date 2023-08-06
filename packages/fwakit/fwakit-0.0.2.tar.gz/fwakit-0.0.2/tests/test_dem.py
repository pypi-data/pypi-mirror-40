import fwakit as fwa
import os


def test_extract_dem():
    bounds = [1046891.13884, 704778.39518, 1055345.57091, 709629.69983]
    out_file = fwa.extract_dem(bounds)
    assert os.path.exists(out_file)

