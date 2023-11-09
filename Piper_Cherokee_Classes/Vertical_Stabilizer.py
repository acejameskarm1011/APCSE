#Vertical_Stabilizer
from Piper import Piper
class VerticalStabilizer(Piper):
    PartName = "VerticalStabilizer"
    def __init__(self, AircraftName, PartName = PartName) -> None:
        self.AircraftName = AircraftName
        self.Name = self.AircraftName + PartName
    def EvaluateC_D(self):
        return 10**(-5)