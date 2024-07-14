import numpy as np
from Control.MissionPhase.Take_Off import Take_Off



class Landing(Take_Off):
    """
    This is the class that holds the methods required for running a Landing simulation. 
    """

    def Ground_Roll(self, tmax = 60, delta_t = 5e-3):
        """
        This method runs the ground roll simulation of the Aircraft during landing. The class stores no data past the rotation speed, however, this method will return all paramters from 
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
        self.Altitude = 0
        self.Atmosphere_attr()
        self.Aircraft.Set_RPM(0)
        self.RPM = self.Aircraft.Engine.RPM
        self.Aircraft.Wings.Phase = "Landing"
        self.Pitch = 0

        self.Position = self.Aircraft.Position
        self.V_infty = self.Aircraft.V_infty

        self.Get_Aircraft_Attr()

        self.mu_f = 0.4

        tArr = np.arange(0, tmax, delta_t)
        tArr = np.append(tArr, tmax + delta_t)       

        Initial = np.block([self.Position, self.V_infty])
        Solution, tArr = self.Adam_Bashforth_Solve(Initial, self.Landing_ODE, tmax, delta_t)

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

        # if not np.any(self.V_infty < 0):
        #     raise Exception("Simulation did not run long enough to stop. Ajust and increase the time length so that the Aircraft can reach 0 speed.")
        
        self.Aircraft.Position = np.array([self.Position_x[-1], self.Position_y[-1], self.Position_z[-1]])
        print("Ground Rolls is: {} with a dt of {}".format((self.Position_x[-1]-self.Position[0])*self.m_to_ft, delta_t))


    def Condition(self):
         Bool = self.V_infty >= 0
         return Bool

    def Landing_ODE(self, State, mass):
        return self.TakeOff_ODE(State, mass)
    
    def __repr__(self) -> str:
          return "Landing"