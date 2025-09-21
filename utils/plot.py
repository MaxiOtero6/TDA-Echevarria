import matplotlib.pyplot as plt
import numpy as np


class Plot:
    def __init__(self, x, y):
        self.x = np.array(x)
        self.y = np.array(y)
        self.fig, self.ax = plt.subplots()
        self.ax.scatter(self.x, self.y, zorder=10)
        x_pad = (self.x.max() - self.x.min()) * 0.05
        y_pad = (self.y.max() - self.y.min()) * 0.05
        self.ax.set_xlim(self.x.min() - x_pad, self.x.max() + x_pad)
        self.ax.set_ylim(self.y.min() - y_pad, self.y.max() + y_pad)

    def add_title(self, title):
        self.ax.set_title(title)

    def add_x_label(self, label):
        self.ax.set_xlabel(label)

    def add_y_label(self, label):
        self.ax.set_ylabel(label)

    def show(self):
        plt.show()

    def plot_poly_regression(self, degree=1, color='#a83291', style='--'):
        coeffs = np.polyfit(self.x, self.y, degree)
        x_fit = np.linspace(self.x.min(), self.x.max(), 100)
        y_fit = np.polyval(coeffs, x_fit)

        label = ' Regression'

        if degree == 0:
            label = 'O(1)' + label
        elif degree == 1:
            label = 'O(N)' + label
        else:
            label = f'O(N^{degree})' + label

        self.ax.plot(x_fit, y_fit, label=label,
                     color=color, linestyle=style, zorder=5)
        self.ax.legend()

    def plot_logn_regression(self, color='green', style='--'):
        x_log = np.log(self.x)
        coeffs = np.polyfit(x_log, self.y, 1)
        x_sorted = np.sort(self.x)
        x_log_sorted = np.log(x_sorted)
        y_fit = np.polyval(coeffs, x_log_sorted)
        self.ax.plot(x_sorted, y_fit,
                     label='O(log(N)) Regression', color=color, linestyle=style, zorder=5)
        self.ax.legend()

    def plot_nlogn_regression(self, color='orange', style='--'):
        x_nlogn = self.x * np.log(self.x)
        coeffs = np.polyfit(x_nlogn, self.y, 1)
        x_sorted = np.sort(self.x)
        x_nlogn_sorted = x_sorted * np.log(x_sorted)
        y_fit = np.polyval(coeffs, x_nlogn_sorted)
        self.ax.plot(x_sorted, y_fit,
                     label='O(N log(N)) Regression', color=color, linestyle=style, zorder=5)
        self.ax.legend()


# Example usage:

# l = list(range(1, 1000, 100))
# p = Plot(l, [np.log(i) for i in l])
# p.add_title("Sample Plot")
# p.add_x_label("X-axis")
# p.add_y_label("Y-axis")
# p.plot_poly_regression(degree=0, color='red')
# p.plot_poly_regression(degree=2)
# p.plot_logn_regression()
# p.plot_nlogn_regression()
# p.show()
