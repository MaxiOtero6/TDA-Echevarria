from utils.plot import Plot
from .dc_test import generate_test_cases
from .algo import dc
import time

SAMPLE_SIZE = 10


def get_execution_time(arr):
    start = time.time()
    res = dc(arr)
    end = time.time()
    return (end - start, len(arr), res)


results = []
cases = generate_test_cases(
    skip_base_cases=True, min=1_000, max=100_000_000, sample_size=SAMPLE_SIZE)
for arr, _ in cases:
    t, length, _ = get_execution_time(arr)
    results.append((t, length))
    print(f'[{len(results)}/{SAMPLE_SIZE}]')

results.sort(key=lambda x: x[1])
times = [t for t, _ in results]
lengths = [l for _, l in results]

print(times)

plot = Plot(lengths, times)
plot.add_title('Divide and Conquer Execution Time')
plot.add_x_label('Input Size (N)')
plot.add_y_label('Execution Time (seconds)')
plot.plot_logn_regression()
plot.plot_poly_regression(degree=1)
plot.show()
