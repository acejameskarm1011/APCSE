from Aircraft import Aircraft
class LandingGear(Aircraft):
    """
    This class stores all necessary methods for storing the necessary geometry and data of the Landing Gear for an aircraft.

    Paramters
    ---------

    AircraftName : str
        This parameter is important so that when displaying test statements, we know what instance of the Landing Gear are being used.
    
    Notes
    -----
    This class is still under progress
    """
    PartName = "LandingGear"
    def __init__(self, AircraftName, AircraftDict) -> None:
        self.AircraftName = AircraftName
        self.Name = self.AircraftName + self.PartName
        self.C_D = 10**(-5)
        self.Dictionary_setattr(AircraftDict[self.PartName])
    def EvaluateC_D(self):
        return self.C_D