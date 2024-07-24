import scipy as sp
import numpy as np
from Control.MissionPhase.MissionPhase import MissionPhase
from math import copysign

class Cruise(MissionPhase):
    """
    This class holds the methods required to run a cruise mission leg. Since aircraft engines change performance, it is required that there
    is a desired RPM for such an engine.

    Parameters
    ---------
    """
    def __init__(self, AircraftInstance, RPM_des) -> None:
        super().__init__(AircraftInstance)
        self.RPM_des = RPM_des

    def Downwind_Solve_1(self, tmax = 60, delta_t = 1e-2):
        print("{} is now Cruising".format(self.Aircraft.AircraftName))
        self.alpha = self.Aircraft.alpha
        self.Aircraft.alpha = self.alpha
        self.Aircraft.Wings.alpha = self.alpha
        self.V_des = 90*self.knots_to_mps
        self.RPM = self.Aircraft.Engine.RPM
        
        self.Altitude = self.Aircraft.Altitude
        self.Atmosphere_attr()
        V_infty = self.Aircraft.V_infty
        self.Pitch = 0
        self.Aircraft.Pitch = self.Pitch
        self.Aircraft.Wings.Phase = "Cruise"
        self.Get_Aircraft_Attr(set=True) 
        Position = self.Aircraft.Position

        self.tick = False
        Initial = np.block([Position, V_infty, self.RPM])
        Solution, tArr = self.Adam_Bashforth_Solve(Initial, self.Cruise_EOM, tmax, delta_t)
        self.Position_x = Solution[:,0]
        self.Position_y = Solution[:,1]
        self.Position_z = Solution[:,2]
        self.Velocity_List = Solution[:,3]
        self.Time_List = tArr
        self.List_to_Array()
        self.Aircraft.Position = np.array([self.Position_x[-1], self.Position_y[-1], self.Position_z[-1]])

        


    def Cruise_EOM(self, State, mass):
        x, y, z, V_infty, RPM = State
        self.V_infty = V_infty

        self.Aircraft.V_infty = V_infty
        
        if -0.01 >= self.V_des-V_infty >= -5*sp.constants.knot or self.tick:
            self.RPM = self.RPM_des
            self.tick = True
        else:
            self.RPM = RPM
        
        self.Get_Aircraft_Attr(set=True)

        dx_dt = V_infty
        dv_dt = (self.Thrust*np.cos(self.alpha)-self.Drag)/mass
        if dv_dt < 0 and self.tick:
            self.RPM_des += .1
        
        factor = 1
        if np.abs(dv_dt) > .5:
            factor = np.abs(dv_dt)
            factor = 1
        
        dRPM_dt = self.delta_RPM(V_infty, RPM)*factor
        if self.tick:
            dRPM_dt = 0
       
        return np.array([dx_dt, 0, 0, dv_dt, dRPM_dt])


    def Condition(self):
        Bool = self.V_infty < 60*sp.constants.knot
        Bool = True
        return Bool


    def delta_RPM(self, V_infty, RPM):
        """
        This method will evaluate what the change in the RPM should be based on how fast the aircraft is going currently. 
        It utlilizes a velocity comparison so that it adjusts the RPM at a constant rate until it is within an error near the desired velocity.
        Within the error distance, it slows how much the throttle needs to adjust. 
        """
        
        V_err = 5*sp.constants.knot
        RPM_err = 300

        V_des = self.V_des
        RPM_des = self.RPM_des
        if abs(V_des-V_infty) <= V_err and abs(RPM-RPM_des) <= RPM_err:
            factor = 10
            if abs(V_des-V_infty) <= V_err/2:
                factor = .2
            dRPM_dt = (V_des-V_infty)/V_des*self.MaxRPM*factor
        elif abs(V_des-V_infty) <= V_err:
            dRPM_dt = (RPM_des-RPM)/RPM_des*self.MaxRPM*.3
        else:
            dRPM_dt = -10
        if RPM >= self.MaxRPM and dRPM_dt > 0:
            dRPM_dt = 0
        if RPM < self.RPM_des*0.96 and dRPM_dt < 0:
            dRPM_dt = 0
        return dRPM_dt
        
    def List_to_Array(self):
        super().List_to_Array()
        self.RPM_List = np.array(self.RPM_List)

    def Save_Data(self):
        super().Save_Data()
        if not hasattr(self, "RPM_List"):
            self.RPM_List = [self.RPM]
        else:
            self.RPM_List.append(self.RPM)


    def Get_Aircraft_Attr(self, set=False):
        super().Get_Aircraft_Attr(set)
        self.alpha = self.Aircraft.alpha


    def __repr__(self) -> str:
          return "Cruise"