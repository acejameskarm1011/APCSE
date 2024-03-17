import numpy as np

class Velocity:
    def __init__(self, V_infty, NeverExceedSpeed, Heading = 0, ClimbAngle = 0) -> None:
        self.V_infty = V_infty
        self.NeverExceedSpeed = NeverExceedSpeed
        self.Velocity = self.V_infty*np.array([1,0,0])