import numpy as np
from numpy.linalg import pinv
import matplotlib.pyplot as plt

x = np.array([0,1,2,3,4])/4
y = np.array([0,1,1.1,.7,0])/12




def solve_ls(x,y,p, n = 50):
    """
    For a given set of x and y points with a chosen polynomial degree of p,
    returns the solution.
    """
    a, b = x[0], x[-1]

    A = []
    for i in range(p+1):
        A.append((x**i).tolist())
    A = np.array(A).T
    pseudo_A = pinv(A)
    constants = pseudo_A@y
    x_ls = np.linspace(a,b,n)
    y_ls = np.zeros(x_ls.shape)

    for i, c in enumerate(constants):
        y_ls += c*x_ls**(i)
    return x_ls, y_ls, constants