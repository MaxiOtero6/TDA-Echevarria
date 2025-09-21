import pytest
from .algo import backtracking

test_cases = []


@pytest.mark.parametrize("arr, expected", test_cases)
def test_backtracking(arr, expected):
    assert backtracking(arr) == expected
