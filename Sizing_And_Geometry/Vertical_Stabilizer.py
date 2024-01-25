#Vertical_Stabilizer

class VerticalStabilizer():
    """
    This class stores all necessary methods for storing the necessary geometry and data of the vertical stabilizer for an aircraft.

    Paramters
    ---------

    AircraftName : str
        This parameter is important so that when displaying test statements, we know what instance of the vertical stabilizer are being used.
    
    Notes
    -----
    This class is still under progress
    """
    PartName = "VerticalStabilizer"
    def __init__(self, AircraftName) -> None:
        self.AircraftName = AircraftName
        self.Name = self.AircraftName + self.PartName
    def EvaluateC_D(self):
        return 10**(-5)