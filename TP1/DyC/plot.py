from utils.plot import Plot
from .dc_test import generate_test_cases
from .algo import dc
import time

SAMPLE_SIZE = 25


def get_execution_time(arr):
    start = time.time()
    res = dc(arr, mock_sum=True)
    end = time.time()
    return (end - start, len(arr), res)


results = []
cases = generate_test_cases(
    skip_base_cases=True, min=1_000, max=100_000_000, sample_size=SAMPLE_SIZE
)
for arr, _ in cases:
    t, length, res = get_execution_time(arr)
    print(f"Execution time: {t}, Length: {length}, Result: {res}, check: {arr[res]}")
    results.append((t, length))
    print(f"[{len(results)}/{SAMPLE_SIZE}]")

results.sort(key=lambda x: x[1])

times = []
lengths = []
for t, l in results:
    times.append(t)
    lengths.append(l)

print(times)

plot = Plot(lengths, times)
plot.add_title("Divide and Conquer Execution Time")
plot.add_x_label("Input Size (N)")
plot.add_y_label("Execution Time (seconds)")
plot.plot_logn_regression()
plot.plot_poly_regression(degree=1)
plot.show()
