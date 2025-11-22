from typing import Any

class Grafo:
    def __init__(self, adyacencia = None):
        self.adyacencia: dict[Any, dict[Any, int]] = adyacencia if adyacencia else {}
        self.aristas: dict[tuple[Any, Any], int] = {}

    def agregar_vertice(self, v: Any):
        if v not in self.adyacencia:
            self.adyacencia[v] = {}

    def agregar_arista(self, v1: Any, v2: Any, peso: int):
        self.agregar_vertice(v1)
        self.agregar_vertice(v2)
        self.adyacencia[v1][v2] = peso
        self.aristas[(v1, v2)] = peso

    def obtener_adyacentes(self, v: Any):
        return self.adyacencia.get(v, {})
    
    def obtener_aristas(self):
        return list(self.aristas.keys())

    def __str__(self):
        return str(self.adyacencia)

