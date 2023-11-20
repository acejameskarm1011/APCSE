#Fuselage
from Piper import Piper
class Fuselage(Piper):
    PartName = "Fuselage"
    def __init__(self, AircraftName, PartName = PartName) -> None:
        self.AircraftName = AircraftName
        self.Name = self.AircraftName + PartName
        self.C_D = 10**(-5)
