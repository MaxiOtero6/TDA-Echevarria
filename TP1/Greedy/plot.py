from utils.plot import Plot
from .algo import greedy
import random
import time
from statistics import mean

SIZES = [
    10,
    100,
    1000,
    3000,
    5000,
    10000,
    20000,
    30000,
    40000,
    50000,
    60000,
    70000,
    80000,
    90000,
    100000,
]
RUNS = 10
RANDOM_SEED = 777


def generate_array(n: int) -> list[int]:
    return [random.randint(-100, 100) for _ in range(n)]


def time_once(arr: list[int]) -> float:
    start = time.perf_counter()
    greedy(arr)
    return time.perf_counter() - start


def benchmark():
    random.seed(RANDOM_SEED)
    lengths: list[int] = []
    avg_times: list[float] = []

    for n in SIZES:
        run_times: list[float] = []
        print(f"\nN = {n}")
        for r in range(1, RUNS + 1):
            arr = generate_array(n)
            t = time_once(arr)
            run_times.append(t)
            print(f"  Run {r}: {t:.6f} s")
        avg_t = mean(run_times)
        print(f"  Promedio: {avg_t:.6f} s")
        lengths.append(n)
        avg_times.append(avg_t)

    plot = Plot(lengths, avg_times)
    plot.add_title("Greedy - Tiempo promedio vs N")
    plot.add_x_label("Tamaño de entrada (N)")
    plot.add_y_label("Tiempo (s)")
    plot.plot_poly_regression(degree=1, color="grey")
    plot.plot_poly_regression(degree=2)
    plot.show()

    out_path = "greedy_results.txt"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("Benchmark Greedy\n")
        f.write(f"Runs por tamaño: {RUNS}\n")
        f.write("N\tPromedio_s\n")
        for n, avg in zip(lengths, avg_times):
            f.write(f"{n}\t{avg:.8f}\n")
    print(f"Resultados guardados en {out_path}")


if __name__ == "__main__":
    benchmark()
