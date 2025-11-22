from .grafo import Grafo
from pathlib import Path
import pulp

def prog_lineal(grafo, nodo_inicio, nodo_fin, capacidad_maxima):
    problema = pulp.LpProblem("min_links", pulp.LpMinimize)
    aristas = grafo.obtener_aristas()

    X = {}  
    F = {}  
    for (i, j) in aristas:
        X[(i, j)] = pulp.LpVariable(f"X_{i}_{j}", cat=pulp.LpBinary)
        F[(i, j)] = pulp.LpVariable(f"F_{i}_{j}", lowBound=0, cat=pulp.LpContinuous)

    problema += pulp.lpSum([X[e] for e in aristas])

    for (i, j) in aristas:
        flujo_maximo = grafo.adyacencia[i][j]
        problema += F[(i, j)] <= flujo_maximo * X[(i, j)], f"cap_link_{i}_{j}"

    nodos = sorted({n for e in aristas for n in e})
    for n in nodos:
        inflow = pulp.lpSum([F[(i, j)] for (i, j) in aristas if j == n])
        outflow = pulp.lpSum([F[(i, j)] for (i, j) in aristas if i == n])
        if n == nodo_inicio:
            problema += outflow - inflow == capacidad_maxima, f"flow_source_{n}"
        elif n == nodo_fin:
            problema += inflow - outflow == capacidad_maxima, f"flow_sink_{n}"
        else:
            problema += inflow - outflow == 0, f"flow_cons_{n}"

    problema.solve()

    status = pulp.LpStatus[problema.status]
    print("Status:", status)
    if status != "Optimal":
        print("Sin solucion optima.")
        return None

    sol_X = {e: int(pulp.value(X[e])) for e in aristas}
    sol_F = {e: float(pulp.value(F[e])) for e in aristas}

    resultados_path = Path(__file__).parent / "resultados.txt"
    with open(resultados_path, "w", encoding="utf-8") as fh:
        fh.write(f"Resultado objetivo (enlaces usados): {pulp.value(problema.objective)}\n")
        fh.write("X (1 si enlace usado, caso contrario 0):\n")
        for e in sol_X:
            fh.write(f"  {e}: {sol_X[e]}\n")
        fh.write("F (flujo por enlace en MB):\n")
        for e in sol_F:
            fh.write(f"  {e}: {sol_F[e]}\n")



G = Grafo()

G.agregar_arista('1', '2', 5)
G.agregar_arista('1', '3', 5)

G.agregar_arista('2', '5', 2)
G.agregar_arista('2', '6', 4)
G.agregar_arista('2', '9', 2)

G.agregar_arista('3', '4', 3)
G.agregar_arista('3', '5', 3)
G.agregar_arista('3', '7', 2)

G.agregar_arista('4', '7', 1)
G.agregar_arista('4', '8', 4)

G.agregar_arista('5', '7', 2)

G.agregar_arista('6', '9', 3)

G.agregar_arista('7', '10', 4)

G.agregar_arista('8', '10', 3)

G.agregar_arista('9', '10', 3)

prog_lineal(G, '1', '10', 10)

