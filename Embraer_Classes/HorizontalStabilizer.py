#Horizontal_Stabilizer

from ImportEmbraer import Embraer
import numpy as np

class HorizontalStabilizer(Embraer):
    PartName = "HorizontalStabilizer"
    def __init__(self, AircraftName, HybridFactor=0, Mach=0, Altitude=0, Range=0, Endurance=0, PartName = PartName, e0 = 1, C_L = 0) -> None:
        super().__init__(AircraftName, HybridFactor, Mach, Altitude, Endurance, e0, C_L)
        self.Name = self.AircraftName + PartName
    def Dictionary_setattr(self, Dictionary):
        super().Dictionary_setattr(Dictionary)
        self.tapratio_h = self.c_tip_h/self.c_root_h
        self.S_wet = self.S_exposed_h*(1.977 + .52*self.tc_MAX_h)
        self.c_average = 2/3*self.c_root_h*(1 + self.tapratio_h + self.tapratio_h**2)/(1 + self.tapratio_h)
        self.S_wet = self.S_exposed_h*(1.977 + .52*self.tc_MAX_h)
        self.AR = self.b_h**2/self.S_h
    def EvaluateC_D(self):
        self.k = (np.pi*self.AR*self.e0)**(-1)
        self.C_L_HS = self.C_L*-0.05
        self.C_Di = self.k * self.C_L_HS**2
        self.C_D = self.C_D0 + self.C_Di
        return self.C_D
