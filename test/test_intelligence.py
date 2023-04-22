import pytest
import numpy 
from intelligence import find_red_pixels, find_cyan_pixels, detect_connected_components

def test_find_red_pixels():
    assert type(find_red_pixels('data/map.png')) == numpy.ndarray


def test_find_cyan_pixels():
    assert type(find_cyan_pixels('data/map.png')) == numpy.ndarray


def test_connected_components():
    assert type(detect_connected_components(find_cyan_pixels('data/map.png'))) == numpy.ndarray