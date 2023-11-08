#Wings 
class Wings:
    PartName = "Wings"
    def __init__(self, AircraftName, PartName = PartName, e0 = 1) -> None:
        self.AircraftName = AircraftName
        self.Name = self.AircraftName + PartName
        self.e0 = self.e0
    def EvaluateC_D(self):
        return 0.03