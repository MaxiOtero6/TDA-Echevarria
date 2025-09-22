import pytest
from .algo import greedy

test_cases = [([3, -5, 7, -4, 1, -8, 3, -7, 5, -9, 5, -2, 4], 3)]
test_cases += [([1, -1, 1, -1, 1, 1], 1)]
test_cases += [([-1, -2, -3, -4], 0)]
test_cases += [([5, 6, -2, -1, 4, -3, 2], 1)]
test_cases += [([0, 0, 0, 0], 0)]
test_cases += [([10, -5, 3, -2, 1, -1, 4, -6, 2], 1)]
test_cases += [([1, 2, 3, -6, 4, 5, -10, 6], 1)]
test_cases += [([-2, -3, 4, -1, -2, 1, 5, -3], 2)]


@pytest.mark.parametrize("arr, expected", test_cases)
def test_greedy(arr, expected):
    assert greedy(arr) == expected
