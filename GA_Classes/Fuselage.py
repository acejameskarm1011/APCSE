#Fuselage
from GA_Classes.GAAircraft import GAAircraft
class Fuselage(GAAircraft):
    PartName = "Fuselage"
    def __init__(self, AircraftName, PartName = PartName) -> None:
        self.AircraftName = AircraftName
        self.Name = self.AircraftName + PartName
        self.C_D = 10**(-5)
    def EvaluateC_D(self):
        return self.C_D