import scipy as sp
import numpy as np
from Control.MissionPhase.MissionPhase import MissionPhase

class Climb(MissionPhase): 
    """
    The purpose of the Climb class is to store the important parameters that define the climb phase for an aircraft.
     - V_y is the relative velocity required best rate of climb flight. Example, the PA28-181 requires a Vy of 76 knots.
     - The power setting will be the same as with take-off, FULL POWER
    """
    def __init__(self, Name, Vy) -> None:
        self.Name = Name
        self.Vy = Vy
        self.V_infty = self.Vy*sp.constants.knot
