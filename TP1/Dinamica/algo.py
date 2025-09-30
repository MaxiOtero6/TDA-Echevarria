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


if __name__ == "__main__":
    arr = [-2,1,-3,4,-1,2,1,-5,4]
    (suma_maxima, inicio, fin) = dinamica(arr)
    print(f"Suma máxima: {suma_maxima}, Secuencia: {arr[inicio:fin+1]}")
