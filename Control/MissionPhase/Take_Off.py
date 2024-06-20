from Control.MissionPhase.MissionPhase import MissionPhase
import numpy as np
import scipy as sp


class Take_Off(MissionPhase):
    """
    This is the class that holds the methods required for running a Take-Off simulation. 
    """
    
    def Ground_Roll_Sim_ODESolve(self, tmax = 30, delta_t = 5e-3):
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
        self.Aircraft.Set_Throttle(2700)
        self.reset()
        V_r = self.Aircraft.RotationSpeed*1.05
        self.Get_Aircraft_Attr()

        mu_f = 0.04
        tArr = np.arange(0, tmax, delta_t)
        tArr = np.append(tArr, tmax + delta_t)

        def TakeOff_ODE(Dot, mass):
            x, y, z, v_x, v_y, v_z  = Dot
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
        


        Initial = np.zeros(6, float)
        Solution = self.Adam_Bashforth_Solve(Initial, TakeOff_ODE, tmax, delta_t)
        vx = Solution[:,3]
        self.Velocity_x = Solution[:,3][vx <= V_r]
        self.Velocity_y = Solution[:,4][vx <= V_r]
        self.Velocity_z = Solution[:,5][vx <= V_r]
        self.Position_x = Solution[:,0][vx <= V_r]
        self.Position_y = Solution[:,1][vx <= V_r]
        self.Position_z = Solution[:,2][vx <= V_r]
        self.Times = tArr[vx <= V_r]

        self.List_to_Array()
        self.Lift_List = self.Lift_List[vx <= V_r]
        self.Thrust_List = self.Thrust_List[vx <= V_r]
        self.Drag_List = self.Drag_List[vx <= V_r]
        self.Weight_List = self.Weight_List[vx <= V_r]
        self.Percent_List = self.Percent_List[vx <= V_r]

        Solution = np.block([Solution, tArr.reshape(len(tArr),1)])
        if not np.any(np.abs(self.Velocity_x*self.mps_to_knots) > V_r):
            print(vx*self.mps_to_knots)
            raise Exception("Simulation did not run long enough in order for rotation speed. Ajust and increase the time length so that the Aircraft can reach rotation speed.")
        self.Aircraft.Velocity = np.array([self.Velocity_x[-1], self.Velocity_y[-1], self.Velocity_z[-1]])
        self.Aircraft.Position = np.array([self.Position_x[-1], self.Position_y[-1], self.Position_z[-1]])
        self.Aircraft.Endurance = self.Times[-1]
        print("Ground Rolls is: {} with a dt of {}".format(self.Position_x[-1]*self.m_to_ft, delta_t))
        return Solution

    
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
        MGTOW = self.Aircraft.Mass.MGTOW
        self.Aircraft.TotalMass = MGTOW
        self.Aircraft.Weight = self.g * MGTOW
        self.Aircraft.Range = 0
        self.Aircraft.Endurance = 0
    