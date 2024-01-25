#Wings 
from Aircraft import Aircraft
class Wings(Aircraft):
    """
    This class stores all necessary methods for storing the necessary geometry and data of the wings for an aircraft.

    Paramters
    ---------

    AircraftName : str
        This parameter is important so that when displaying test statements, we know what instance of the wings are being used.
    
    Notes
    -----
    This class is still under progress
    """
    PartName = "Wings"
    def __init__(self, AircraftName) -> None:
        self.AircraftName = AircraftName
        self.Name = self.AircraftName + self.PartName
    def EvaluateC_D(self):
        return 0.03