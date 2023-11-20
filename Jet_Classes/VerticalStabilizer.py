#Vertical_Stabilizer

from Jet_Classes.ImportJet import JetAircraft

class VerticalStabilizer(JetAircraft):
    PartName = "VerticalStabilizer"
    def __init__(self, AircraftName, PartName = PartName) -> None:
        self.AircraftName = AircraftName
        self.Name = self.AircraftName + PartName
    def EvaluateC_D(self):
        return 10**(-5)