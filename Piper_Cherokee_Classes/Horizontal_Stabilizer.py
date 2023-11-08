#Horizontal_Stabilizer
class HorizontalStabilizer:
    PartName = "HorizontalStabilizer"
    def __init__(self, AircraftName, PartName = PartName, e0 = 1, C_L = 0) -> None:
        self.AircraftName = AircraftName
        self.Name = self.AircraftName + PartName
        self.C_L = C_L
        self.e0 = e0
    def EvaluateC_D(self):
        return 0.005