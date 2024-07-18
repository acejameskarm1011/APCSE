from Control.MissionPhase.MissionPhase import MissionPhase
import numpy as np
import scipy as sp


class Take_Off(MissionPhase):
    """
    This is the class that holds the methods required for running a Take-Off simulation. 
    """
    
    def Ground_Roll_Sim_ODESolve(self, tmax = 40, delta_t = 5e-3):
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
        self.V_r = self.Aircraft.RotationSpeed*1.0
        V_r = self.V_r
        self.Get_Aircraft_Attr()
        self.Pitch = 0

        self.mu_f = 0.04
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
        self.Lift_List = self.Lift_List 
        self.Thrust_List = self.Thrust_List 
        self.Drag_List = self.Drag_List 
        self.Weight_List = self.Weight_List 
        self.Percent_List = self.Percent_List

        if not np.any(np.abs(self.Velocity_List*self.mps_to_knots) > V_r):
            print(V_infty*self.mps_to_knots)
            raise Exception("Simulation did not run long enough in order for rotation speed. Ajust and increase the time length so that the Aircraft can reach rotation speed.")
        
        self.Aircraft.Position = np.array([self.Position_x[-1], self.Position_y[-1], self.Position_z[-1]])
        self.Aircraft.Endurance = self.Time_List[-1]
        print("Ground Rolls is: {} ft".format(round(self.Position_x[-1]*self.m_to_ft)))

    def TakeOff_ODE(self, State, mass):
        x, y, z, V_infty = State
        self.V_infty = V_infty
        self.Get_Aircraft_Attr()
        dxdt = V_infty
        dydt = 0
        dzdt = 0
        
        dv_dt = (self.Thrust-self.Drag-(mass*self.g-self.Lift)*self.mu_f)/mass
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
        Bool = self.V_infty <= self.V_r
        return Bool

    def __repr__(self) -> str:
          return "Take-Off"