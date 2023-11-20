#Wings 
from GA_Classes.GAAircraft import GAAircraft
class Wings(GAAircraft):
    PartName = "Wings"
    def __init__(self, AircraftName, PartName = PartName, e0 = 1) -> None:
        self.AircraftName = AircraftName
        self.Name = self.AircraftName + PartName
        self.e0 = e0
    def EvaluateC_D(self):
        return 0.03