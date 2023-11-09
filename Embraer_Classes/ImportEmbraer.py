#Embraer

from Aviation import *

class Embraer(Aviation):
    def __init__(self, AircraftName, CruiseMach, CruiseAltitude, S=0, HybridFactor=0, Mach=0, Altitude=0, Range=0, Endurance=0, C_D0 = 0.005, C_L = 0, e0 = 1) -> None:
        super().__init__(AircraftName, CruiseMach, CruiseAltitude, S, HybridFactor, Mach, Altitude, Range, Endurance)
        self.C_D0 = 0
        self.e0 = e0

    def EvaluateC_D(self):
        C_D = self.C_D0
        return C_D

from Embraer_Components import *