from Control.MissionPhase.MissionPhase import MissionPhase
import numpy as np
import scipy as sp


class Take_Off(MissionPhase):
    """
    This is the class that holds the methods required for running a Take-Off simulation. 
    """
    
    def Ground_Roll_Sim_ODESolve(self, tmax = 30, delta_t = 5e-3):
        """
        This method runs the ground roll simulation of the aircraft. The class stores no data past the rotation speed, however, this method will return all paramters from 
        the entire timeframe from t=0 to t=tmax.

        Paramters
        ---------
        tmax : int/float
            Maximum time run of simulation in [s]
        delta_t : int/float
            Time step that will determine the step length in the time array

        Returns
        -------
        solution : numpy.ndarry
            An array where each column corresponds to a different property, ie 
            [vx, vy, vz, x, y, z, t]
        
        Notes: The restricted ground roll is stored inside the instance of the Take_Off class
        """
        self.reset()
        V_r = self.aircraft.RotationSpeed
        self.Get_Aircraft_Attr()

        mu_f = 0.04
        tArr = np.arange(0, tmax, delta_t)
        tArr = np.append(tArr, tmax + delta_t)

        def TakeOff_ODE(Dot, mass):
            x, y, z, v_x, v_y, v_z  = Dot
            Position = np.array([x, y, z])
            Velocity = np.array([v_x, v_y, v_z])
            self.aircraft.Velocity = Velocity
            self.Get_Aircraft_Attr()
            dxdt = v_x
            dydt = v_y
            dzdt = v_z
            dv_xdt = 1/mass*(self.Thrust-self.Drag-(mass*self.g-self.Lift)*mu_f)
            dv_ydt = 0
            dv_zdt = 0
            return np.array([dxdt, dydt, dzdt, dv_xdt, dv_ydt, dv_zdt])
        


        Initial = np.zeros(6, float)
        k = int(tmax/delta_t)
        solution = np.zeros((k+1, len(Initial)), float)
        u_0 = Initial
        self.Save_Data()

        u_1 = self.aircraft.Forward_Euler(TakeOff_ODE, u_0, delta_t)
        self.Save_Data()

        u_2 = self.aircraft.ab2(TakeOff_ODE, u_1, u_0, delta_t)
        self.Save_Data()
        solution[0:3,:] = [u_0, u_1, u_2]
        for i in range(2,k):
            u_km2 = solution[i-2, :]
            u_km1 = solution[i-1, :]
            u_k = solution[i, :]
            solution[i+1,:] = self.aircraft.ab3(TakeOff_ODE, u_k, u_km1, u_km2, delta_t)
            self.Save_Data()
        vx = solution[:,3]
        self.Velocity_x = solution[:,3][vx <= V_r]
        self.Velocity_y = solution[:,4][vx <= V_r]
        self.Velocity_z = solution[:,5][vx <= V_r]
        self.Position_x = solution[:,0][vx <= V_r]
        self.Position_y = solution[:,1][vx <= V_r]
        self.Position_z = solution[:,2][vx <= V_r]
        self.Times = tArr[vx <= V_r]

        self.Lift_List = np.array(self.Lift_List)[vx <= V_r]
        self.Thrust_List = np.array(self.Thrust_List)[vx <= V_r]
        self.Drag_List = np.array(self.Drag_List)[vx <= V_r]
        self.Weight_List = np.array(self.Weight_List)[vx <= V_r]
        self.Percent_List = np.array(self.Percent_List)[vx <= V_r]
        solution = np.block([solution, tArr.reshape(len(tArr),1)])
        if not np.any(np.abs(self.Velocity_x*self.mps_to_knots) > V_r):
            print(vx*self.mps_to_knots)
            raise Exception("Simulation did not run long enough in order for rotation speed. Ajust and increase the time length so that the aircraft can reach rotation speed.")
        self.aircraft.Velocity = np.array([self.Velocity_x[-1], self.Velocity_y[-1], self.Velocity_z[-1]])
        self.aircraft.Position = np.array([self.Position_x[-1], self.Position_y[-1], self.Position_z[-1]])
        self.aircraft.Endurance = self.Times[-1]
        print("Ground Rolls is: {} with a dt of {}".format(self.Position_x[-1]*self.m_to_ft, delta_t))
        return solution

    
    def reset(self, ground_level = 0):
        """
        ONLY RUN IF YOU WANT THE AIRCRAFT TO HAVE THE BASE STATE OF TAKE-OFF.

        This method starts the aircraft off at a state at ground level and with zero.
        """
        self.Altitude = ground_level
        self.Atmosphere_attr()
        self.aircraft.Altitude = ground_level
        self.aircraft.Velocity = np.zeros(3, float)
        self.aircraft.Position = np.zeros(3, float)
        MGTOW = self.aircraft.Mass.MGTOW
        self.aircraft.TotalMass = MGTOW
        self.aircraft.Weight = self.g * MGTOW
        self.aircraft.Range = 0
        self.aircraft.Endurance = 0
    