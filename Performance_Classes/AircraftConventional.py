#PerformanceV2

from PerformanceOLD import *
from Aircraft import *


class AircraftConventional(Aircraft):
    def __init__(self, AircraftName, CruiseMach, CruiseAltitude, AircraftType, AircraftDictionary) -> None:
        super().__init__(AircraftName, CruiseMach, CruiseAltitude, AircraftType, AircraftDictionary)
    def Emergency_Check(self):
        if self.EnergyMass < 0:
            self.Thrust = 0
            self.Power_Thrust = 0
            self.Emergency = "No_Energy"
            print(f'{self.AircraftName} has no fuel')
    def GetSC(self):
        self.GetTSFC(unit = 's')
        return None