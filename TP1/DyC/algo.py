from typing import Literal


# O(N)
def f_bruta(arr: list[int]) -> int | Literal[-1]:
    n = len(arr)

    for i in range(n):
        if arr[i] == i:
            return i

    return -1


# O(log(N))
def dc(arr: list[int]) -> int | Literal[-1]:
    def run(arr: list[int], left: int, right: int) -> int | Literal[-1]:
        if left >= right:
            return -1

        mid_idx: int = (left + right) // 2

        if arr[mid_idx] < mid_idx:
            return run(arr, mid_idx + 1, right)

        if arr[mid_idx] > mid_idx:
            return run(arr, left, mid_idx)

        return mid_idx

    return run(arr, 0, len(arr))
