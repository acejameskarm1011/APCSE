#Wings

from ImportEmbraer import Embraer
import numpy as np


class Wings(Embraer):
    PartName = "Wings"
    def __init__(self, AircraftName, Mach=0, Altitude=0, Range=0, Endurance=0, PartName = PartName, e0 = 1) -> None:
        super().__init__(AircraftName, Mach, Altitude, Endurance, e0)
        self.Name = self.AircraftName + PartName
        self.e0 = self.e0


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