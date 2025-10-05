def dinamica(arr: list[int]):
    n = len(arr)
    if n == 0:
        return (0, -1, -1)

    suma_maxima, suma_actual = arr[0], arr[0]
    inicio, fin, temp_inicio = 0, 0, 0

    for i in range(1, n):
        if suma_actual + arr[i] > arr[i]:
            suma_actual += arr[i]
        else:
            suma_actual = arr[i]
            temp_inicio = i

        if suma_actual > suma_maxima:
            suma_maxima = suma_actual
            inicio = temp_inicio
            fin = i

    return (suma_maxima, inicio, fin)


def main():
    datasets = [[2, -4, 3, -1, 2], [-3, -1, -7], [1, 2, 3, 4], [0, -1, 3, -2, 0, 4]]

    for i, arr in enumerate(datasets, start=1):
        suma_max, inicio, fin = dinamica(arr)
        subseq = arr[inicio : fin + 1] if inicio != -1 else []
        print(f"== Set {i} ==")
        print(f"Input: {arr}")
        print(f"Mejor suma: {suma_max}")
        print(f"Subsecuencia optima: {subseq}\n")


if __name__ == "__main__":
    main()
