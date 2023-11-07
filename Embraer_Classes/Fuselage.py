#Fuselage

from ImportEmbraer import Embraer

class Fuselage(Embraer):
    PartName = "Fuselage"
    def __init__(self, AircraftName, HybridFactor=0, Mach=0, Altitude=0, Range=0, Endurance=0, PartName = PartName) -> None:
        super().__init__(AircraftName, HybridFactor, Mach, Altitude, Range, Endurance)
        self.Name = self.AircraftName + PartName
        self.C_D = self.C_D0
