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
        self.V_des = 70 * self.knots_to_mps
        self.RPM = 500

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
        def Descent_EOM(State, mass):
            return self.Pitch_EOM(State, mass)
        Initial = np.block([self.Position, self.V_infty, self.Pitch, self.RPM])
        Solution = self.Adam_Bashforth_Solve(Initial, Descent_EOM, tmax, delta_t)



        print("Descent is phase completed, now loading data")
        z = Solution[:,2]
        self.Position_x = Solution[:,0][z >= Ground_Altitude]
        self.Position_y = Solution[:,1][z >= Ground_Altitude]
        self.Position_z = Solution[:,2][z >= Ground_Altitude]
        self.Velocity_List = Solution[:,3][z >= Ground_Altitude]
        # self.Pitch_List = Solution[:,4][z >= Ground_Altitude]
        self.Pitch_List = Solution[:,4][z >= Ground_Altitude]
        self.RPM_List = Solution[:,5][z >= Ground_Altitude]
        self.Times = tArr[z >= Ground_Altitude]

        self.List_to_Array()
        self.Lift_List = self.Lift_List[z >= Ground_Altitude]
        self.Thrust_List = self.Thrust_List[z >= Ground_Altitude]
        self.Drag_List = self.Drag_List[z >= Ground_Altitude]
        self.Weight_List = self.Weight_List[z >= Ground_Altitude]
        self.Percent_List = self.Percent_List[z >= Ground_Altitude]
        self.Altitude_List = self.Altitude_List[z >= Ground_Altitude]
        self.Pitch_List = 3/180*np.pi*np.ones(len(self.Altitude_List))
        Solution = np.block([Solution, tArr.reshape(len(tArr),1)])
        print("Time elapsed during descent: {} min".format(self.Times[-1]/60))
        if not np.any(z < Ground_Altitude):
            print(z*self.m_to_ft)
            raise Exception("Simulation did not run long enough to reach pattern altitude. Ajust and increase the time length so that the Aircraft can reach pattern altitude.")
        self.Aircraft.Position = np.array([self.Position_x[-1], self.Position_y[-1], self.Position_z[-1]])

        """
        Comment
        -------
        Future plans for tomorrow hope to see how and when the engine setting should change. Should I update it within the Pitch_EOM function?
        Certainly not, as that will cause complications when the engine is at a different setting than what was expected. Should I add the engine
        RPM to the equations of motion? Maybe...

        It isn't a state variable, so I don't see why it would fit, but I do think that it could be valuable to investigate and see if that is a valid
        choice to make here. It would help with the saving of that information. Now the only thing left is to see where I could fit the whole solution.
        More abstraction, less abstration, and where and why? All of these questions, I will tackle in the morning, or maybe right after taking a shower
        """

    def Pitch_EOM(self, State, mass):
        x, y, z, V_infty, Pitch, RPM = State
        self.RPM = RPM
        self.Aircraft.Altitude = z*self.m_to_ft
        self.Aircraft.V_infty = V_infty
        self.Aircraft.Pitch = Pitch
        if abs(V_infty) < 0:
            raise ValueError("This velocity of {} is not possible".format(V_infty))
        self.Aircraft.Set_Lift()
        self.Get_Aircraft_Attr()
        dPosition_dt = V_infty*np.array([np.cos(Pitch), 0, np.sin(Pitch)])
        dgamma_dt = (self.Lift - self.Weight*np.cos(Pitch))/mass
        dv_dt = (self.Thrust - self.Drag - self.Weight*np.sin(Pitch))/mass
        dRPM_dt = self.delta_RPM(V_infty)
        if not np.isclose(self.RPM, RPM):
            dRPM_dt = -dRPM_dt
        return np.array([*dPosition_dt, dv_dt, dgamma_dt, dRPM_dt])
    
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
        
