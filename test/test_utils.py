import pytest
from utils import maxvalue, meannvalue

def test_maxvalue():
    assert type(maxvalue([4,5,1])) == int

    assert maxvalue([3,7,8,13,1,0,2]) == 3
    with pytest.raises(ValueError):
        maxvalue([1,4,0,'hi', 2])

def test_meanvalue():
    assert type(meannvalue([90,7,5,1])) == float

    assert meannvalue([3,7,8]) == float(6)
    with pytest.raises(ValueError):
        meannvalue([1,4,0,'hi', 2])