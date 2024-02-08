from Aircraft import Aircraft
class VerticalStabilizer(Aircraft):
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
    PartName = "Vertical_Stabilizer"
    def __init__(self, AircraftName, AircraftDict) -> None:
        self.AircraftName = AircraftName
        self.Name = self.AircraftName + self.PartName
        self.Dictionary_setattr(AircraftDict[self.PartName])
    def EvaluateC_D(self):
        return 10**(-5)