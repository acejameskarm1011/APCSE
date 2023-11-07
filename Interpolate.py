import numpy as np
def Interpolate(known, unknown, value):
    x = unknown
    y = known
    diff = y-value
    minimum = np.abs(diff).min()
    if value+minimum in y:
        upper = y[y == value+minimum][0]
        lower = y[y < upper][-1]
    elif value-minimum in y:
        lower = y[y == value-minimum][0]
        upper = y[y > lower][0]
    else:
        print("Nothing passed")
        return None
    per = (value-lower)/(upper-lower)
    interpolated = per*(x[y==upper][0]-x[y==lower][0]) + x[y==lower][0]
    return interpolated
