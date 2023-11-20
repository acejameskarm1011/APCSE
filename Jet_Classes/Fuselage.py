#Fuselage

from Jet_Classes.ImportJet import JetAircraft

class Fuselage(JetAircraft):
    PartName = "Fuselage"
    def __init__(self, AircraftName, PartName = PartName) -> None:
        self.AircraftName = AircraftName
        self.Name = self.AircraftName + PartName
        self.C_D = 10**(-5)
    def EvaluateC_D(self):
        return 0
 