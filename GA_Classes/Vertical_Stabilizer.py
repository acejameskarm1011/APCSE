#Vertical_Stabilizer
from GA_Classes.GAAircraft import GAAircraft
class VerticalStabilizer(GAAircraft):
    PartName = "VerticalStabilizer"
    def __init__(self, AircraftName, PartName = PartName) -> None:
        self.AircraftName = AircraftName
        self.Name = self.AircraftName + PartName
    def EvaluateC_D(self):
        return 10**(-5)