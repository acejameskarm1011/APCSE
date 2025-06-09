#Control
from Aviation import Aviation
import numpy as np
from Emissions import Emissions
from Save_to_Excel import Save_to_Excel
from Save_to_CSV import Save_to_CSV

import pandas as pd

import pickle


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
        print("Using {} Engine".format(self.Aircraft.Engine.__repr__()))
        self.Aircraft_Type = str(self.Aircraft.Engine)
        self.MGTOW_Percent = self.Aircraft.MGTOW_Percent
        self.reset(self.MGTOW_Percent)
        
    def reset(self, MGTOW_Percent):
        self.Aircraft.reset()
        from Control.ImportControl import Take_Off, Climb, Cruise, Descent, Landing
        RPM_Factor = MGTOW_Percent
        if self.Aircraft_Type == "Piston":
            cruise_to_descent = 1600/2306
        elif self.Aircraft_Type == "Electric":
            cruise_to_descent = 0.25
        else:
            raise Exception("Missing an Aircraft Type...")
        
        self.Take_Off = Take_Off(self.Aircraft)
        self.Climb = Climb(self.Aircraft)
        self.Cruise = Cruise(self.Aircraft)
        self.Reserves = Cruise(self.Aircraft)
        self.Descent = Descent(self.Aircraft)
        self.Landing = Landing(self.Aircraft)

        self.TotalEmissions_List = []
        self.Take_Off_groundRoll_List = []
        self.key = -1.05 # Factor used to determine where one phase begins and another one begins
        self.Pattern_Altitude = 750

    def TakeOff_only(self):
        M_1 = self.Aircraft.TotalMass
        E_1 = self.Aircraft.BatteryEnergy
        self.Take_Off.Ground_Roll_Sim_ODESolve()
        M_2 = self.Aircraft.TotalMass
        E_2 = self.Aircraft.BatteryEnergy
        self.TotalEmissions_List.append(Emissions(M_1-M_2, E_1-E_2, str(self.Take_Off)))
        self.Take_Off_groundRoll = self.Take_Off.groundRoll
        Save_to_Excel("Take-Off_Only", self.Take_Off)
        Save_to_CSV(self.Take_Off)


    def TakeOffToClimb(self):
        self.Take_Off.Ground_Roll_Sim_ODESolve()
     
        self.Climb.Pattern_Work_Climb_Solve(tmax=5*60., Pattern_Altitude=self.Pattern_Altitude)

        self.Climb.Time_List += self.Take_Off.Time_List[-1]
        
        print("Gathering Data...")
        Save_to_Excel(self.Aircraft_Type + "_Up_to_Climb", self.Take_Off, self.Climb)
        Save_to_CSV(self.Take_Off, self.Climb)
        

    def Pattern_Cycle(self, iterations = 3):
        """
        This method runs the basic pattern phase with a Take-Off -> Climb -> Cruise -> Descent -> Descent Phase
        """
        self.Phase_Change = []
        for i in range(iterations):
            # with open("test_05-27_0.pickle", 'rb') as file:
            #     self.Aircraft = pickle.load(file)
            self.Aircraft.reset()

            self.Cruise.setDes_RPM(700, 90)


            M_1 = self.Aircraft.TotalMass
            E_1 = self.Aircraft.BatteryEnergy
            self.Take_Off.Ground_Roll_Sim_ODESolve()
            M_2 = self.Aircraft.TotalMass
            E_2 = self.Aircraft.BatteryEnergy
            self.TotalEmissions_List.append(Emissions(M_1-M_2, E_1-E_2, str(self.Take_Off)))
            self.Take_Off_groundRoll = self.Take_Off.groundRoll
            if i > 0:
                self.Take_Off.Time_List += self.Landing.Time_List[-1]
            
            M_1 = self.Aircraft.TotalMass
            E_1 = self.Aircraft.BatteryEnergy
            self.Climb.Pattern_Work_Climb_Solve(tmax=3*60., Pattern_Altitude=self.Pattern_Altitude)
            M_2 = self.Aircraft.TotalMass
            E_2 = self.Aircraft.BatteryEnergy

            # self.TotalEmissions_List.append(Emissions(M_1-M_2, E_1-E_2, str(self.Take_Off)))

            # ClimbPlot(self.Climb)
            self.Climb.Time_List += self.Take_Off.Time_List[-1]
            self.Phase_Change.append(self.Take_Off.Time_List[-1])
            
            M_1 = self.Aircraft.TotalMass
            E_1 = self.Aircraft.BatteryEnergy
            self.Cruise.Downwind_Solve_1(tmax=3*60.)
            M_2 = self.Aircraft.TotalMass
            E_2 = self.Aircraft.BatteryEnergy
            # self.TotalEmissions_List.append(Emissions(M_1-M_2, E_1-E_2, str(self.Cruise)))

            # CruisePlot(self.Cruise)
            
            self.Cruise.Time_List += self.Climb.Time_List[-1]
            self.Phase_Change.append(self.Climb.Time_List[-1])


            M_1 = self.Aircraft.TotalMass
            E_1 = self.Aircraft.BatteryEnergy
            self.Descent.Approach_Descent(tmax=10.*60., printing=True)
            M_2 = self.Aircraft.TotalMass
            E_2 = self.Aircraft.BatteryEnergy
            # self.TotalEmissions_List.append(Emissions(M_1-M_2, E_1-E_2, str(self.Descent)))

            # Descent_Plot(self.Descent)
            self.Descent.Time_List += self.Cruise.Time_List[-1]
            self.Phase_Change.append(self.Cruise.Time_List[-1])


            M_1 = self.Aircraft.TotalMass
            E_1 = self.Aircraft.BatteryEnergy
            self.Landing.Ground_Roll(printing=True)
            M_2 = self.Aircraft.TotalMass
            E_2 = self.Aircraft.BatteryEnergy
            # self.TotalEmissions_List.append(Emissions(M_1-M_2, E_1-E_2, str(self.Landing)))

            # TakeOff_Plot(self.Landing)
            self.Landing.Time_List += self.Descent.Time_List[-1]
            self.Phase_Change.append(self.Descent.Time_List[-1])
            # with open("test_05-27_0.pickle", "wb") as file:
            #     pickle.dump(self.Aircraft, file)
            print("Round {} energy capacity: {} %".format(i+1,round(self.Landing.Percent, 4)))
            if str(self.Aircraft.Engine)=="Electric":
                print("Final energy usage: {} kWh".format(round((self.Aircraft.MaxEnergy - self.Aircraft.BatteryEnergy)*self.J_to_Wh/1000, 4)))
            if str(self.Aircraft.Engine)=="Piston":
                print("Final fuel burn: {} gal".format(round((100-self.Landing.Percent) * self.Aircraft.MaxFuel/self.lbf_to_kg/6/100, 4)))
            print("Gathering Data... round {}...".format(i+1))
            # Save_to_Excel(self.Aircraft_Type + "_Full_Pattern_Mission_{}".format(i+1), self.Take_Off, self.Climb, self.Cruise, self.Descent, self.Landing)
            Save_to_CSV(self.Take_Off, self.Climb, self.Cruise, self.Descent, self.Landing, missionType=self.Aircraft_Type + "-lap-{}".format(i+1))
            self.Take_Off.reset()
            self.Climb.reset()
            self.Cruise.reset()
            self.Descent.reset()
            self.Landing.reset()
    
    def Range_Mission(self, Range, h_cruise, v_cruise, runReserves = True, saveData = False, saveTotalFile = False, printing = False):
        """
        This method runs the basic pattern phase with a Take-Off -> Climb -> Cruise -> Descent -> Descent Phase
        """
        self.Aircraft.Coefficients.missionPhase = "Nominal" # This ensures ground effect is being utilized
        self.Cruise.setDes_RPM(h_cruise,v_cruise)
        self.Phase_Change = []
        M_1 = self.Aircraft.TotalMass
        E_1 = self.Aircraft.BatteryEnergy
        self.Take_Off.Ground_Roll_Sim_ODESolve(printing=printing)
        M_2 = self.Aircraft.TotalMass
        E_2 = self.Aircraft.BatteryEnergy
        self.TotalEmissions_List.append(Emissions(M_1-M_2, E_1-E_2, str(self.Take_Off)))
        self.Take_Off_groundRoll = self.Take_Off.groundRoll

        if self.Take_Off.Percent < 0:
            print("Engine failure during Take-Off")
            # return "Take-Off", False

        M_1 = self.Aircraft.TotalMass
        E_1 = self.Aircraft.BatteryEnergy
        self.Climb.climb_to_altitude(h_cruise, tmax=h_cruise/100*60, delta_t=0.05, printing=printing)
        M_2 = self.Aircraft.TotalMass
        E_2 = self.Aircraft.BatteryEnergy
        # self.TotalEmissions_List.append(Emissions(M_1-M_2, E_1-E_2, str(self.Take_Off)))

        if self.Climb.Percent < 0:
            print("Engine failure during climb")
            # return "Climb", False

        # print("Percent after climb", self.Climb.Percent)
        # exit()
        # ClimbPlot(self.Climb)
        self.Climb.Time_List += self.Take_Off.Time_List[-1]
        self.Phase_Change.append(self.Take_Off.Time_List[-1])
        

        M_1 = self.Aircraft.TotalMass
        E_1 = self.Aircraft.BatteryEnergy
        self.Cruise.cruise_at_range(Range, v_cruise, printing=printing, tmax=6.*60**2)
        M_2 = self.Aircraft.TotalMass
        E_2 = self.Aircraft.BatteryEnergy
        # self.TotalEmissions_List.append(Emissions(M_1-M_2, E_1-E_2, str(self.Cruise)))

        if self.Cruise.Percent < 0:
            print("Engine failure at Cruise")
            # return "Cruise", False
        
        self.Cruise.Time_List += self.Climb.Time_List[-1]
        self.Phase_Change.append(self.Climb.Time_List[-1])


        M_1 = self.Aircraft.TotalMass
        E_1 = self.Aircraft.BatteryEnergy
        self.Descent.Approach_Descent(tmax=h_cruise/100*60, delta_t=0.1, printing=printing)
        M_2 = self.Aircraft.TotalMass
        E_2 = self.Aircraft.BatteryEnergy
        # self.TotalEmissions_List.append(Emissions(M_1-M_2, E_1-E_2, str(self.Descent)))

        # Descent_Plot(self.Descent)
        self.Descent.Time_List += self.Cruise.Time_List[-1]
        self.Phase_Change.append(self.Cruise.Time_List[-1])

        if self.Descent.Percent < 0:
            print("Engine failure at Descent")
            # return "Descent", False
        
        if runReserves:
            M_1 = self.Aircraft.TotalMass
            E_1 = self.Aircraft.BatteryEnergy
            self.Reserves.Reserves(70, printing=printing)
            M_2 = self.Aircraft.TotalMass
            E_2 = self.Aircraft.BatteryEnergy
            # self.TotalEmissions_List.append(Emissions(M_1-M_2, E_1-E_2, str(self.Descent)))

            if self.Reserves.Percent < 0:
                print("Engine failure at reserves")
                # return "Reserves", False
            # Descent_Plot(self.Descent)
            self.Reserves.Time_List += self.Descent.Time_List[-1]
            self.Phase_Change.append(self.Descent.Time_List[-1])
            self.Aircraft.Coefficients.missionPhase = "Nominal"

        M_1 = self.Aircraft.TotalMass
        E_1 = self.Aircraft.BatteryEnergy
        self.Landing.Ground_Roll(printing=printing)
        M_2 = self.Aircraft.TotalMass
        E_2 = self.Aircraft.BatteryEnergy
        # self.TotalEmissions_List.append(Emissions(M_1-M_2, E_1-E_2, str(self.Landing)))

        if self.Landing.Percent < 0:
            print("Engine failure during landing")
            # return "Landing", False
        # TakeOff_Plot(self.Landing)
        if runReserves:
            self.Landing.Time_List += self.Reserves.Time_List[-1]
            self.Phase_Change.append(self.Reserves.Time_List[-1])
        else:
            self.Landing.Time_List += self.Descent.Time_List[-1]
            self.Phase_Change.append(self.Descent.Time_List[-1])
        
        data = {
            "take-off ground roll [ft]" : self.Take_Off_groundRoll,
            "landing ground roll [ft]" : self.Landing.groundRoll,
            "percent" : self.Landing.Percent,
            "range [nmi]" : Range,
            "h_p [ft]" : h_cruise,
            "vInfty [knots]" : v_cruise
        }

        print("Final energy capacity: {} %".format(round(self.Landing.Percent, 3)))
        if str(self.Aircraft.Engine)=="Electric":
            energyUsage = round((self.Aircraft.MaxEnergy - self.Aircraft.BatteryEnergy)*self.J_to_Wh, -1)
            data["energy usage [Wh]"] = energyUsage
            print("Final energy usage: {} WWh".format(energyUsage))
        if str(self.Aircraft.Engine)=="Piston":
            fuelBurn = round((100-self.Landing.Percent)/100 * self.Aircraft.MaxFuel/self.lbf_to_kg/6, 2)
            data["fuel burn [gal]"] = fuelBurn
            print("Final fuel burn: {} gal".format(fuelBurn, 0))


        self.Take_Off.reset()
        self.Climb.reset()
        self.Cruise.reset()
        self.Reserves.reset()
        self.Descent.reset()
        self.Landing.reset()
        self.Aircraft.reset(type = "else")

        if saveTotalFile:
            print("Gathering Data...")
            Save_to_Excel(self.Aircraft_Type + "{}_{}_Full_Pattern_Mission".format(h_cruise,v_cruise), self.Take_Off, self.Climb, self.Cruise, self.Descent, self.Landing)
            Save_to_CSV(self.Take_Off, self.Climb, self.Cruise, self.Descent, self.Landing, missionType=self.Aircraft_Type)
        return data, True

    def Gather_States(self):
        """
        THIS IS AN OUTDATED METHOD, PLEASE USE Save_to_Excel and Save_to_CSV !
        ----------------------------------------------------------------------

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
        if name == "Take_Off_groundRoll":
            self.Take_Off_groundRoll_List.append(value)
        object.__setattr__(self, name, value)


    def __repr__(self) -> str:
          return "Control"