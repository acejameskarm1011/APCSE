import scipy as sp
import numpy as np
from Control.MissionPhase.Climb import Climb
from math import copysign

class Descent(Climb):
    def __init__(self, AircraftInstance) -> None:
        super().__init__(AircraftInstance)
        self.glideSlope = 3
        self.setDes_RPM()

        
    def setDes_RPM(self, h_p=700., V_des=80.):
        # print("working on check: ", self.call)
        self.Aircraft.Wings.Flaps(15) # Needs aircraft to descend more
        vInfty = self.Aircraft.V_infty
        alt = h_p
        alpha = self.Aircraft.alpha
        Pitch = self.Aircraft.Pitch

        RPM_des = 1000
        self.RPM = RPM_des
        deltamV = 100
        print("Starting here")

        self.Aircraft.V_infty = V_des * self.knots_to_mps
        self.Aircraft.Altitude = h_p
        self.Aircraft.Pitch = - self.glideSlope/180*np.pi
        self.Aircraft.Set_Lift()
        i = 0
        while np.abs(deltamV) > .1:
            self.Aircraft.Set_Lift()
            self.Get_Aircraft_Attr(True)
            deltamV = (self.Thrust*np.cos(self.alpha) - self.Weight*np.sin(self.Aircraft.Pitch) - self.Drag)
            self.RPM -= deltamV/2
            i += 1
            if self.RPM == 0 or i > 200:
                print("RPM: ", self.RPM)
                print(i, "Iterations")
                raise ValueError("This ain't correct")
        
        # print("AOA", self.Aircraft.alpha/np.pi*180)
        # exit()
        self.Aircraft.V_infty = vInfty
        self.Aircraft.Altitude = alt
        self.Aircraft.alpha = alpha
        self.Aircraft.Pitch = Pitch
        self.Aircraft.Wings.Flaps(0)
        self.Aircraft.Aircraft_Forces()
        self.RPM_des = round(self.RPM)
        print("RPM desired for Descent: ", self.RPM_des)
   
    def Approach_Descent(self, h_f = 0, tmax = 10*60, delta_t = 1e-2, printing = False):
        """
        This method of evaluating the aircraft's descent uses the same EOM as Climb's "Pattern_Work_Climb_Solve()" except there's a controller 
        that determines the what the engine's power setting should be based on the aircraft's state. 

        * EOM - RPM is now added to the EOM, but this does have limitations that shall be controlled for: 0 < RPM < 2700

        Currently this method holds the pitch angle constant at 3 deg, and it utilized a closed loop controller to constrain engine RPM withssssssss
        velocity
        """
        if printing:
            print("Beginning the descent phase")
        self.delta_t = delta_t
        Ground_Altitude = h_f
        self.z_min = Ground_Altitude * self.ft_to_m
        

        self.RPM = self.RPM_des

        tArr = np.arange(0, tmax, delta_t)
        tArr = np.append(tArr, tmax + delta_t)
        
        self.Pitch = -self.glideSlope/180*np.pi
        self.Aircraft.Wings.Flaps(30)
        self.Aircraft.Pitch = self.Pitch
        self.Position = self.Aircraft.Position
        self.V_infty = self.Aircraft.V_infty
        self.Get_Aircraft_Attr(set=True)
 
        Initial = np.block([self.Position, self.V_infty, self.Pitch])
        Solution, tArr = self.Adam_Bashforth_Solve(Initial, self.Pitch_EOM, tmax, delta_t)


        if printing:
            print("Descent is phase completed, now loading data")
        z = Solution[:,2]
        self.Position_x = Solution[:,0]
        self.Position_y = Solution[:,1]
        self.Position_z = Solution[:,2]
        self.Velocity_List = Solution[:,3]
        self.Pitch_List = Solution[:,4]
        self.Time_List = tArr

        self.List_to_Array()
        self.Lift_List = self.Lift_List
        self.Thrust_List = self.Thrust_List
        self.Drag_List = self.Drag_List
        self.Weight_List = self.Weight_List
        self.Percent_List = self.Percent_List
        self.Altitude_List = self.Altitude_List
        
        if printing:
            print("Time elapsed during descent: {} min".format(round(self.Time_List[-1]/60, 3)))
        if not np.any(z < Ground_Altitude):
            from Plotting.Plotting import Descent_Plot
            Descent_Plot(self, title = "Descent Failed")
            raise Exception("Simulation Failed. The aircraft was unable to descent to zero Altitude.")
        self.Aircraft.Position = np.array([self.Position_x[-1], self.Position_y[-1], self.Position_z[-1]])

    def Pitch_EOM(self, State, mass):
        x, y, z, V_infty, Pitch = State
        self.z = z
        set = True
        if z*self.m_to_ft < 175:
            self.Aircraft.Wings.Flaps(40)
            self.V_des = 70*sp.constants.knot
            set = False
        self.Aircraft.Altitude = z*self.m_to_ft
        self.Aircraft.V_infty = V_infty
        self.Aircraft.Pitch = Pitch

        Pitch_Factor = 0
        if Pitch < -self.glideSlope*np.pi/180 and z*self.m_to_ft < 170:
            Pitch_Factor = (-3*np.pi/180-Pitch)*1.5
        elif self.Aircraft.Wings.alpha > 6:
            Pitch_Factor = -0.5
        
        self.Get_Aircraft_Attr(set)
        dPosition_dt = V_infty*np.array([np.cos(Pitch), 0, np.sin(Pitch)])
        dgamma_dt = (self.Thrust*np.sin(self.alpha) + self.Lift - self.Weight*np.cos(Pitch))/(mass*V_infty) + Pitch_Factor
        dv_dt = (self.Thrust*np.cos(self.alpha) - self.Drag - self.Weight*np.sin(Pitch))/mass
        return np.array([*dPosition_dt, dv_dt, dgamma_dt])
    
    def Condition(self):
        Bool = self.z >= self.z_min or self.V_infty < 50*sp.constants.knot or self.alpha > 12
        return Bool

    def delta_RPM(self, V_infty, RPM):
        """
        This method will evaluate what the change in the RPM should be based on how fast the aircraft is going currently. 
        It utlilizes a velocity comparison so that it adjusts the RPM at a constant rate until it is within an error near the desired velocity.
        Within the error distance, it slows how much the throttle needs to adjust. 
        """
        
        V_err = 2*sp.constants.knot
        RPM_err = 500

        V_des = self.V_des
        RPM_des = self.RPM_des

        if abs(V_des-V_infty) <= V_err and abs(RPM-RPM_des) <= RPM_err:
            factor = 10
            if abs(V_des-V_infty) <= V_err/2:
                factor = 1
            dRPM_dt = (V_des-V_infty)/V_des*self.MaxRPM*factor
        elif abs(V_des-V_infty) <= V_err:
            dRPM_dt = (RPM_des-RPM)/RPM_des*self.MaxRPM*.3
        else:
            dRPM_dt = copysign(1/40, V_des-V_infty)
        if RPM >= self.MaxRPM and dRPM_dt > 0:
            dRPM_dt = 0
        # if RPM <= self.RPM_des*0.75 and dRPM_dt < 0:
        #     dRPM_dt = 0
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


    def reset(self):
        super().reset()
        delattr(self, "RPM_List")
        self.V_des = 80 * self.knots_to_mps

    def __repr__(self) -> str:
          return "Descent"
 
    def __dict__(self):
        dict = super().__dict__()
        dict["RPM [rev/min]"] = self.RPM_List
        return dict