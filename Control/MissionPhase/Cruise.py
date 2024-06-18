import scipy as sp
import numpy as np
from Control.MissionPhase.MissionPhase import MissionPhase

class Cruise(MissionPhase):
    def __init__(self, AircraftInstance) -> None:
        self.Aircraft = AircraftInstance
    
    def Downwind_Solve_1(self, tmax = 60, delta_t = 1e-2):
        tArr = np.arange(0, tmax, delta_t)
        tArr = np.append(tArr, tmax + delta_t)
        V_des = 90 # knots
        self.Altitude = self.Aircraft.Altitude
        self.Atmosphere_attr()
        V_infty = V_des*self.knots_to_mps
        self.Aircraft.Velocity = V_infty*np.array([1,0,0])
        self.Aircraft.V_infty = V_infty
        Lift = self.Aircraft.Weight
        self.Aircraft.Set_Lift(Lift)
        self.Get_Aircraft_Attr()
        self.Position = self.Aircraft.Position
        self.Velocity = self.Aircraft.Velocity
        def Cruise_EOM(DOT, mass):
            x, y, z, v_x, v_y, v_z = DOT
            self.Get_Aircraft_Attr()
            return np.array([v_x, v_y, v_z, 0, 0, 0])
        Initial = np.block([self.Position, self.Velocity])
        Solution = self.Adam_Bashforth_Solve(Initial, Cruise_EOM, tmax, delta_t)
        
        self.Position_x = Solution[:,0]
        self.Position_y = Solution[:,1]
        self.Position_z = Solution[:,2]
        self.Velocity_List = Solution[:,3]
        self.Times = tArr
        self.List_to_Array()

    def Get_Aircraft_Attr(self):
        super().Get_Aircraft_Attr()
        self.RPM = self.Aircraft.Engine.RPM

    def Save_Data(self):
        super().Save_Data()
        if not hasattr(self, "RPM_List"):
            self.RPM_List = [self.RPM]
        else:
            self.RPM_List.append(self.RPM)

# What do I want with cruise? 
# Ground Roll
# RPM
# Fuel Percent
