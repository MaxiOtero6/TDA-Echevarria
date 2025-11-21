from pathlib import Path
from .grafo import Grafo
from collections import deque
from typing import Hashable


def bfs(grafo: Grafo, fuente: Hashable, sumidero: Hashable, parent: dict[Hashable, Hashable]) -> bool:
    visited = set()
    queue = deque([fuente])
    visited.add(fuente)
    parent.clear()

    while queue:
        u = queue.popleft()

        adyacentes = grafo.obtener_adyacentes(u)

        for v, capacidad in adyacentes.items():
            if v not in visited and capacidad > 0:
                visited.add(v)
                parent[v] = u
                queue.append(v)
                if v == sumidero:
                    return True
    return False


def edmondsKarp(grafo: Grafo, fuente: Hashable, sumidero: Hashable, caminos: list[tuple[list[Hashable], int]]) -> int:
    flujo_maximo: int = 0
    camino_encontrado: dict[Hashable, Hashable] = {}

    # Mientras exista un camino desde la fuente al sumidero
    # BFS actualiza camino_encontrado
    while bfs(grafo, fuente, sumidero, camino_encontrado):

        # 1. Buscamos el cuello de botella (flujo mínimo) en el camino hallado
        flujo_camino = float('inf')
        v = sumidero

        path: list[Hashable] = []  # Para reconstruir el camino

        while v != fuente:
            path.append(v)
            u = camino_encontrado[v]  # u es el nodo anterior a v en el camino
            flujo_camino = min(flujo_camino, grafo.adyacencia[u][v])
            v = u
        path.append(fuente)
        path.reverse()

        flujo_camino = int(flujo_camino)

        # 2. Guardamos el camino utilizado junto con su flujo máximo
        caminos.append((path, flujo_camino))

        # 3. Actualizamos las capacidades residuales del grafo
        v = sumidero
        while v != fuente:
            u = camino_encontrado[v]

            # Restar flujo en la arista original
            grafo.adyacencia[u][v] = grafo.adyacencia[u][v] - flujo_camino

            # Sumar flujo en la arista residual
            if v not in grafo.adyacencia:
                grafo.agregar_vertice(v)
            if u not in grafo.adyacencia[v]:
                grafo.adyacencia[v][u] = 0

            grafo.adyacencia[v][u] = grafo.adyacencia[v][u] + flujo_camino

            v = u

        # 4. Actualizamos el flujo total
        flujo_maximo = flujo_maximo + flujo_camino

    return flujo_maximo


def algoritmo(grafo: Grafo, fuente: Hashable, sumidero: Hashable, flujo_esperado: int) -> None:
    caminos = []
    flujo_maximo = edmondsKarp(grafo, fuente, sumidero, caminos)

    if flujo_maximo < flujo_esperado:
        print("No se puede fragmentar el paquete en la red de la facultad")
        return

    results_file_path = Path(__file__).parent / "resultados.txt"
    used_edges = set()
    with open(results_file_path, "w") as f:
        print(f"Flujo máximo alcanzado: {flujo_maximo}MB", file=f)
        for c in caminos:
            for i in range(len(c[0]) - 1):
                u = c[0][i]
                v = c[0][i + 1]
                used_edges.add((u, v))

            print(f"Camino {' -> '.join(c[0])} con flujo {c[1]}MB", file=f)

        f.flush()
        print(f"Cantidad de aristas utilizadas: {len(used_edges)}", file=f)
        print(f"Resultados escritos en {results_file_path}")


G = Grafo()

G.agregar_arista('1', '2', 5)
G.agregar_arista('1', '3', 5)

G.agregar_arista('2', '6', 4)
G.agregar_arista('2', '9', 2)
G.agregar_arista('2', '5', 2)

G.agregar_arista('pivote-6-2', '2', 4)
G.agregar_arista('6', 'pivote-6-2', 4)
G.agregar_arista('6', '9', 3)

G.agregar_arista('pivote-9-6', '6', 3)
G.agregar_arista('9', 'pivote-9-6', 3)
G.agregar_arista('9', '10', 3)
G.agregar_arista('9', 'pivote-9-2', 2)
G.agregar_arista('pivote-9-2', '2', 2)

G.agregar_arista('pivote-5-2', '2', 2)
G.agregar_arista('5', 'pivote-5-2', 2)
G.agregar_arista('5', '7', 3)
G.agregar_arista('5', '3', 3)

G.agregar_arista('pivote-7-5', '5', 3)
G.agregar_arista('7', 'pivote-7-5', 2)
G.agregar_arista('7', 'pivote-7-3', 2)
G.agregar_arista('7', 'pivote-7-4', 1)
G.agregar_arista('7', '10', 4)

G.agregar_arista('pivote-3-5', '5', 3)
G.agregar_arista('3', 'pivote-3-5', 3)
G.agregar_arista('3', '7', 2)
G.agregar_arista('3', '4', 3)

G.agregar_arista('pivote-7-3', '3', 2)
G.agregar_arista('pivote-4-3', '3', 3)

G.agregar_arista('4', 'pivote-4-3', 3)
G.agregar_arista('4', '7', 1)
G.agregar_arista('4', '8', 4)
G.agregar_arista('pivote-7-4', '4', 1)

G.agregar_arista('8', 'pivote-8-4', 4)
G.agregar_arista('8', '10', 3)
G.agregar_arista('pivote-8-4', '4', 4)

algoritmo(G, '1', '10', 10)
