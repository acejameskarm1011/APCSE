import scipy as sp
import numpy as np
from Control.MissionPhase.MissionPhase import MissionPhase

class Climb(MissionPhase): 
    """
    The purpose of the Climb class is to store the important parameters that define the climb phase for an Aircraft.
     - V_y is the relative velocity required best rate of climb flight. Example, the PA28-181 requires a Vy of 76 knots.
     - The power setting will be the same as with take-off, FULL POWER
    """ 
    def Pattern_Work_Climb_Solve(self, tmax = 100, delta_t = 1e-2, Pattern_Altitude = 700):
        """
        For pattern altitudes  it is usually about 700-1000 ft above ground level

        Paramters
        ---------
        tmax : int/float
            Maximum time run of simulation in [s]
        delta_t : int/float
            Time step that will determine the step length in the time array
        Pattern_Altitude : int/float [ft]
            Desired altitude to fly to
        """
        print("Climb Phase Starting")
        self.RPM = self.Aircraft.Engine.RPM
        self.V_infty = self.Aircraft.V_infty
        self.z_max = Pattern_Altitude*self.ft_to_m
        Max_z = self.z_max
        tArr = np.arange(0, tmax, delta_t)
        tArr = np.append(tArr, tmax + delta_t)
        self.Get_Aircraft_Attr()
        self.Pitch = 0
        self.Position = self.Aircraft.Position
        self.Velocity = self.Aircraft.Velocity


        Initial = np.block([self.Position, self.V_infty, self.Pitch])

        Solution, tArr = self.Adam_Bashforth_Solve(Initial, self.Pitch_EOM, tmax, delta_t)
        print("Climb phase completed")

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
        print("Time elapsed during climb: {} min".format(self.Time_List[-1]/60))
        if not np.any(z > Max_z):
            print(z[-5:-1]*self.m_to_ft)
            raise Exception("Simulation did not run long enough to reach pattern altitude. Ajust and increase the time length so that the Aircraft can reach pattern altitude.")
        self.Aircraft.Position = np.array([self.Position_x[-1], self.Position_y[-1], self.Position_z[-1]])


    def Pitch_EOM(self, State, mass):
        x, y, z, V_infty, Pitch = State
        self.z = z
        self.Aircraft.Position = np.array([x, y, z])
        self.V_infty = V_infty
        self.Get_Aircraft_Attr()

        dxdt = V_infty*np.cos(Pitch)
        dydt = 0
        dzdt = V_infty*np.sin(Pitch)
        
        dv_dt = (self.Thrust-self.Drag-self.Weight*np.sin(Pitch))/mass
        dgamma_dt = (self.Lift-self.Weight*np.cos(Pitch))/(mass*V_infty) - .2*Pitch
        if dgamma_dt < 0 and Pitch == 0:
            dgamma_dt = 0
        return np.array([dxdt, dydt, dzdt, dv_dt, dgamma_dt])

    def Condition(self):
        Bool = self.z <= self.z_max
        return Bool





    def Get_Aircraft_Attr(self):
        super().Get_Aircraft_Attr()
        self.Altitude = self.Aircraft.Altitude

    def List_to_Array(self):
        super().List_to_Array()
        self.Altitude_List = np.array(self.Altitude_List)


    def Save_Data(self):
        super().Save_Data()
        if not hasattr(self, "Altitude_List"):
            self.Altitude_List = [self.Altitude]
        else:
            self.Altitude_List.append(self.Altitude)

    def __repr__(self) -> str:
          return "Climb"