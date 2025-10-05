import pytest
from .dinamica import dinamica

test_cases = [
    ([-2, 1, -3, 4, -1, 2, 1, -5, 4], (6, 3, 6)),
    ([1, 2, 3, 4, 5], (15, 0, 4)),
    ([-1, -2, -3, -4], (-1, 0, 0)),
    ([0, 0, 0, 0], (0, 0, 0)),
    ([3, -2, 5, -1], (6, 0, 2)),
]


@pytest.mark.parametrize("arr, expected", test_cases)
def test_dinamica(arr, expected):
    assert dinamica(arr) == expected
