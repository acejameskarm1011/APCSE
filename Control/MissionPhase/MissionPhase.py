from Control.Control import Control
from Propulsion.Engine import ElectricEngineTest
import numpy as np
class MissionPhase(Control):
    weather = "Good"
    def __init__(self, AircraftInstance) -> None:
        self.Aircraft = AircraftInstance
        self.MaxRPM = self.Aircraft.Engine.MaxRPM

    def Get_Aircraft_Attr(self):
        """
        Get all needed Aircraft attributes for a desired mission phase.
        """
        self.Aircraft.Aircraft_Forces()
        self.Lift = self.Aircraft.Lift
        self.Drag = self.Aircraft.Drag
        self.Weight = self.Aircraft.Weight
        self.Thrust = self.Aircraft.Thrust
        
        if isinstance(self.Aircraft.Engine, ElectricEngineTest):
            self.Percent = 100*self.Aircraft.BatteryRatio
        else:
            self.Percent = 100*self.Aircraft.FuelRatio
            
    def Adam_Bashforth_Solve(self, Initial, func, tmax, delta_t):
        """
        Utilizing the Adam Bashforth three step method, we are able to evaluate the Aircraft's performance with 
        significant accuracy for time steps greater than forward Euler.

        Parameters
        ----------
        Initial : np.ndarray
            The vector of the initial conditions for a set of linear ODEs

        func : Function
            The function that representes the time rate of change for the linear system. It also must update attributes of the Aircraft during the mission
        
        tmax : int/float
            The total amount of time that the solver will run for
        
        delta_t : int/float
            Time step value that the system will progress through

        Returns
        -------
        Solution : np.ndarray
            The entire solution for the set of equations
        """
        k = int(tmax/delta_t)
        Solution = np.zeros((k+1, len(Initial)), float)
        u_0 = Initial
        self.Save_Data()

        u_1 = self.Aircraft.Forward_Euler(func, u_0, delta_t)
        self.Save_Data()

        u_2 = self.Aircraft.ab2(func, u_1, u_0, delta_t)
        self.Save_Data()
        Solution[0:3,:] = [u_0, u_1, u_2]
        for i in range(2,k):
            u_km2 = Solution[i-2, :]
            u_km1 = Solution[i-1, :]
            u_k = Solution[i, :]
            Solution[i+1,:] = self.Aircraft.ab3(func, u_k, u_km1, u_km2, delta_t)
            self.Save_Data()
        return Solution
    def List_to_Array(self):
        self.Lift_List = np.array(self.Lift_List)
        self.Thrust_List = np.array(self.Thrust_List)
        self.Drag_List = np.array(self.Drag_List)
        self.Weight_List = np.array(self.Weight_List)
        self.Percent_List = np.array(self.Percent_List)

    @classmethod
    def changeweather(cls, text):
        cls.weather = text
    def Save_Data(self):
        if not hasattr(self, "Lift_List"):
            self.Lift_List = [self.Lift]
        else:
            self.Lift_List.append(self.Lift)

        if not hasattr(self, "Thrust_List"):
            self.Thrust_List = [self.Thrust]
        else:
            self.Thrust_List.append(self.Thrust)

        if not hasattr(self, "Drag_List"):
            self.Drag_List = [self.Drag]
        else:
            self.Drag_List.append(self.Drag)

        if not hasattr(self, "Weight_List"):
            self.Weight_List = [self.Weight]
        else:     
            self.Weight_List.append(self.Weight)
        
        if not hasattr(self, "Percent_List"):
            self.Percent_List = [self.Percent]
        else:
            self.Percent_List.append(self.Percent)

    def __setattr__(self, name, value) -> None:
        if name == "RPM":
            max = self.MaxRPM
            min = 250
            if value > max:
                value = max
            elif value < min:
                value = min
        object.__setattr__(self, name, value)
        if name == "RPM":
            self.Aircraft.Set_RPM(self.RPM)


class subphase(MissionPhase):
    pass