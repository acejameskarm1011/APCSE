from Control.MissionPhase.MissionPhase import MissionPhase
import numpy as np
import scipy as sp


class Take_Off(MissionPhase):
    """
    This is the class that holds the methods required for running a Take-Off simulation. 
    """
    
    def Ground_Roll_Sim_ODESolve(self, tmax = 60, delta_t = 5e-3):
        """
        This method runs the ground roll simulation of the Aircraft. The class stores no data past the rotation speed, however, this method will return all paramters from 
        the entire timeframe from t=0 to t=tmax.

        Paramters
        ---------
        tmax : int/float
            Maximum time run of simulation in [s]
        delta_t : int/float
            Time step that will determine the step length in the time array

        Returns
        -------
        Solution : numpy.ndarry
            An array where each column corresponds to a different property, ie 
            [vx, vy, vz, x, y, z, t]
        
        Notes: The restricted ground roll is stored inside the instance of the Take_Off class
        """
        self.RPM = self.MaxRPM
        self.Aircraft.Set_RPM(self.RPM)
        self.reset()
        self.V_r = self.Aircraft.RotationSpeed
        V_r = self.V_r
        self.Get_Aircraft_Attr()
        self.Pitch = 0

        tArr = np.arange(0, tmax, delta_t)
        tArr = np.append(tArr, tmax + delta_t)

        Initial = np.zeros(4, float)
        
        Solution, tArr = self.Adam_Bashforth_Solve(Initial, self.TakeOff_ODE, tmax, delta_t)

        V_infty = Solution[:,3]
        self.Position_x = Solution[:,0]
        self.Position_y = Solution[:,1]
        self.Position_z = Solution[:,2]
        self.Velocity_List = Solution[:,3] 
        self.Time_List = tArr        
        self.List_to_Array()

        self.Aircraft.Position = np.array([self.Position_x[-1], self.Position_y[-1], self.Position_z[-1]])
        self.Aircraft.Endurance = self.Time_List[-1]
        self.GroundRoll = self.Position_x[-1]*self.m_to_ft
        print("Ground Rolls is: {} ft".format(round(self.GroundRoll)))
        print("Final take-off velocity: ", round(self.V_infty*self.mps_to_knots), "knots")

    def TakeOff_ODE(self, State, mass):
        x, y, z, V_infty = State
        self.V_infty = V_infty
        self.Get_Aircraft_Attr()
        dxdt = V_infty
        dydt = 0
        dzdt = 0

        if V_infty > self.V_r:
            self.Aircraft.alpha = 5/180*np.pi

        k_D = 1
        k_L = 1

        self.Normal = self.Weight-self.Lift-self.Thrust*np.sin(self.alpha)
        if self.Normal < 0:
            self.mu_f = 0
        dv_dt = (self.Thrust*np.cos(self.alpha)-self.Drag-(self.Normal)*self.mu_f)/mass
        return np.array([dxdt, dydt, dzdt, dv_dt])
    
    def reset(self, ground_level = 0):
        """
        ONLY RUN IF YOU WANT THE Aircraft TO HAVE THE BASE STATE OF TAKE-OFF.

        This method starts the Aircraft off at a state at ground level and with zero.
        """
        self.Altitude = ground_level
        self.Atmosphere_attr()
        self.Aircraft.Altitude = ground_level
        self.Aircraft.Velocity = np.zeros(3, float)
        self.Aircraft.Position = np.zeros(3, float)
    
    def Condition(self):
        Bool = self.Normal >= -5*self.lbf_to_kg*self.g
        return Bool

    def __repr__(self) -> str:
          return "Take-Off"
    
    def __dict__(self):
        dict = super().__dict__()
        # print(self.Weight_List)
        # exit()
        dict["Velocity [knots]"] = self.Velocity_List * self.mps_to_knots
        dict["Altitude [ft]"] = self.Altitude
        dict["Range [nmi]"] = self.Position_x * self.m_to_nmi
        dict["Time [s]"] = self.Time_List
        dict["RPM [rev/min]"] = self.MaxRPM
        dict["Ground Roll [ft]"] = self.Position_x * self.m_to_ft
        return dict