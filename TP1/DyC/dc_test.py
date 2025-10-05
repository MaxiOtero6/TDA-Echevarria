import pytest
import random
from .algo import dc, f_bruta

base_cases: list[tuple[list[int], int]] = [
    ([-1, 2, 3, 4, 5], -1),
    ([0, 2, 3, 4, 5], 0),
    ([-2, -1, 0, 3, 5], 3),
    ([1, 2, 3, 4, 5], -1),
    ([-1, 0, 2, 3, 4], 2),
    ([-3, -2, -1, 1, 4], 4),
    ([2, 3, 4, 5, 6], -1),
    ([-5, -4, -3, -2, -1], -1),
    ([-2, -1, 2, 3, 4], 2),
    ([-1, 1, 3, 4, 5], 1),
    ([0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16], 0),
    ([-1, 0, 1, 2, 3, 4, 5, 7, 9, 10, 11, 12, 13, 14, 15, 16], 7),
    ([-2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 14], 14),
    ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16], -1),
    ([], -1),
    ([2], -1),
    ([0], 0),
    ([-1, 1], 1),
    ([-1, 0, 2], 2),
]

random.seed(777)  # Seed for reproducibility


def generate_test_cases(skip_base_cases=False, min=10000, max=20000, sample_size=50):
    if not skip_base_cases:
        for _, case in enumerate(base_cases):
            yield case

    for _ in range(sample_size):
        n = random.randint(min, max)
        arr = list({random.randint(-n, n) for _ in range(n)})
        print(f"Generated array of size {n}")
        arr.sort()
        print(f"Sorted array of size {n}")

        expected = f_bruta(arr)
        if expected == -1:
            print("Yield")
            yield (arr, expected)
        else:
            # Ensure algorithm result is unique
            _expected = expected
            index_to_remove = []
            while _expected != -1:
                index_to_remove.insert(0, _expected)
                arr[_expected] = -1
                _expected = f_bruta(arr)

            for idx in index_to_remove:
                arr.pop(idx)

            arr.insert(expected, expected)
            print("Size after ensuring the result is unique:", len(arr))
            print("Yield")
            yield (arr, expected)


cases = generate_test_cases()


@pytest.mark.parametrize("arr, expected", cases)
def test_dc(arr, expected):
    res = dc(arr)

    assert res == expected
    assert res == f_bruta(arr)
