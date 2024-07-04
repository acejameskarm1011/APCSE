import scipy as sp
import numpy as np
from Control.MissionPhase.Climb import Climb
from math import copysign

class Descent(Climb):

    def NoFlaps_Descent_Kinematics(self):
        self.V_infty = 70 * self.knots_to_mps
        gamma = -3/180*np.pi
        Velocity = self.V_infty*np.array([np.cos(gamma),0,np.sin(gamma)])
        self.Aircraft.Velocity = Velocity
        self.Aircraft.Pitch = gamma
        self.Aircraft.Set_Lift()
        self.Get_Aircraft_Attr()

    def Approach_Descent(self, tmax = 1.9*60, delta_t = 1e-2):
        """
        This method of evaluating the aircraft's descent uses the same EOM as Climb's "Pattern_Work_Climb_Solve()" except there's a controller 
        that determines the what the engine's power setting should be based on the aircraft's state. 

        * EOM - RPM is now added to the EOM, but this does have limitations that shall be controlled for: 0 < RPM < 2700

        Currently this method holds the pitch angle constant at 3 deg, and it utilized a closed loop controller to constrain engine RPM withssssssss
        velocity
        """
        print("Beginning the descent phase")
        self.delta_t = delta_t
        Ground_Altitude = 0
        self.z_min = Ground_Altitude
        self.V_des = 70 * self.knots_to_mps
        self.RPM = 1500

        tArr = np.arange(0, tmax, delta_t)
        tArr = np.append(tArr, tmax + delta_t)

        self.V_infty = self.Aircraft.V_infty
        self.Aircraft.Set_Lift()
        self.Get_Aircraft_Attr()
        self.Pitch = -3/180*np.pi
        self.Aircraft.Wings.Flaps(40)
        self.Aircraft.Pitch = self.Pitch
        self.Position = self.Aircraft.Position
        self.Velocity = self.Aircraft.V_infty*np.array([np.cos(self.Pitch), 0, np.sin(self.Pitch)])
 
        Initial = np.block([self.Position, self.V_infty, self.Pitch, self.RPM])
        Solution, tArr = self.Adam_Bashforth_Solve(Initial, self.Pitch_EOM, tmax, delta_t)



        print("Descent is phase completed, now loading data")
        z = Solution[:,2]
        self.Position_x = Solution[:,0]
        self.Position_y = Solution[:,1]
        self.Position_z = Solution[:,2]
        self.Velocity_List = Solution[:,3]
        self.Pitch_List = Solution[:,4]
        self.RPM_List = Solution[:,5]
        self.Time_List = tArr

        self.List_to_Array()
        self.Lift_List = self.Lift_List
        self.Thrust_List = self.Thrust_List
        self.Drag_List = self.Drag_List
        self.Weight_List = self.Weight_List
        self.Percent_List = self.Percent_List
        self.Altitude_List = self.Altitude_List
        
        print("Time elapsed during descent: {} min".format(self.Time_List[-1]/60))
        if not np.any(z < Ground_Altitude):
            print(z*self.m_to_ft)
            raise Exception("Simulation did not run long enough to reach pattern altitude. Ajust and increase the time length so that the Aircraft can reach pattern altitude.")
        self.Aircraft.Position = np.array([self.Position_x[-1], self.Position_y[-1], self.Position_z[-1]])

    def Pitch_EOM(self, State, mass):
        x, y, z, V_infty, Pitch, RPM = State
        self.z = z
        self.RPM = RPM
        self.Aircraft.Altitude = z*self.m_to_ft
        self.Aircraft.V_infty = V_infty
        self.Aircraft.Pitch = Pitch

        self.Aircraft.Set_Lift()
        self.Get_Aircraft_Attr()
        dPosition_dt = V_infty*np.array([np.cos(Pitch), 0, np.sin(Pitch)])
        dgamma_dt = (self.Lift - self.Weight*np.cos(Pitch))/mass
        dv_dt = (self.Thrust - self.Drag - self.Weight*np.sin(Pitch))/mass
        dRPM_dt = self.delta_RPM(V_infty)
        if not np.isclose(self.RPM, RPM):
            dRPM_dt = -dRPM_dt
        dRPM_dt = 0
        return np.array([*dPosition_dt, dv_dt, dgamma_dt, dRPM_dt])
    
    def Condition(self):
        Bool = self.z >= self.z_min
        return Bool

    def delta_RPM(self, V_infty):
        """
        This method will evaluate what the change in the RPM should be based on how fast the aircraft is going currently. 
        It utlilizes a velocity comparison so that it adjusts the RPM at a constant rate until it is within an error near the desired velocity.
        Within the error distance, it slows how much the throttle needs to adjust. 
        """
        V_des = self.V_des
        if abs(V_des-V_infty) <= 1.4:
            return (V_des-V_infty)/V_des*self.MaxRPM
        else:
            return copysign(1/40, V_des-V_infty)*self.MaxRPM
        
    def __repr__(self) -> str:
          return "Descent"