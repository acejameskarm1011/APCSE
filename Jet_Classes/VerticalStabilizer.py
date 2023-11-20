#Vertical_Stabilizer

from ImportEmbraer import Embraer

class VerticalStabilizer(Embraer):
    PartName = "VerticalStabilizer"
    def __init__(self, AircraftName, PartName = PartName) -> None:
        self.AircraftName = AircraftName
        self.Name = self.AircraftName + PartName
    def EvaluateC_D(self):
        return 10**(-5)