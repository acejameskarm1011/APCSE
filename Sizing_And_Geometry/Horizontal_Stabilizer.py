from Aircraft import Aircraft
class HorizontalStabilizer(Aircraft):
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
    PartName = "Horizontal_Stabilizer"
    def __init__(self, AircraftName, AircraftDict) -> None:
        self.AircraftName = AircraftName
        self.Name = self.AircraftName + self.PartName
        self.C_L = 0
        self.e0 = 1
        self.Dictionary_setattr(AircraftDict[self.PartName])
    def EvaluateC_D(self):
        return 0.005