#Fuselage

from ImportEmbraer import Embraer

class Fuselage(Embraer):
    PartName = "Fuselage"
    def __init__(self, AircraftName, PartName = PartName) -> None:
        self.AircraftName = AircraftName
        self.Name = self.AircraftName + PartName
        self.C_D = 10**(-5)
 