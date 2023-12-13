import numpy as np
from matplotlib import pyplot as plt
plt.rcParams["figure.figsize"] = [7.00, 3.50]
plt.rcParams["figure.autolayout"] = True
data = np.array([[2, 1], [-1, 2], [4, -1],[0,-1]])
origin = np.array([[0, 0, 0, 0],[0, 0, 0, 0]])
plt.quiver(*origin, data[:, 0], data[:, 1], color=['black', 'red', 'green', 'black'], scale=15)
plt.show()