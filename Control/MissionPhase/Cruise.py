import scipy as sp
import numpy as np
from Control.MissionPhase.MissionPhase import MissionPhase

class Cruise(MissionPhase):
    def __init__(self, AircraftInstance) -> None:
        self.aircraft = AircraftInstance
    
    def Downwind_Solve_1(self, tmax = 60, delta_t = 1e-2):
        V_des = 90 # knots
        RPM_Setting = 2200
        self.Atmosphere_attr()
        S = self.aircraft.Wings.S_wing
        V_infty = V_des*self.knots_to_mps
        Lift = self.aircraft.Weight
        self.aircraft.Set_Lift(Lift)
        