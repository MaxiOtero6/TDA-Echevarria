import pytest
from .algo import max_subarray_backtracking as backtracking

test_cases = [
  ([2, -4, 3, -1, 2], (4, [3, -1, 2])), 
  ([-3, -1, -7], (-1, [-1])), 
  ([1, 2, 3, 4], (10, [1, 2, 3, 4])), 
  ([0, -1, 3, -2, 0, 4], (5, [3, -2, 0, 4])), 
  ([-2, 1, -3, 4, -1, 2, 1, -5, 4], (6, [4, -1, 2, 1])),
  ([5, -2, 5], (8, [5, -2, 5])),
  ([0], (0, [0])),
  ([0, 0, 0], (0, [0])),
  ([-10, 2, 3], (5, [2, 3])),
  ([1, -1, 1], (1, [1])),
]

@pytest.mark.parametrize("arr, expected", test_cases)
def test_backtracking(arr, expected):
    assert backtracking(arr) == expected
