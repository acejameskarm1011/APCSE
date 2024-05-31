from Control.Control import Control
import numpy as np
import scipy as sp

'''
class Take_Off(Control):
    """
    This is the class that holds the methods required for running a Take-Off simulation. 
    """
    def __init__(self, AircraftInstance) -> None:
        self.aircraft = AircraftInstance
    def Ground_Roll_Sim_ODESolve(self, tmax = 20, dt = 1e-3):
        """
        This method runs the ground roll simulation of the aircraft. The class stores no data past the rotation speed, however, this method will return all paramters from 
        the entire timeframe from t=0 to t=tmax.

        Paramters
        ---------
        tmax : int/float
            Maximum time run of simulation in [s]
        dt : int/float
            Time step that will determine the step length in the time array

        Returns
        -------
        solution : numpy.ndarry
            An array where each column corresponds to a different property, ie 
            [vx, vy, vz, x, y, z, t]
        
        Notes: The restricted ground roll is stored inside the instance of the Take_Off class
        """
        self.reset()
        V_y = self.aircraft.RotationSpeed
        S = self.aircraft.Wings.S_wing  # meters^2
        g, rho = self.g, self.rho
        C_D = self.aircraft.Wings.Get_C_D()
        C_L = self.aircraft.Wings.Get_C_L()

        self.Thrust = np.array([0])
        self.Weight = np.array([0])
        mu_f = 0.04
        tArr = np.arange(0, tmax, dt)
        i = 0
        def TakeOff_ODE(Dot, mass, t):
            x, y, z, v_x, v_y, v_z  = Dot
            Position = np.array([x, y, z])
            Velocity = np.array([v_x, v_y, v_z])
            self.aircraft.Velocity = Velocity
            V_infty = np.sqrt(Velocity.T@Velocity)
            Thrust = self.aircraft.GetTotalThrust(V_infty)
            dxdt = v_x
            dydt = v_y
            dzdt = v_z
            dv_xdt = 1/mass*(Thrust-.5*rho*S*C_D*v_x**2-(mass*g-.5*rho*C_L*v_x**2)*mu_f)
            dv_ydt = 0
            dv_zdt = 0
            self.aircraft.FuelDraw(dt)
            self.Thrust = np.append(self.Thrust, Thrust)
            self.Weight = np.append(self.Weight, mass*g)
            return [dv_xdt, dv_ydt, dv_zdt, dxdt, dydt, dzdt]
        Initial = np.zeros(6, float)



        solution = sp.integrate.odeint(TakeOff_ODE, Initial, tArr)
        vx = solution[:,0]
        self.Velocity_x = solution[:,0][vx <= V_y]
        self.Velocity_y = solution[:,1][vx <= V_y]
        self.Velocity_z = solution[:,2][vx <= V_y]
        self.Position_x = solution[:,3][vx <= V_y]
        self.Position_y = solution[:,4][vx <= V_y]
        self.Position_z = solution[:,5][vx <= V_y]
        self.Times = tArr[vx <= V_y]
        self.Lift = .5*rho*S*C_L*self.Velocity_x**2
        self.Drag = .5*rho*S*C_D*self.Velocity_x**2
        self.Thrust = self.Thrust[vx <= V_y]
        self.Weight = self.Weight[vx <= V_y]
        solution = np.block([solution, tArr.reshape(len(tArr),1)])
        if not np.any(np.abs(self.Velocity_x*self.mps_to_knots) > V_y):
            print(vx*self.mps_to_knots)
            raise Exception("Simulation did not run long enough in order for rotation speed. Ajust and increase the time length so that the aircraft can reach rotation speed.")
        self.aircraft.Velocity = np.array([self.Velocity_x[-1], self.Velocity_y[-1], self.Velocity_z[-1]])
        self.aircraft.Position = np.array([self.Position_x[-1], self.Position_y[-1], self.Position_z[-1]])
        self.aircraft.Endurance = self.Times[-1]
        self.aircraft.Weight = self.Weight[-1]
        self.aircraft.Lift = self.Lift[-1]
        self.aircraft.Thrust = self.Thrust[-1]
        self.aircraft.Drag = self.Drag[-1]
        return solution

    def reset(self):
        """
        ONLY RUN IF YOU WANT THE AIRCRAFT TO HAVE THE BASE STATE OF TAKE-OFF.

        This method starts the aircraft off at a state at ground level and with zero.
        """
        self.Altitude = 0
        self.Atmosphere_attr()
        self.aircraft.Altitude = 0
        self.aircraft.Atmosphere_attr()
        self.aircraft.Velocity = np.zeros(3)
        self.aircraft.Position = np.zeros(3)
        MGTOW = self.aircraft.Mass.MGTOW
        self.aircraft.TotalMass = MGTOW
        self.aircraft.Weight = self.aircraft.g * MGTOW
        self.aircraft.Range = 0
        self.aircraft.Endurance = 0

'''
class Take_Off(Control):
    """
    This is the class that holds the methods required for running a Take-Off simulation. 
    """
    def __init__(self, AircraftInstance) -> None:
        self.aircraft = AircraftInstance
    def Ground_Roll_Sim_ODESolve(self, tmax = 20, dt = 1e-3):
        """
        This method runs the ground roll simulation of the aircraft. The class stores no data past the rotation speed, however, this method will return all paramters from 
        the entire timeframe from t=0 to t=tmax.

        Paramters
        ---------
        tmax : int/float
            Maximum time run of simulation in [s]
        dt : int/float
            Time step that will determine the step length in the time array

        Returns
        -------
        solution : numpy.ndarry
            An array where each column corresponds to a different property, ie 
            [vx, vy, vz, x, y, z, t]
        
        Notes: The restricted ground roll is stored inside the instance of the Take_Off class
        """
        self.reset()
        V_y = self.aircraft.RotationSpeed
        S = self.aircraft.Wings.S_wing  # meters^2
        g, rho = self.g, self.rho
        C_D = self.aircraft.Wings.Get_C_D()
        C_L = self.aircraft.Wings.Get_C_L()

        ThrustArr = [self.aircraft.GetTotalThrust()]
        WeightArr = [self.aircraft.TotalMass*g]
        mu_f = 0.04
        tArr = np.arange(0, tmax+dt, dt)
        i = 0
        def TakeOff_ODE(Dot, mass):
            x, y, z, v_x, v_y, v_z  = Dot
            Position = np.array([x, y, z])
            Velocity = np.array([v_x, v_y, v_z])
            self.aircraft.Velocity = Velocity
            Thrust = self.aircraft.GetTotalThrust()
            dxdt = v_x
            dydt = v_y
            dzdt = v_z
            dv_xdt = 1/mass*(Thrust-.5*rho*S*C_D*v_x**2-(mass*g-.5*rho*C_L*v_x**2)*mu_f)
            dv_ydt = 0
            dv_zdt = 0
            return np.array([dxdt, dydt, dzdt, dv_xdt, dv_ydt, dv_zdt])
        


        Initial = np.zeros(6, float)
        k = int(tmax/dt)
        solution = np.zeros((k+1, len(Initial)), float)
        u_0 = Initial
        u_1 = self.aircraft.Forward_Euler(TakeOff_ODE, u_0, dt)
        ThrustArr.append(self.aircraft.GetTotalThrust())
        WeightArr.append(self.aircraft.TotalMass*g)

        u_2 = self.aircraft.ab2(TakeOff_ODE, u_1, u_0, dt)
        ThrustArr.append(self.aircraft.GetTotalThrust())
        WeightArr.append(self.aircraft.TotalMass*g)
        solution[0:3,:] = [u_0, u_1, u_2]
        for i in range(2,k):
            u_km2 = solution[i-2, :]
            u_km1 = solution[i-1, :]
            u_k = solution[i, :]
            solution[i+1,:] = self.aircraft.ab3(TakeOff_ODE, u_k, u_km1, u_km2, dt)
            ThrustArr.append(self.aircraft.GetTotalThrust())
            WeightArr.append(self.aircraft.TotalMass*g)  
        # solution = sp.integrate.odeint(TakeOff_ODE, Initial, tArr)
        vx = solution[:,3]
        self.Velocity_x = solution[:,3][vx <= V_y]
        self.Velocity_y = solution[:,4][vx <= V_y]
        self.Velocity_z = solution[:,5][vx <= V_y]
        self.Position_x = solution[:,0][vx <= V_y]
        self.Position_y = solution[:,1][vx <= V_y]
        self.Position_z = solution[:,2][vx <= V_y]
        self.Times = tArr[vx <= V_y]
        self.Lift = .5*rho*S*C_L*self.Velocity_x**2
        self.Drag = .5*rho*S*C_D*self.Velocity_x**2
        self.Thrust = np.array(ThrustArr)[vx <= V_y]
        self.Weight = np.array(WeightArr)[vx <= V_y]
        solution = np.block([solution, tArr.reshape(len(tArr),1)])
        if not np.any(np.abs(self.Velocity_x*self.mps_to_knots) > V_y):
            print(vx*self.mps_to_knots)
            raise Exception("Simulation did not run long enough in order for rotation speed. Ajust and increase the time length so that the aircraft can reach rotation speed.")
        self.aircraft.Velocity = np.array([self.Velocity_x[-1], self.Velocity_y[-1], self.Velocity_z[-1]])
        self.aircraft.Position = np.array([self.Position_x[-1], self.Position_y[-1], self.Position_z[-1]])
        self.aircraft.Endurance = self.Times[-1]
        self.aircraft.Weight = self.Weight[-1]
        self.aircraft.Lift = self.Lift[-1]
        self.aircraft.Thrust = self.Thrust[-1]
        self.aircraft.Drag = self.Drag[-1]
        return solution

    def reset(self):
        """
        ONLY RUN IF YOU WANT THE AIRCRAFT TO HAVE THE BASE STATE OF TAKE-OFF.

        This method starts the aircraft off at a state at ground level and with zero.
        """
        self.Altitude = 0
        self.Atmosphere_attr()
        self.aircraft.Altitude = 0
        self.aircraft.Atmosphere_attr()
        self.aircraft.Velocity = np.zeros(3)
        self.aircraft.Position = np.zeros(3)
        MGTOW = self.aircraft.Mass.MGTOW
        self.aircraft.TotalMass = MGTOW
        self.aircraft.Weight = self.aircraft.g * MGTOW
        self.aircraft.Range = 0
        self.aircraft.Endurance = 0
    