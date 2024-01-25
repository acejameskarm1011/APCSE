

class Fuselage():
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
    def __init__(self, AircraftName) -> None:
        self.AircraftName = AircraftName
        self.Name = self.AircraftName + self.PartName
        self.C_D = 10**(-5)
    def EvaluateC_D(self):
        return self.C_D