"""Next Fit (Bin Packing) core
- next_fit(objetos, capacidad): online heuristic (2-approx).
- calcular_metricas(recipientes): usage, waste, efficiency.
- cota_inferior_teorica(objetos): ceil(sum/capacity).
- generar_casos_prueba(seed): fixed small scenarios.
- generar_dataset(n, rng): random instance for benchmarking.
"""
import random

"""Heurística Next Fit (online) para Bin Packing"""
def next_fit(objetos, capacidad=1.0):
    if not objetos:
        return []

    recipientes = []
    recipiente_actual = []
    espacio_libre = capacidad

    for objeto in objetos:
        if objeto <= espacio_libre:
            recipiente_actual.append(objeto)
            espacio_libre -= objeto
        else:
            recipientes.append(recipiente_actual)
            recipiente_actual = [objeto]
            espacio_libre = capacidad - objeto

    if recipiente_actual:
        recipientes.append(recipiente_actual)

    return recipientes

"""Calcula métricas de la solución obtenida"""
def calcular_metricas(recipientes, capacidad=1.0):
    if not recipientes:
        return {"num_recipientes": 0, "utilización_promedio": 0, "desperdicio_total": 0}
    
    utilizaciones = [sum(recipiente) for recipiente in recipientes]
    desperdicio_total = len(recipientes) * capacidad - sum(utilizaciones)

    return {
        "num_recipientes": len(recipientes),
        "utilización_promedio": sum(utilizaciones) / len(recipientes),
        "desperdicio_total": desperdicio_total,
        "eficiencia": sum(utilizaciones) / (len(recipientes) * capacidad)
    }

"""Calcula la cota inferior teórica (suma total / capacidad)"""
def cota_inferior_teorica(objetos, capacidad=1.0):
    import math
    suma_total = sum(objetos)
    return math.ceil(suma_total / capacidad)

"""Genera diferentes tipos de datasets para pruebas"""
def generar_casos_prueba(seed=None):
    rng = random.Random(seed) if seed is not None else random
    casos = {
        "basico": [0.6, 0.3, 0.7, 0.2, 0.1],
        "items_grandes": [0.9, 0.8, 0.95, 0.85, 0.7],
        "items_pequenos": [0.1, 0.2, 0.15, 0.05, 0.3],
        "peor_caso": [0.51, 0.51, 0.51, 0.51, 0.51], # Cada item necesita un recipiente nuevo
        "mixto": [0.4, 0.6, 0.2, 0.8, 0.1, 0.9, 0.3, 0.7],
        "aleatorio": [round(rng.uniform(0.01, 0.99), 2) for _ in range(20)]
    }

    return casos

"""Genera datasets separados (sin medir)"""
def generar_dataset(n, rng=None):
    r = rng if rng is not None else random
    return [round(r.uniform(0.1, 0.9), 2) for _ in range(n)]