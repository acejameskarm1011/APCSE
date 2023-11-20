#Wings

from Jet_Classes.ImportJet import JetAircraft
import numpy as np


class Wings(JetAircraft):
    PartName = "Wings"
    def __init__(self, AircraftName, PartName = PartName, e0 = 1) -> None:
        self.AircraftName = AircraftName
        self.Name = self.AircraftName + PartName
        self.e0 = e0
        self.C_D0 = 0.03

    def Dictionary_setattr(self, Dictionary):
        super().Dictionary_setattr(Dictionary)
        try:
            self.S_wet = 2*(self.S_wing-self.c_root*self.d_f)*(1+(.25*self.tc_MAX*(1+self.tc_maxtip/self.tc_MAX+self.tapratio_wingtip)/(1+self.tapratio_wingtip)))
            self.m1 = (self.c_joint-self.c_root)/(self.y_joint)
            self.m2 = (self.c_tip-self.c_joint)/self.ydiff
            self.part1 = self.y_joint**3*self.m1**3/3+self.y_joint**2*self.c_root*self.m1+self.y_joint*self.c_root**2
            self.part2 = ((self.c_joint + self.m2*self.ydiff)**3 -(self.c_joint+self.m2*self.y_joint)**3)/3/self.m2
            self.c_average = 2/self.S_wing*(self.part1 + self.part2)
            self.S = self.S_wing
            self.AR = self.b_wing**2/self.S
        except:
            # print("An error occured in the wings class")
            pass  
    def EvaluateC_D(self):
        self.k = (np.pi*self.AR*self.e0)**(-1)
        self.C_L_Wing = self.C_L*1.05
        self.C_Di = self.k * self.C_L_Wing**2
        self.C_D = self.C_D0 + self.C_Di
        return self.C_D