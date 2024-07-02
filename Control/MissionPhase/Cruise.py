import scipy as sp
import numpy as np
from Control.MissionPhase.MissionPhase import MissionPhase
from math import copysign

class Cruise(MissionPhase):

    def Downwind_Solve_1(self, tmax = 60, delta_t = 1e-2):
        tArr = np.arange(0, tmax, delta_t)
        tArr = np.append(tArr, tmax + delta_t)
        self.V_des = 90*self.knots_to_mps # knots
        self.RPM = 2200
        self.Altitude = self.Aircraft.Altitude
        self.Atmosphere_attr()
        V_infty = self.V_des
        self.Aircraft.Velocity = V_infty*np.array([1,0,0])
        self.Aircraft.V_infty = V_infty
        self.Aircraft.Pitch = 0

        self.Aircraft.Set_Lift()
        self.Get_Aircraft_Attr() 
        self.Position = self.Aircraft.Position
        self.Velocity = self.Aircraft.Velocity
        def Cruise_EOM(State, mass):
            x, y, z, v_x, v_y, v_z, RPM = State
            self.Aircraft.V_infty = v_x
            self.RPM = RPM
            self.Aircraft.Set_Lift()
            self.Get_Aircraft_Attr()
            return np.array([v_x, v_y, v_z, (self.Thrust-self.Drag)/mass, 0, 0, self.delta_RPM(v_x)])
        Initial = np.block([self.Position, self.Velocity, self.RPM])
        Solution = self.Adam_Bashforth_Solve(Initial, Cruise_EOM, tmax, delta_t)
        
        self.Position_x = Solution[:,0]
        self.Position_y = Solution[:,1]
        self.Position_z = Solution[:,2]
        self.Velocity_List = Solution[:,3]
        self.RPM_List = Solution[:,6]
        self.Times = tArr
        self.List_to_Array()

    def delta_RPM(self, V_infty):
        """
        This method will evaluate what the change in the RPM should be based on how fast the aircraft is going currently. 
        It utlilizes a velocity comparison so that it adjusts the RPM at a constant rate until it is within an error near the desired velocity.
        Within the error distance, it slows how much the throttle needs to adjust. 
        """
        
        V_des = self.V_des
        if abs(V_des-V_infty) <= .5:
            return (V_des-V_infty)/V_des*self.MaxRPM
        else:
            return copysign(1/27, V_des-V_infty)*self.MaxRPM