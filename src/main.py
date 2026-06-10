import numpy as np
import matplotlib.pyplot as plt
import pytest

print("Hello, World!")

x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.plot(x, y)
plt.title("Test Plot")
plt.savefig("test_plot.png")
