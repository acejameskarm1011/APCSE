#Horizontal_Stabilizer

class HorizontalStabilizer():
    """
    This class stores all necessary methods for storing the necessary geometry and data of the horizontal stabilizer for an aircraft.

    Paramters
    ---------

    AircraftName : str
        This parameter is important so that when displaying test statements, we know what instance of the horizontal stabilizer are being used.
    
    Notes
    -----
    This class is still under progress
    """
    PartName = "HorizontalStabilizer"
    def __init__(self, AircraftName) -> None:
        self.AircraftName = AircraftName
        self.Name = self.AircraftName + self.PartName
        self.C_L = 0
        self.e0 = 1
    def EvaluateC_D(self):
        return 0.005