from Aircraft import Aircraft
import numpy as np
class Fuselage(Aircraft):
    """
    This class stores all necessary methods for storing the necessary geometry and data of the fuselage for an aircraft.

    Paramters
    ---------

    AircraftName : str
        This parameter is important so that when displaying test statements, we know what instance of the fuselage are being used.
    
    Notes
    -----
    This class is still under progress
    """
    PartName = "Fuselage"
    def __init__(self, AircraftName, AircraftDict) -> None:
        self.AircraftName = AircraftName
        self.Name = self.AircraftName + self.PartName
        self.C_D = 10**(-5)
        self.Dictionary_setattr(AircraftDict[self.PartName])
        self.S_fus_b = (self.d_fus_b**2)*(np.pi/4)
    def EvaluateC_D(self):
        return self.C_D