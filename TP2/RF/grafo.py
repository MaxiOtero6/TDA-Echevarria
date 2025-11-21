from typing import Any


class Grafo:
    def __init__(self, adyacencia = None):
        self.adyacencia: dict[Any, dict[Any, int]] = adyacencia if adyacencia else {}

    def agregar_vertice(self, v: Any):
        if v not in self.adyacencia:
            self.adyacencia[v] = {}

    def agregar_arista(self, v1: Any, v2: Any, peso: int):
        self.agregar_vertice(v1)
        self.agregar_vertice(v2)
        self.adyacencia[v1][v2] = peso
        self.adyacencia[v2][v1] = peso  # Si es dirigido, eliminar esta línea

    def obtener_adyacentes(self, v: Any):
        return self.adyacencia.get(v, {})

    def __str__(self):
        return str(self.adyacencia)

# # Ejemplo de uso:
# g = Grafo()
# g.agregar_arista('A', 'B', 5)
# g.agregar_arista('A', 'C', 2)
