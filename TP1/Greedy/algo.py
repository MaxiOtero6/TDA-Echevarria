def turns_positive(arr: list[int], i: int, suma: int) -> bool:
    for j in range(i + 1, len(arr)):
        suma += arr[j]
        if suma > 0:
            return True
    return False

def greedy(arr: list[int]):
    intervalos = 0
    subintervalo = []
    suma = 0

    for i, numero in enumerate(arr):
        suma += numero
        if suma > 0:
            subintervalo.append(numero)
        elif (numero > 0 and not subintervalo):
            subintervalo.append(numero)
            suma = numero

        if not turns_positive(arr, i, suma):
            suma = 0
            if subintervalo and len(subintervalo) > 1:
                intervalos += 1
            subintervalo = []
    if subintervalo and len(subintervalo) > 1:
        intervalos += 1
    return intervalos
