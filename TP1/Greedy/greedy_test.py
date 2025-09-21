import pytest
from .algo import greedy

test_cases = [([3, -5, 7, -4, 1, -8, 3, -7, 5, -9, 5, -2, 4], 3)]


@pytest.mark.parametrize("arr, expected", test_cases)
def test_greedy(arr, expected):
    assert greedy(arr) == expected
