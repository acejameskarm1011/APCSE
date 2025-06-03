from math import copysign
import scipy as sp
import numpy as np
from Control.MissionPhase.MissionPhase import MissionPhase

class Climb(MissionPhase): 
    """
    The purpose of the Climb class is to store the important parameters that define the climb phase for an Aircraft.
     - V_y is the relative velocity required best rate of climb flight. Example, the PA28-181 requires a Vy of 76 knots.
     - The power setting will be the same as with take-off, FULL POWER
    """ 
    def Pattern_Work_Climb_Solve(self, tmax = 200, delta_t = 1e-2, Pattern_Altitude = 700):
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
        
        self.Aircraft.Climb = None
        self.RPM = self.Aircraft.Engine.RPM
        self.V_infty = self.Aircraft.V_infty
        self.z_max = Pattern_Altitude*self.ft_to_m
        Max_z = self.z_max
        tArr = np.arange(0, tmax, delta_t)
        tArr = np.append(tArr, tmax + delta_t)
        self.Get_Aircraft_Attr()
        self.Pitch = 0
        self.Position = self.Aircraft.Position
        alphaInitial = self.alpha

        ArcherAircraft = self.Aircraft
        ArcherAircraft.V_infty = 76 * self.knots_to_mps
        flightAngle = 11/180*np.pi
        # if str(self.Aircraft.Engine) == "Electric":
        #     flightAngle = 7.5/180*np.pi
        i=0
        while i < 3:
            ArcherAircraft.Set_Lift()
            # print(flightAngle/np.pi*180)
            flightAngle = np.arcsin((ArcherAircraft.Thrust*np.cos(ArcherAircraft.alpha)-ArcherAircraft.Drag)/ArcherAircraft.Weight)
            ArcherAircraft.Pitch = flightAngle
            i+=1
        self.trimForces = ArcherAircraft.Lift + ArcherAircraft.Thrust*np.cos(ArcherAircraft.alpha)-ArcherAircraft.Weight*np.cos(flightAngle)
        self.idealPitch = flightAngle
        self.idealAlpha = ArcherAircraft.alpha
        # print(ArcherAircraft.alpha/np.pi*180)
        self.stopPitch = 0
        self.set = False

        self.Aircraft.Pitch = self.Pitch
        self.Aircraft.alpha = alphaInitial
        self.Aircraft.Position = self.Position
        # print("Ideal pitch angle", int(self.idealPitch/np.pi*180))


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
        print("Time elapsed during climb: {} min".format(round(self.Time_List[-1]/60, 3)))
        if not np.any(z > Max_z):
            from Plotting.Plotting import ClimbPlot
            ClimbPlot(self, title = "Climb Failed")
            raise Exception("Simulation did not run long enough to reach pattern altitude. Ajust and increase the time length so that the Aircraft can reach pattern altitude.")
        self.Aircraft.Position = np.array([self.Position_x[-1], self.Position_y[-1], self.Position_z[-1]])
    
    
    def climb_to_altitude(self, h_f, tmax = 200, delta_t = 1e-2, printing = False):
        """
        Paramters
        ---------
        h_f : int/float
            Final altitude the aircraft is climbing towards
        tmax : int/float
            Maximum time run of simulation in [s]
        delta_t : int/float
            Time step that will determine the step length in the time array
        Pattern_Altitude : int/float [ft]
            Desired altitude to fly to
        """
        if printing:
            print("Climb Phase Starting")
        
        self.Aircraft.Climb = None
        self.RPM = self.Aircraft.Engine.RPM
        self.V_infty = self.Aircraft.V_infty
        self.z_max = h_f*self.ft_to_m
        Max_z = self.z_max
        tArr = np.arange(0, tmax, delta_t)
        tArr = np.append(tArr, tmax + delta_t)
        self.Get_Aircraft_Attr()
        self.Pitch = 0
        self.Position = self.Aircraft.Position
        alphaInitial = self.alpha

        ArcherAircraft = self.Aircraft
        ArcherAircraft.V_infty = 76 * self.knots_to_mps
        flightAngle = 11/180*np.pi

        i=0
        while i < 3:
            ArcherAircraft.Set_Lift()
            # print(flightAngle/np.pi*180)
            flightAngle = np.arcsin((ArcherAircraft.Thrust*np.cos(ArcherAircraft.alpha)-ArcherAircraft.Drag)/ArcherAircraft.Weight)
            ArcherAircraft.Pitch = flightAngle
            i+=1
        self.trimForces = ArcherAircraft.Lift + ArcherAircraft.Thrust*np.cos(ArcherAircraft.alpha)-ArcherAircraft.Weight*np.cos(flightAngle)
        self.idealPitch = flightAngle
        self.idealAlpha = ArcherAircraft.alpha
        # print(ArcherAircraft.alpha/np.pi*180)
        self.stopPitch = 0
        self.set = False

        self.Aircraft.Pitch = self.Pitch
        self.Aircraft.alpha = alphaInitial
        self.Aircraft.Position = self.Position
        # print("Ideal pitch angle", int(self.idealPitch/np.pi*180))


        Initial = np.block([self.Position, self.V_infty, self.Pitch])

        Solution, tArr = self.Adam_Bashforth_Solve(Initial, self.Pitch_EOM, tmax, delta_t)
        if printing:
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
        if printing:
            print("Time elapsed during climb to {} ft: {} min".format(round(h_f), round(self.Time_List[-1]/60, 3)))
        if not np.any(z > Max_z):
            from Plotting.Plotting import ClimbPlot
            ClimbPlot(self, title = "Climb Failed")
            raise Exception("Simulation did not run long enough to reach pattern altitude. Ajust and increase the time length so that the Aircraft can reach pattern altitude.")
        self.Aircraft.Position = np.array([self.Position_x[-1], self.Position_y[-1], self.Position_z[-1]])


    def Pitch_EOM(self, State, mass):
        x, y, z, V_infty, Pitch = State
        self.z = z
        self.Aircraft.Position = np.array([x, y, z])
        self.V_infty = V_infty
        self.Aircraft.Pitch = Pitch
        self.Get_Aircraft_Attr(self.set)

        dxdt = V_infty*np.cos(Pitch)
        dydt = 0
        dzdt = V_infty*np.sin(Pitch)
        V_des = 76 * self.knots_to_mps



        dv_dt = (self.Thrust*np.cos(self.alpha)-self.Drag-self.Weight*np.sin(Pitch))/mass
        dgamma_dt = (self.Lift-self.Weight*np.cos(Pitch)+self.Thrust*np.sin(self.alpha))/(mass*V_infty) # Actual 

        limitingFactor = 0.25
        limitingFactor = 0.5
        limitingFactor = 0.2
        
        if self.stopPitch:
            limitingFactor = .4
        dgamma_dt = limitingFactor*dgamma_dt # Limited version 


        self.gForce = np.sqrt((dgamma_dt*V_infty)**2)/self.g

 
        self.set = False
        if dgamma_dt < 0 and Pitch < 0:
            print("Why is dgamma_dt less than zero")
            print("d gamma / dt", dgamma_dt)
            raise Exception("An error occurred in climb")
        elif (Pitch > self.idealPitch*0.85 and dgamma_dt > 0):
            self.stopPitch = True
            self.Aircraft.alpha = self.idealAlpha
            dgamma_dt = 0
            # self.set = True
        # elif np.abs(V_des - V_infty) > 2*self.knots_to_mps:
        #     dgamma_dt -= (V_des - V_infty)/10
        return np.array([dxdt, dydt, dzdt, dv_dt, dgamma_dt])


    def Condition(self):
        Bool = self.z <= self.z_max
        return Bool


    def Get_Aircraft_Attr(self, set = False):
        super().Get_Aircraft_Attr(set)
        self.Altitude = self.Aircraft.Altitude

    def List_to_Array(self):
        super().List_to_Array()
        self.Altitude_List = np.array(self.Altitude_List)
        self.Alpha_List = np.array(self.Alpha_List)


    def Save_Data(self):
        super().Save_Data()
        if not hasattr(self, "Altitude_List"):
            self.Altitude_List = [self.Altitude]
        else:
            self.Altitude_List.append(self.Altitude)
        if not hasattr(self, "Alpha_List"):
            self.Alpha_List = [self.Aircraft.alpha]
        else:
            self.Alpha_List.append(self.Aircraft.alpha)

    def reset(self):
        super().reset()
        delattr(self, "Alpha_List")
        delattr(self, "Altitude_List")

    def __repr__(self) -> str:
          return "Climb"
    
    def __dict__(self):
        dict = super().__dict__()
        dict["Velocity [knots]"] = self.Velocity_List * self.mps_to_knots
        dict["Altitude [ft]"] = self.Altitude_List
        dict["Range [nmi]"] = self.Position_x * self.m_to_nmi
        dict["RPM [rev/min]"] = self.MaxRPM
        dict["Pitch [deg]"] = self.Pitch_List / np.pi * 180
        dict["AOA [deg]"] = self.Alpha_List / np.pi * 180
        return dict