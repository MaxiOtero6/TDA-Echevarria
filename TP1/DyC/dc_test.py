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

random.seed(749)


def generate_test_cases(skip_base_cases=False, min=10000, max=20000, sample_size=50):
    if not skip_base_cases:
        for _, case in enumerate(base_cases):
            yield case

    for _ in range(sample_size):
        n = random.randint(min, max)
        arr = list(
            {random.randint(-n, n) for _ in range(n)}
        )
        print(f'Generated array of size {n}')
        arr.sort()
        print(f'Sorted array of size {n}')

        expected = f_bruta(arr)
        if expected == -1:
            print('Yield')
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
            print('Yield')
            yield (arr, expected)


# def save_gen_in_file():
#     with open('plot_cases.json', 'w') as f:
#         import json
#         json.dump(
#             [case for case, _ in generate_test_cases(skip_base_cases=True, min=100_000_000, max=100_000_000, sample_size=1)], f)


# def load_gen_from_file():
#     with open('plot_cases.json', 'r') as f:
#         import json
#         arrs = json.load(f)
#         for arr in arrs:
#             yield arr


cases = generate_test_cases()
# test_cases.sort(key=lambda x: len(x[0]))
# save_gen_in_file()


@pytest.mark.parametrize("arr, expected", cases)
def test_dc(arr, expected):
    res = dc(arr)

    assert res == expected
    assert res == f_bruta(arr)
