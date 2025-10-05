from typing import Literal


# O(N)
def f_bruta(arr: list[int]) -> int | Literal[-1]:
    n = len(arr)

    for i in range(n):
        if arr[i] == i:
            return i

    return -1


# O(log(N))


def dc(arr: list[int], mock_sum=False) -> int | Literal[-1]:
    """
    El parametro mock_sum es para simular una carga de trabajo mayor en cada llamada recursiva.
    Esto se agrego debido a que la funcion original es muy rapida y para tamaños de entrada grandes,
    el tiempo de ejecucion es muy bajo, lo que dificulta la medicion precisa del tiempo de ejecucion,
    resultando en que la mayoria del tiempo que se mide es el overhead de la llamada a la funcion y no
    el tiempo real de procesamiento del algoritmo.

    Se consulto con Pablo Echevarria y se decidio agregar esta carga de trabajo simulada para obtener
    mediciones de tiempo mas precisas y representativas del comportamiento del algoritmo en si.
    """

    def run(arr: list[int], left: int, right: int) -> int | Literal[-1]:
        if left >= right:
            return -1

        mid_idx: int = (left + right) // 2

        if mock_sum:
            sum = 0
            for _ in range(50_000_000):
                sum += 1

        if arr[mid_idx] < mid_idx:
            return run(arr, mid_idx + 1, right)

        if arr[mid_idx] > mid_idx:
            return run(arr, left, mid_idx)

        return mid_idx

    return run(arr, 0, len(arr))
