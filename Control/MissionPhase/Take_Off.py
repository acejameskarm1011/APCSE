from Control.Control import Control
import numpy as np
import scipy as sp

class Take_Off(Control):
    """
    This is the class that holds the methods required for running a Take-Off simulation. 
    """
    def __init__(self, AircraftInstance) -> None:
        self.aircraft = AircraftInstance
    def Ground_Roll_Sim_ODESolve(self, tmax = 120, dt = 1e-3):
        """
        This method runs the ground roll simulation of the aircraft. The class will no store data past the rotation speed, however, this method will return all paramters from 
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
        V_NE = self.aircraft.NeverExceedSpeed
        S = self.aircraft.Wings.S_wing
        g, rho = self.g, self.rho
        def Thrust(V_infty):
            Thrust = self.aircraft.Engine.Get_Thrust(V_infty, V_NE)
            return Thrust
        C_D = self.aircraft.Wings.Get_C_D()
        C_L = self.aircraft.Wings.Get_C_L()

        def mass(t):
            mdot = self.aircraft.Engine.Get_FuelConsumption()
            mass = self.aircraft.TotalMass + mdot*t
            return mass
        mu_f = 0.04
        tArr = np.arange(0, tmax, dt)
        def TakeOff_ODE(Dot, t):
            v_x, v_y, v_z, x, y, z = Dot
            dv_xdt = 1/mass(t)*(Thrust(v_x)-.5*rho*S*C_D*v_x**2-(mass(t)*g-.5*rho*C_L*v_x**2)*mu_f)
            dv_ydt = 0
            dv_zdt = 0
            dxdt = v_x
            dydt = v_y
            dzdt = v_z
            return [dv_xdt, dv_ydt, dv_zdt, dxdt, dydt, dzdt]
        
        Initial = np.zeros(6)
        solution = sp.integrate.odeint(TakeOff_ODE, Initial, tArr)
        vx = solution[:,0]
        self.Velocity_x = solution[:,0][vx <= V_y]
        self.Velocity_y = solution[:,1][vx <= V_y]
        self.Velocity_z = solution[:,2][vx <= V_y]
        self.Position_x = solution[:,3][vx <= V_y]
        self.Position_y = solution[:,4][vx <= V_y]
        self.Position_z = solution[:,5][vx <= V_y]
        self.Thrust = Thrust(self.Velocity_x)
        self.Times = tArr[vx <= V_y]
        self.Weight = mass(self.Times)*g
        self.Lift = .5*rho*S*C_L*self.Velocity_x**2
        self.Drag = .5*rho*S*C_D*self.Velocity_x**2
        solution = np.block([solution, tArr.reshape(len(tArr),1)])
        if not np.any(np.abs(self.Velocity_x*self.mps_to_knots) > V_y):
            print(vx*self.mps_to_knots)
            raise Exception("Simulation did not run long enough in order for rotation speed. Ajust and increase the time length so that the aircraft can reach rotation speed.")
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
        self.aircraft.TotalMass = self.aircraft.MGTOW
        self.aircraft.Weight = self.aircraft.g * self.aircraft.MGTOW
        self.aircraft.Range = 0
        self.aircraft.Endurance = 0
    