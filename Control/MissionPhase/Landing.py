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
        self.Pitch = 0

        self.Position = self.Aircraft.Position
        self.Velocity = self.Aircraft.V_infty*np.array([1,0,0])

        self.Get_Aircraft_Attr()

        mu_f = 0.4

        tArr = np.arange(0, tmax, delta_t)
        tArr = np.append(tArr, tmax + delta_t)

        def TakeOff_ODE(State, mass):
            x, y, z, v_x, v_y, v_z = State
            Position = np.array([x, y, z])
            Velocity = np.array([v_x, v_y, v_z])
            self.Aircraft.Velocity = Velocity
            self.Get_Aircraft_Attr()
            dxdt = v_x
            dydt = v_y
            dzdt = v_z
            dv_xdt = 1/mass*(self.Thrust-self.Drag-(mass*self.g-self.Lift)*mu_f)
            dv_ydt = 0
            dv_zdt = 0
            return np.array([dxdt, dydt, dzdt, dv_xdt, dv_ydt, dv_zdt])
        


        Initial = np.block([self.Position, self.Velocity])
        Solution = self.Adam_Bashforth_Solve(Initial, TakeOff_ODE, tmax, delta_t)
        vx = Solution[:,3]
        self.Velocity_x = Solution[:,3][vx >= 0]
        self.Velocity_y = Solution[:,4][vx >= 0]
        self.Velocity_z = Solution[:,5][vx >= 0]
        self.Position_x = Solution[:,0][vx >= 0]
        self.Position_y = Solution[:,1][vx >= 0]
        self.Position_z = Solution[:,2][vx >= 0]
        self.Time_List = tArr[vx >= 0]

        self.List_to_Array()
        self.Lift_List = self.Lift_List[vx >= 0]
        self.Thrust_List = self.Thrust_List[vx >= 0]
        self.Drag_List = self.Drag_List[vx >= 0]
        self.Weight_List = self.Weight_List[vx >= 0]
        self.Percent_List = self.Percent_List[vx >= 0]

        Solution = np.block([Solution, tArr.reshape(len(tArr),1)])
        # if not np.any(np.abs(self.Velocity_x*self.mps_to_knots) < 0):
        #     print(vx*self.mps_to_knots)
        #     raise Exception("Simulation did not run long enough in order for rotation speed. Ajust and increase the time length so that the Aircraft can reach rotation speed.")
        self.Aircraft.Velocity = np.array([self.Velocity_x[-1], self.Velocity_y[-1], self.Velocity_z[-1]])
        self.Aircraft.Position = np.array([self.Position_x[-1], self.Position_y[-1], self.Position_z[-1]])
        self.Aircraft.Endurance = self.Time_List[-1]
        print("Ground Rolls is: {} with a dt of {}".format((self.Position_x[-1]-self.Position[0])*self.m_to_ft, delta_t))
        return Solution
