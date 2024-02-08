import scipy as sp
import numpy as np
from Control.MissionPhase.MissionPhase import MissionPhase

class Climb(MissionPhase): 
    """
    The purpose of the Climb class is to store the important parameters that define the climb phase for an aircraft.
     - Name is an arbitrary title given to the inside of the instance, and will have no bearing on performance.
     - V_y is the relative velocity required best rate of climb flight. Example, the PA28-181 requires a Vy of 76 knots.
     - The VerticalSpeed is in units of feet per minute, and is a control decided by the pilot. Further plans hope to have the vertical speed more rigourously defined
    """
    def __init__(self, Name, Vy, VerticalSpeed) -> None:
        self.Name = Name
        self.Vy = Vy
        self.V_infty = self.Vy*sp.constants.knot
        self.VerticalSpeed = VerticalSpeed
test = Climb("test",76,1000)