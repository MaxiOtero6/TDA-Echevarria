def greedy(arr: list[int]):
    intervalos = []
    subintervalo = []
    suma = 0

    for i, numero in enumerate(arr):
        suma += numero
        if suma > 0 or (i < len(arr) - 1 and (suma + arr[i+1]) > 0):
            subintervalo.append(numero)
        else:
            suma = 0
            if subintervalo and len(subintervalo) > 1:
                intervalos.append(subintervalo)
            subintervalo = []
    if subintervalo and len(subintervalo) > 1:
                intervalos.append(subintervalo)
    return len(intervalos)
