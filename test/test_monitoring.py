import pytest
from monitoring import find_station_code, peak_workday

def test_find_station_code():
    assert find_station_code('Harlington') == 'LH0'


def test_peak_workday():
    assert type(peak_workday()) == dict