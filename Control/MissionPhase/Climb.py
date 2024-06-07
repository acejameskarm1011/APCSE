import scipy as sp
import numpy as np
from Control.MissionPhase.MissionPhase import MissionPhase

class Climb(MissionPhase): 
    """
    The purpose of the Climb class is to store the important parameters that define the climb phase for an aircraft.
     - V_y is the relative velocity required best rate of climb flight. Example, the PA28-181 requires a Vy of 76 knots.
     - The power setting will be the same as with take-off, FULL POWER
    """
    def __init__(self, AircraftInstance) -> None:
        self.aircraft = AircraftInstance
        
        
    def Pattern_Work_Climb_FE_Solve(self, tmax = 10*60, delta_t = 1e-2, Pattern_Altitude = 10000):
        """
        For pattern altitudes  it is usually about 700-1000 ft above ground level
        """
        self.V_infty = self.aircraft.BestClimbSpeed
        Max_z = Pattern_Altitude*self.ft_to_m
        tArr = np.arange(0, tmax, delta_t)
        tArr = np.append(tArr, tmax + delta_t)
        self.aircraft.V_infty = self.V_infty
        self.Get_Aircraft_Attr()
        self.Pitch = np.arcsin((self.Thrust-self.Drag)/self.Weight)
        self.Position = self.aircraft.Position
        self.Velocity = self.V_infty*np.array([np.cos(self.Pitch), 0, np.sin(self.Pitch)])
        def Climb_EOM(Dot, mass):
            x, y, z, v_x, v_y, v_z  = Dot
            self.Pitch = np.arctan2(v_z, v_x)
            Position = np.array([x, y, z])
            Velocity = np.array([v_x, v_y, v_z])
            self.aircraft.Altitude = z*self.m_to_ft
            self.aircraft.Velocity = Velocity
            self.Get_Aircraft_Attr()
            dxdt = v_x
            dydt = v_y
            dzdt = v_z
            
            dv_xdt = (self.Thrust*np.cos(self.Pitch)-self.Lift*np.sin(self.Pitch)-self.Drag*np.cos(self.Pitch))/mass
            # Constrain the x component in relation to the z component
            # Look at a d(gamma)/dt rotational equation of motion. Check Dr. Elle's disset.


            dv_ydt = 0
            
            dv_zdt = (self.Lift*np.cos(self.Pitch)-self.Weight-self.Drag*np.sin(self.Pitch) + self.Thrust*np.sin(self.Pitch))/mass
            # Leave this one as is

            return np.array([dxdt, dydt, dzdt, dv_xdt, dv_ydt, dv_zdt])
        
        Initial = np.block([self.Position, self.Velocity])

        k = int(tmax/delta_t)
        solution = np.zeros((k+1, len(Initial)), float)
        u_0 = Initial
        self.Save_Data()

        u_1 = self.aircraft.Forward_Euler(Climb_EOM, u_0, delta_t)
        self.Save_Data()

        u_2 = self.aircraft.ab2(Climb_EOM, u_1, u_0, delta_t)
        self.Save_Data()
        solution[0:3,:] = [u_0, u_1, u_2]
        for i in range(2,k):
            u_km2 = solution[i-2, :]
            u_km1 = solution[i-1, :]
            u_k = solution[i, :]
            solution[i+1,:] = self.aircraft.ab3(Climb_EOM, u_k, u_km1, u_km2, delta_t)
            self.Save_Data()
        z = solution[:,2]
        self.Velocity_x = solution[:,3][z <= Max_z]
        self.Velocity_y = solution[:,4][z <= Max_z]
        self.Velocity_z = solution[:,5][z <= Max_z]
        self.Position_x = solution[:,0][z <= Max_z]
        self.Position_y = solution[:,1][z <= Max_z]
        self.Position_z = solution[:,2][z <= Max_z]
        self.Times = tArr[z <= Max_z]

        self.Lift_List = np.array(self.Lift_List)[z <= Max_z]
        self.Thrust_List = np.array(self.Thrust_List)[z <= Max_z]
        self.Drag_List = np.array(self.Drag_List)[z <= Max_z]
        self.Weight_List = np.array(self.Weight_List)[z <= Max_z]
        self.Percent_List = np.array(self.Percent_List)[z <= Max_z]
        self.Altitude_List = np.array(self.Altitude_List)[z <= Max_z]
        solution = np.block([solution, tArr.reshape(len(tArr),1)])
        if not np.any(np.abs(z*self.m_to_ft) > Max_z):
            # print(z*self.m_to_ft)
            pass
            # raise Exception("Simulation did not run long enough to reach pattern altitude. Ajust and increase the time length so that the aircraft can reach pattern altitude.")
        self.aircraft.Velocity = np.array([self.Velocity_x[-1], self.Velocity_y[-1], self.Velocity_z[-1]])
        self.aircraft.Position = np.array([self.Position_x[-1], self.Position_y[-1], self.Position_z[-1]])

    def Get_Aircraft_Attr(self):
        super().Get_Aircraft_Attr()
        # self.Pitch = np.arccos((self.Lift)/self.Weight)
        self.Altitude = self.aircraft.Altitude


    def Save_Data(self):
        super().Save_Data()
        if not hasattr(self, "Altitude_List"):
            self.Altitude_List = [self.Altitude]
        else:
            self.Altitude_List.append(self.Altitude)

        if not hasattr(self, "Pitch_List"):
            self.Pitch_List = [self.Pitch]
        else:
            self.Pitch_List.append(self.Pitch)
        # include pitch