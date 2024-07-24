#Control
from Aviation import Aviation
import numpy as np
from Plotting.Plotting import TakeOff_Plot
from Emissions import Emissions

class Control(Aviation):
    """
    This class handles and operates on the Aircraft class.

    Parameters
    ----------
    AircraftInstance : Aircraft
        Must input an instance of an Aircraft so that the control class will be able to employ methods that will update the 
        characteristics of the Aircraft.
    """
    def __init__(self, AircraftInstance, ) -> None:
        from Control.ImportControl import Take_Off, Climb, Cruise, Descent, Landing
        self.Aircraft = AircraftInstance
        self.MGTOW_Percent = self.Aircraft.MGTOW_Percent
        self.Aircraft_Type = str(self.Aircraft.Engine)

        RPM_Factor = self.Aircraft.MGTOW_Percent
        if self.Aircraft_Type == "Conventional":
            RPM_des_Cruise = 2306*RPM_Factor # Found using quasi - cruise
            RPM_des_Descent = 1600*RPM_Factor
        elif self.Aircraft_Type == "Electric":
            RPM_des_Cruise = 1500*RPM_Factor # Found using quasi - cruise
            RPM_des_Descent = 1000*RPM_Factor
        else:
            raise Exception("Missing an Aircraft Type...")
        
        self.Take_Off = Take_Off(self.Aircraft)
        self.Climb = Climb(self.Aircraft)
        self.Cruise = Cruise(self.Aircraft, RPM_des_Cruise)
        self.Descent = Descent(self.Aircraft, RPM_des_Descent)
        self.Landing = Landing(self.Aircraft)

        self.TotalEmissions_List = []
        self.Take_Off_GroundRoll_List = []
        
        
        self.key = -1.05 # Factor used to determine where one phase begins and another one begins

    def reset(self, MGTOW_Percent):
        from Control.ImportControl import Take_Off, Climb, Cruise, Descent, Landing
        self.Aircraft.reset()
        RPM_Factor = MGTOW_Percent
        if self.Aircraft_Type == "Conventional":
            RPM_des_Cruise = 2306*RPM_Factor # Found using quasi - cruise
            RPM_des_Descent = 1600*RPM_Factor
        elif self.Aircraft_Type == "Electric":
            RPM_des_Cruise = 1500*RPM_Factor # Found using quasi - cruise
            RPM_des_Descent = 1000*RPM_Factor
        else:
            raise Exception("Missing an Aircraft Type...")
        
        self.Take_Off = Take_Off(self.Aircraft)
        self.Climb = Climb(self.Aircraft)
        self.Cruise = Cruise(self.Aircraft, RPM_des_Cruise)
        self.Descent = Descent(self.Aircraft, RPM_des_Descent)
        self.Landing = Landing(self.Aircraft)

        self.TotalEmissions_List = []
        self.Take_Off_GroundRoll_List = []




    def Pattern_Cycle(self):
        """
        This method runs the basic pattern phase with a Take-Off -> Climb -> Cruise -> Descent -> Descent Phase
        """
        from Plotting.Plotting import ClimbPlot, CruisePlot, Descent_Plot, TakeOff_Plot
        self.Phase_Change = []
        M_1 = self.Aircraft.TotalMass
        E_1 = self.Aircraft.BatteryEnergy
        self.Take_Off.Ground_Roll_Sim_ODESolve()
        M_2 = self.Aircraft.TotalMass
        E_2 = self.Aircraft.BatteryEnergy
        self.TotalEmissions_List.append(Emissions(M_1-M_2, E_1-E_2, str(self.Take_Off)))
        self.Take_Off_GroundRoll = self.Take_Off.GroundRoll
        # TakeOff_Plot(self.Take_Off)

        M_1 = self.Aircraft.TotalMass
        E_1 = self.Aircraft.BatteryEnergy
        self.Climb.Pattern_Work_Climb_Solve(tmax=3*60.)
        M_2 = self.Aircraft.TotalMass
        E_2 = self.Aircraft.BatteryEnergy
        self.TotalEmissions_List.append(Emissions(M_1-M_2, E_1-E_2, str(self.Take_Off)))

        # ClimbPlot(self.Climb)
        self.Climb.Time_List += self.Take_Off.Time_List[-1]
        self.Phase_Change.append(self.Take_Off.Time_List[-1])
        

        M_1 = self.Aircraft.TotalMass
        E_1 = self.Aircraft.BatteryEnergy
        self.Cruise.Downwind_Solve_1(tmax=2.*60.)
        M_2 = self.Aircraft.TotalMass
        E_2 = self.Aircraft.BatteryEnergy
        self.TotalEmissions_List.append(Emissions(M_1-M_2, E_1-E_2, str(self.Cruise)))

        # CruisePlot(self.Cruise)
        self.Cruise.Time_List += self.Climb.Time_List[-1]
        self.Phase_Change.append(self.Climb.Time_List[-1])


        M_1 = self.Aircraft.TotalMass
        E_1 = self.Aircraft.BatteryEnergy
        self.Descent.Approach_Descent(tmax=1.2*60.)
        M_2 = self.Aircraft.TotalMass
        E_2 = self.Aircraft.BatteryEnergy
        self.TotalEmissions_List.append(Emissions(M_1-M_2, E_1-E_2, str(self.Descent)))

        # Descent_Plot(self.Descent)
        self.Descent.Time_List += self.Cruise.Time_List[-1]
        self.Phase_Change.append(self.Cruise.Time_List[-1])


        M_1 = self.Aircraft.TotalMass
        E_1 = self.Aircraft.BatteryEnergy
        self.Landing.Ground_Roll()
        M_2 = self.Aircraft.TotalMass
        E_2 = self.Aircraft.BatteryEnergy
        self.TotalEmissions_List.append(Emissions(M_1-M_2, E_1-E_2, str(self.Landing)))

        # TakeOff_Plot(self.Landing)
        self.Landing.Time_List += self.Descent.Time_List[-1]
        self.Phase_Change.append(self.Descent.Time_List[-1])
        
        print("Gathering Data...")
        self.Gather_States()
        self.Gather_Aerodynamics()
        self.Gather_EnginePars()
        self.Gather_Emissions()


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

    def Gather_Emissions(self):
        self.TotalEmissions_Arr = np.array(self.TotalEmissions_List)
        self.TotalEmissions = np.sum(self.TotalEmissions_Arr, axis=0)
        self.Total_CO2, self.Total_CH4, self.Total_N2O, self.Total_Pb = self.TotalEmissions

    def __setattr__(self, name, value):
        if name == "Take_Off_GroundRoll":
            self.Take_Off_GroundRoll_List.append(value)
        object.__setattr__(self, name, value)


    def __repr__(self) -> str:
          return "Control"