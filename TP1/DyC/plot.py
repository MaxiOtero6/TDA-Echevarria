from utils.plot import Plot
from .dc_test import generate_test_cases
from .algo import dc
import time

SAMPLE_SIZE = 3


def get_execution_time(arr):
    start = time.time()
    res = dc(arr)
    end = time.time()
    return (end - start, len(arr), res)


times = []
cases = generate_test_cases(
    skip_base_cases=True, min=1_000_000_000, max=10_000_000_000, sample_size=SAMPLE_SIZE)
for arr, _ in cases:
    times.append(get_execution_time(arr))
    print(f'[{len(times)}/{SAMPLE_SIZE}]')

times = sorted(times, key=lambda x: x[1])

print(times)

plot = Plot(times[1], times[0])
plot.add_title('Divide and Conquer Execution Time')
plot.add_x_label('Input Size (N)')
plot.add_y_label('Execution Time (seconds)')
plot.plot_logn_regression()
plot.plot_poly_regression(degree=1)
plot.show()
