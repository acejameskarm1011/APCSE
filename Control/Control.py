#Control
from Aviation import Aviation
import numpy as np
from Plotting.Plotting import TakeOff_Plot

class Control(Aviation):
    """
    This class handles and operates on the Aircraft class.

    Parameters
    ----------
    AircraftInstance : Aircraft
        Must input an instance of an Aircraft so that the control class will be able to employ methods that will update the 
        characteristics of the Aircraft.
    """
    def __init__(self, AircraftInstance) -> None:
        from Control.ImportControl import Take_Off, Climb, Cruise, Descent, Landing
        self.Aircraft = AircraftInstance
        self.Take_Off = Take_Off(self.Aircraft)
        self.Climb = Climb(self.Aircraft)
        self.Cruise = Cruise(self.Aircraft)
        self.Descent = Descent(self.Aircraft)
        self.Landing = Landing(self.Aircraft)
        
        self.key = -1.05 # Factor used to determine where one phase begins and another one begins



    def Pattern_Cycle(self):
        """
        This method runs the basic pattern phase with a Take-Off -> Climb -> Cruise -> Descent -> Descent Phase
        """
        self.Take_Off.Ground_Roll_Sim_ODESolve()
        self.Climb.Pattern_Work_Climb_Solve(tmax=80)
        self.Climb.Time_List += self.Take_Off.Time_List[-1]

        self.Cruise.Downwind_Solve_1()
        self.Cruise.Time_List += self.Climb.Time_List[-1]

        self.Descent.Approach_Descent()
        self.Descent.Time_List += self.Cruise.Time_List[-1]
        
        self.Landing.Ground_Roll()
        self.Landing.Time_List += self.Descent.Time_List[-1]



        
        print("Gathering Data...")
        self.Gather_States()
        self.Gather_Aerodynamics()
        self.Gather_EnginePars()

    def Gather_States(self):
        """
        Gather's the aircraft's State-Data into arrays for the entire mission.
        To obtain the data, run this function and call the attributes:

        * Control . . . Time_Arr [s]
        * Control . . . Position_x_Arr [m]
        * Control . . . Position_y_Arr [m]
        * Control . . . Position_z_Arr [m]
        * Control . . . Velocity_Arr [m/s]
        * Control . . . Pitch_Arr [rad]

        """
        from Control.ImportControl import Take_Off, Cruise, Landing
        State_List = ["Time", "Position_x", "Position_y", "Position_z", "Velocity", "Pitch"]
        Phase_List = [self.Take_Off, self.Climb, self.Cruise, self.Descent, self.Landing]
        for State in State_List:
            input = []
            for j, Phase in enumerate(Phase_List):
                name = State + "_List"
                if State[:-2] == "Position":
                    name = State
                if State == "Pitch":
                    if isinstance(Phase, (Take_Off, Cruise, Landing)):
                        name = "Pitch"
                        input.append(getattr(Phase, name)*np.ones(Phase.Time_List.shape))
                        # input.append(self.key)
                    else:
                        input.append(getattr(Phase, name))
                        # input.append(self.key)
                else:

                    input.append(getattr(Phase, name))
                    # input.append(self.key)
            self.__setattr__(State + "_Arr", np.block(input)[:-1])

    def Gather_Aerodynamics(self):
        """
        Gather's the aircraft's Aerodynamic-Data into arrays for the entire mission.
        To obtain the data, run this function and call the attributes:

        * Control . . . Lift_Arr
        * Control . . . Thrust_Arr
        * Control . . . Weight_Arr
        * Control . . . Drag_Arr

        """
        Aero_List = ["Lift", "Thrust", "Weight", "Drag"]
        Phase_List = [self.Take_Off, self.Climb, self.Cruise, self.Descent, self.Landing]
        for Aero in Aero_List:
            input = []
            for Phase in Phase_List:
                input.append(getattr(Phase, Aero + "_List"))
                # input.append(self.key)
            self.__setattr__(Aero + "_Arr", np.block(input)[:-1])
        
    def Gather_EnginePars(self):
        """
        Gather's the aircraft's Engine-Data into arrays for the entire mission.
        To obtain the data, run this function and call the attributes:

        * Control . . . RPM_Arr [rev/min]
        * Control . . . Percent_Arr [%]

        """
        from Control.ImportControl import Take_Off, Climb, Cruise, Descent, Landing
        Para_List = ["Percent", "RPM"]
        Phase_List = [self.Take_Off, self.Climb, self.Cruise, self.Descent, self.Landing]
        for Para in Para_List:
            input = []
            for Phase in Phase_List:
                name = Para + "_List"
                if Para == "RPM":
                    if not isinstance(Phase, (Cruise, Descent)):
                        name = "RPM"
                        input.append(getattr(Phase, name)*np.ones(Phase.Time_List.shape))
                        # input.append(self.key)
                    else:
                        input.append(getattr(Phase, Para + "_List"))
                        # input.append(self.key)
                else:
                    input.append(getattr(Phase, Para + "_List"))
                    # input.append(self.key)
            self.__setattr__(Para + "_Arr", np.block(input)[:-1])
    