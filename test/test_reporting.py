import pytest
from reporting import data_implementation, daily_average, monthly_average


def test_data_implementation():
    assert type(data_implementation()) == dict


def test_monthly_average():
    assert round(monthly_average(None, 'Kensington', 'pm25')[0],2) == 8.72

    with pytest.raises(AssertionError):
        assert round(monthly_average(None, 'Marylebone', 'pm10')[-1],2) == 10.37


def test_daily_average():
    assert len(daily_average(None, 'Harlington', 'pm10')) == 365