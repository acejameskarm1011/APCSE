from Control.Control import Control
from Propulsion.Engine import ElectricEngineTest, EMRAX_268_Engine
import numpy as np
class MissionPhase(Control):
    weather = "Good"
    mu_f = 0.04 # rolling
    mu_br = 0.4 # Braking
    def __init__(self, AircraftInstance) -> None:
        self.Aircraft = AircraftInstance
        self.MaxRPM = self.Aircraft.Engine.MaxRPM
        self.Time_List = []

    def Get_Aircraft_Attr(self, set=False):
        """
        Get all needed Aircraft attributes for a desired mission phase.
        """
        if set:
            self.Aircraft.Set_Lift()
        else:
            self.Aircraft.Aircraft_Forces()
        self.Lift = self.Aircraft.Lift
        self.Drag = self.Aircraft.Drag
        self.Weight = self.Aircraft.Weight
        self.Thrust = self.Aircraft.Thrust
        self.alpha = self.Aircraft.alpha
        self.g = self.Aircraft.g
        self.Power = self.Aircraft.Engine.Power
        
        if str(self.Aircraft.Engine)=="Electric":
            self.Percent = 100*self.Aircraft.BatteryPercent
        else:
            self.Percent = 100*self.Aircraft.FuelPercent
            
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
        tArr = np.arange(0, tmax + delta_t, delta_t)

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
            if not self.Condition():
                Solution = Solution[:i+1, :]
                tArr = tArr[:i+1]
                break
            u_km2 = Solution[i-2, :]
            u_km1 = Solution[i-1, :]
            u_k = Solution[i, :]
            Solution[i+1,:] = self.Aircraft.ab3(func, u_k, u_km1, u_km2, delta_t)
            self.Save_Data()
        return Solution, tArr
    def Condition(self):
        raise Exception("A condition must be implemented for the class: {}".format(self))
        exit()
        return True    

    def List_to_Array(self):
        self.Lift_List = np.array(self.Lift_List)
        self.Thrust_List = np.array(self.Thrust_List)
        self.Drag_List = np.array(self.Drag_List)
        self.Weight_List = np.array(self.Weight_List)
        self.Percent_List = np.array(self.Percent_List)
        self.Power_List = np.array(self.Power_List)

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

        if not hasattr(self, "Power_List"):
            self.Power_List = [self.Power]
        else:
            self.Power_List.append(self.Power)

    def __setattr__(self, name, value) -> None:
        if name == "RPM":
            max = self.MaxRPM
            min = 1
            if value > max:
                value = max
            elif value < min:
                value = min
        object.__setattr__(self, name, value)
        if name == "RPM":
            self.Aircraft.Set_RPM(self.RPM)
        if name == "V_infty":
            self.Aircraft.V_infty = value
        if name == "Altitude":
            self.Aircraft.Altitude = value

    def reset(self):
        delattr(self, "Lift_List")
        delattr(self, "Thrust_List")
        delattr(self, "Drag_List")
        delattr(self, "Weight_List")
        delattr(self, "Percent_List")
        delattr(self, "Power_List")
    def __repr__(self) -> str:
          return "MissionPhase"
    def __dict__(self):
        return {
            "Time [s]" : self.Time_List,
            "Thrust [lb]" : self.Thrust_List*self.N_to_lbf,
            "Lift [lb]" : self.Lift_List*self.N_to_lbf,
            "Drag [lb]" : self.Drag_List*self.N_to_lbf,
            "Power [hp]" : self.Power_List, 
            "Weight [lb]" : self.Weight_List*self.N_to_lbf,
            "Percent [%]" : self.Percent_List,
        }

class subphase(MissionPhase):
    pass
