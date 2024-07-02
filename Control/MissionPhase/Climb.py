import scipy as sp
import numpy as np
from Control.MissionPhase.MissionPhase import MissionPhase

class Climb(MissionPhase): 
    """
    The purpose of the Climb class is to store the important parameters that define the climb phase for an Aircraft.
     - V_y is the relative velocity required best rate of climb flight. Example, the PA28-181 requires a Vy of 76 knots.
     - The power setting will be the same as with take-off, FULL POWER
    """ 
    def Pattern_Work_Climb_Solve(self, tmax = 60, delta_t = 1e-2, Pattern_Altitude = 700):
        """
        For pattern altitudes  it is usually about 700-1000 ft above ground level
        """
        print("Climb Phase Starting")
        self.V_infty = self.Aircraft.V_infty
        Max_z = Pattern_Altitude*self.ft_to_m
        tArr = np.arange(0, tmax, delta_t)
        tArr = np.append(tArr, tmax + delta_t)
        self.Get_Aircraft_Attr()
        self.Pitch = np.arccos(self.Aircraft.Velocity[0]/self.V_infty)
        self.Position = self.Aircraft.Position
        self.Velocity = self.Aircraft.Velocity
        def Climb_EOM(State, mass):
            return self.Pitch_EOM(State, mass)
        
        Initial = np.block([self.Position, self.V_infty, self.Pitch])

        Solution = self.Adam_Bashforth_Solve(Initial, Climb_EOM, tmax, delta_t)
        print("Climb phase completed, now loading data")
        z = Solution[:,2]
        self.Position_x = Solution[:,0][z <= Max_z]
        self.Position_y = Solution[:,1][z <= Max_z]
        self.Position_z = Solution[:,2][z <= Max_z]
        self.Velocity_List = Solution[:,3][z <= Max_z]
        self.Pitch_List = Solution[:,4][z <= Max_z]
        self.Time_List = tArr[z <= Max_z]

        self.List_to_Array()
        self.Lift_List = self.Lift_List[z <= Max_z]
        self.Thrust_List = self.Thrust_List[z <= Max_z]
        self.Drag_List = self.Drag_List[z <= Max_z]
        self.Weight_List = self.Weight_List[z <= Max_z]
        self.Percent_List = self.Percent_List[z <= Max_z]
        self.Altitude_List = self.Altitude_List[z <= Max_z]
        Solution = np.block([Solution, tArr.reshape(len(tArr),1)])
        print("Time elapsed during climb: {} min".format(self.Time_List[-1]/60))
        if not np.any(z > Max_z):
            print(z*self.m_to_ft)
            raise Exception("Simulation did not run long enough to reach pattern altitude. Ajust and increase the time length so that the Aircraft can reach pattern altitude.")
        self.Aircraft.Position = np.array([self.Position_x[-1], self.Position_y[-1], self.Position_z[-1]])


    def Pitch_EOM(self, State, mass):

        x, y, z, V_infty, Pitch = State
        self.Aircraft.Altitude = z*self.m_to_ft
        self.Aircraft.V_infty = V_infty
        self.Get_Aircraft_Attr()
        dxdt = V_infty*np.cos(Pitch)
        dydt = 0
        dzdt = V_infty*np.sin(Pitch)
        dv_dt = (self.Thrust-self.Drag-self.Weight*np.sin(Pitch))/mass
        dgamma_dt = (self.Lift-self.Weight*np.cos(Pitch))/(mass*V_infty) - .6*Pitch
        return np.array([dxdt, dydt, dzdt, dv_dt, dgamma_dt])







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