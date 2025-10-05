import pytest
from .dinamica import dinamica

test_cases = []


@pytest.mark.parametrize("arr, expected", test_cases)
def test_dinamica(arr, expected):
    assert dinamica(arr) == expected
