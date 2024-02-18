from Control.Control import Control
import numpy as np
class Take_Off(Control):
    """
    This is the class that holds the methods required for running a Take-Off simulation. 
    """
    def __init__(self, AircraftInstance) -> None:
        self.aircraft = AircraftInstance
    def reset(self):
        """
        ONLY RUN IF YOU WANT THE AIRCRAFT TO HAVE THE BASE STATE OF TAKE-OFF.

        This method starts the aircraft off at a state at ground level and with zero.
        """
        self.aircraft.Altitude = 0
        self.aircraft.Velocity = np.zeros(3)
        self.aircraft.Weight = self.aircraft.g * self.aircraft.MGTOW