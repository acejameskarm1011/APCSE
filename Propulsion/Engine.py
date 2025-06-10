import os
from AtmosphereFunction import AtmosphereFunctionSI
from Aviation import Aviation
import scipy as sp
import scipy.linalg as la
from scipy.interpolate import make_smoothing_spline
import numpy as np
import pandas as pd



class Powerplant(Aviation):
    hp_to_watt = 745.7

class Propeller():
    """
    Stores the attributes of the propeller

    Parameters
    ----------
    Make : string
        Maker of the propeller
    Model : string
        Specific Model of the propeller
    Diameter : float/int
        Diameter of the propeller in inches
    Spinner_Diameter : float/int
        Diamter of the spinner or maximum obstruction in inches
    """
    def __init__(self, Make, Model, Diameter, Spinner_Diameter) -> None:
        self.Make = Make
        self.Model = Model
        self.Diameter = Diameter * sp.constants.inch
        self.Spinner_Diameter = Spinner_Diameter * sp.constants.inch
    def Get_Area_and_AreaEfficiency(self):
        """
        Function that takes in no arguments and returns both the area and the area efficiency
        Returns
        ------
        A_2 : float
            Area of the propeller "disc"
        eta_A : float
            Efficiency ratio of the difference in area normalized by propeller area

        Notes: This is NOT the area of the actual propeller, but it is the area of the control section of airflow through the propeller. 
        This is useful in the Rankine-Foude Momentum Theory framework so that we can find the static thrust for the engine and propeller.
        """
        A_2 = self.Diameter**2*np.pi/4
        A_spin = self.Spinner_Diameter**2*np.pi/4
        eta_A = 1-A_spin/A_2
        return A_2, eta_A






class PistonEngine(Powerplant):
    """
    This class is not completeled. Current goal is to use this as the basis for aquiring the trust, power and fuel drain from the aircraft.

    Parameters
    ---------
    Name : string
        Name of the aircraft or engine of interest
    MaxPower : int/float
        Rated power of the engine in terms of [hp]
    """
    def __init__(self, Name, AircraftPropeller, MaxBreakHorsePower = 180) -> None:

        # Below is tick to check if any methods are being called on too many times
        self.tick = 0
        self.RPM_tick = 0
        self.Gal_Hr_List = []

        self.Name = Name + ": Piston Engine"
        # Since this is a test class, we will use the general "Name" to keep track of what the class is
        self.Propeller = AircraftPropeller
        # Propeller information is different between props, so we have a class for those properties
        self.MaxBreakHorsePower = MaxBreakHorsePower
        # Units in Horse Power
        self.eta = 0.93
        # self.eta = 0.9
        # Current Model for the engine to propeller efficiency is unknown
        self.BreakHorsePower = self.MaxBreakHorsePower
        # Power of the engine in terms of horsepower
        self.MaxBreakPower = self.MaxBreakHorsePower * self.hp_to_watt 
        # We define the engine's max break power to be in terms of Watts so fundementals equations can be applied
        self.Power = self.MaxBreakPower * self.eta
        self.MaxPower = self.Power
        self.PowerRating = self.BreakHorsePower/self.MaxBreakHorsePower
        self.MaxPower_SL = self.MaxPower
        # Current acutual power the aircraft is experiencing

        self.MaxRPM = 2700
        self.Throttle = 1

        self.altVoltage = 28   # Piper Archer III alternator draws energy from here
        self.altAmpere = 70   # Piper Archer III alternator draws energy from here


        self.Altitude = 0
        # Engine requires the atmospheric information
        self.Temperature_SL = self.Temperature
        # Setting Sea Level Parameters
        self.RPM = self.MaxRPM

        bore = 5.125 * sp.constants.inch
        stroke = 4.375 * sp.constants.inch
        N_cylinders = 4
        Volume = np.pi/4*N_cylinders*(bore**2*stroke) # Total Volume
        compression_ratio = 8.5 # Useable volume to nonuseable is 8.5:1
        self.V_displacement = Volume * (compression_ratio-1)/(compression_ratio)
        self.Mixture = "RICH"
        self.Fuel_Density = 6*self.lbf_to_kg/sp.constants.gallon  # kg/m^3
                
        Number = 5000
        self.PArr = np.linspace(0, self.MaxPower, Number)

    def Thrust_Static(self):
        """
        Using the engine's current propeller, power setting, and altitude this method returns the static thrust. This method requires no inputs.

        Returns
        -------
        Thrust_Static : float
            The current thrust of the engine when the velocity is zero.
        """
        if self.rho < 0:
            raise ValueError("An invalid value of {} was found for the air density".format(self.rho))
        self.Atmosphere_attr()
        A_2, eta_A = self.Propeller.Get_Area_and_AreaEfficiency()
        # Get the disk area of the propeller, and get the efficiency of the area that accounts for blockage effects
        Thrust_Static = 0.85*self.Power**(2/3)*(2*self.rho*A_2)**(1/3)*eta_A
        # Using Disk Momentum theory, we get the thrust for a stationary aircraft
        return Thrust_Static

    def Get_Thrust(self, Velocity_infty, Velocity_Max):
        """
        Utilizing a quadradic interpolation of the 
        """
        V = Velocity_infty
        if Velocity_infty > Velocity_Max:
            self.Thrust = self.Power / Velocity_infty
            return self.Thrust
        Thrust_Max = self.Power/Velocity_Max
        Thrust_Static = self.Thrust_Static()
        self.Thrust = Thrust_Static + (3*Thrust_Max-2*Thrust_Static)/Velocity_Max*V + (Thrust_Static-2*Thrust_Max)/Velocity_Max**2*V**2
        return self.Thrust


    def getR_m(self):
        #####################################################################
        # Testing for engine performance
        tau_arr = np.array([0, 2265, 2405, 2515, 2700])/2700
        rating_arr = np.array([0, 55, 65, 75, 100])/100
        R_m_func = make_smoothing_spline(tau_arr, rating_arr, lam=0)
        return R_m_func(self.Throttle)
        import matplotlib.pyplot as plt
        
        tau_arr_new = np.linspace(0,1,100)
        plt.close()
        plt.figure(figsize=(12,8))
        plt.plot(tau_arr_new*2700, R_m_func(tau_arr_new)*100, label = "Spline model")
        plt.plot(tau_arr*2700, rating_arr*100, "r+", label = "Real data [POH]")
        plt.xlabel(r"RPM")
        plt.ylabel(r"Lycoming Power Rating [\%]")
        plt.savefig("RPM-Power.png")
        plt.legend()
        plt.show()
        exit()
        
        #####################################################################
    def Get_Power(self):
        """
        This returns the current power output [W] of the engine based on altitude and RPM setting

        Returns
        -------
        self.Power : float
            Current power output of the propeller [W]
        """
        # sigma = self.rho/self.rho_SL
        sigma = (1-0.0000068756*self.Altitude)**(4.2561)

        input = self.Throttle
        
        ######################################################################################     
        # This is old code, found to overestimate the power output during flight - needs tailoring   
        R_m = 0.6*np.sin(self.Throttle**6.5*np.pi/2) + 0.4 # the 0.4 has been validated to be valid from a paper about emissions (WTF) 
        R_m = 0.9*np.sin(self.Throttle**6.5*np.pi/2) + 0.1 # This is now in progress again
        ######################################################################################
        R_m = self.getR_m()
   

        if np.isclose(1.0, self.Throttle):
            R_m = 0.999999
        
        self.Power_SL = self.MaxPower_SL * R_m

        self.Power = self.Power_SL * R_m * sigma # Simple Altitude Model
        self.Power = self.Power_SL * R_m * (sigma-0.117)/0.883 # Gagg and Farrar Model
        # self.Power = self.MaxPower_SL*(R_m*(sigma-R_m**(0.8097))+(R_m**(0.8097)-0.117)/0.883*(1-sigma))/(1-R_m**(0.8097)) # Petty Equation
        return self.Power

    def Get_FuelConsumption(self):
        """
        The fuel consumption is derived from the air and fuel density ratio, volume of the chambers [compression ratio corrected], and the RPM.
        The output is in terms of kg/s so that other methods can determine the exact mass draw for a time step.
        """
        etaFuel = (self.Power-self.altAmpere*self.altVoltage)/self.Power
        if etaFuel < 0.9:
            etaFuel = 0.9
        self.V_Fuel = self.V_displacement/(1+self.AirFuel_ratio*self.Fuel_Density/self.rho) # m^3
        self.Fuel_Consumption = self.V_Fuel*self.Fuel_Density*(self.RPM/2)/60/etaFuel  # kg/s
        mdot = - self.Fuel_Consumption
        self.gal_hour = self.Fuel_Consumption/self.Fuel_Density*60**2/sp.constants.gallon

        # gal_hour.append()
        # print("Fuel burn: {} gal/hour\nWith RPM: {}".format(round(gal_hour, 2), round(self.RPM)))
        return mdot
    
    def __str__(self) -> str:
        return "Conventional"


    def __setattr__(self, name, value):
        # It is helpful to define the attributes first since that allows us to use it's specific name rather than the term "value"
        if name == "RPM":
            max = self.MaxRPM
            min = 1
            if value > max:
                value = max
            elif value < min:
                value = min
        object.__setattr__(self, name, value)
        #################
        # TYP the RPM will always be defined first as the POH usually dictates the RPM
        if name == "RPM":
            self.Throttle = self.RPM/self.MaxRPM
            self.Get_Power() 
            self.PowerRating = self.Power/self.MaxBreakPower*100
            # RPM affects power, so if the RPM changes, then so must the power
        
        ######################
        # Altitude parameters impact engine performance
        if name == "Altitude":
            self.Atmosphere_attr()
            if not hasattr(self, "rho_SL"):
                # This part will define the sea level condition for the simulation
                self.rho_SL = self.rho
            self.Get_Power()
            # The power setting will also need to be adjusted to account for the changes in density

        #####################
        # The engine mixture will change how much the air to fuel ratio is
        if name == "Mixture":
            if value.upper() == "RICH":
                self.AirFuel_ratio = 12 # Air to fuel ratio is 12:1
            if value.upper() == "LEAN":
                self.AirFuel_ratio = 16 # Air to fuel ratio is 16:1
                if self.Power/self.MaxPower > 0.75:
                    # For high power settings, a lower air to fuel ratio is required
                    # i.e. more fuel to air
                    self.Mixture = "RICH"
    def __repr__(self) -> str:
          return "Lycoming O-360-A4M"
    def __str__(self) -> str:
        return "Piston"










class ElectricEngineTest(PistonEngine):
    def __init__(self, Name, AircraftPropeller, MaxBreakHorsePower=180) -> None:
        super().__init__(Name, AircraftPropeller, MaxBreakHorsePower)
        self.Name = Name + ": Electric Engine"
    def Get_FuelConsumption(self):
        return 0
    def Get_EnergyDrain(self, dt, eta = 0.93):
        PowerWatt = self.Power
        Delta_Energy = -PowerWatt*dt/eta
        return Delta_Energy
    
    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if name == "RPM":
            max = self.MaxRPM
            min = 1
            if value > max:
                value = max
            elif value < min:
                value = min
        object.__setattr__(self, name, value)
        # TYP the RPM will always be defined first as the POH usually dictates the RPM
        if name == "RPM":
            self.Throttle = self.RPM/self.MaxRPM
            self.Get_Power() 
            # RPM affects power, so if the RPM changes, then so must the power
    
    def Get_Power(self):
        self.Power = self.MaxPower*self.Throttle
    def __repr__(self) -> str:
          return "ElectricEngineTest: {}".format(self.Name)
    def __str__(self) -> str:
        return "Electric"
    

class EMRAX_268_Engine(PistonEngine):
    def __init__(self, Name, AircraftPropeller, MaxBreakHorsePower=210/1.34102) -> None:
        self.Condition = "Continuous"
        # Since this is a test class, we will use the general "Name" to keep track of what the class is
        self.Propeller = AircraftPropeller
        # Propeller information is different between props, so we have a class for those properties
        self.MaxBreakHorsePower = MaxBreakHorsePower
        # Units in Horse Power
        self.eta = 0.93
        # self.eta = 0.9
        # Current Model for the engine to propeller efficiency is unknown
        self.BreakHorsePower = self.MaxBreakHorsePower
        # Power of the engine in terms of horsepower
        self.MaxBreakPower = self.MaxBreakHorsePower * self.hp_to_watt 
        # We define the engine's max break power to be in terms of Watts so fundementals equations can be applied
        self.Power = self.MaxBreakPower * self.eta
        self.MaxPower = self.Power
        self.PowerRating = self.BreakHorsePower/self.MaxBreakHorsePower
        self.MaxPower_SL = self.MaxPower
        # Current acutual power the aircraft is experiencing

        self.altVoltage = 28   # Piper Archer III alternator draws energy from here
        self.altAmpere = 70   # Piper Archer III alternator draws energy from here

        self.MaxRPM = 2700 
        self.Altitude = 0
        self.N_motors = 2
        self.Atmosphere_attr()
        # Setting Sea Level Parameters
        self.RPM = self.MaxRPM
        self.MaxBreakPower = MaxBreakHorsePower
        self.RPM = 0
        self.Name = Name + ": Electric Engine"
        if os.getcwd()[-5:] == "APCSE":
            filepath = os.getcwd() + "\\Propulsion"
        else:
            raise Exception("Engine.py is not configured to be ran outside of the 'APCSE' directory")
        data = pd.read_csv(filepath+"\\"+"Continuous Efficiency.csv", header=None).to_numpy().T
        self.RPM_data, self.eta_data = data
    def Get_FuelConsumption(self):
        return 0
    def Get_EnergyDrain(self, dt):
        PowerWatt = self.Power + self.altVoltage*self.altAmpere*1.2
        Delta_Energy = -PowerWatt*dt/self.eta / self.motorEta()
        return Delta_Energy
    def motorEta(self):
        funkyTime = make_smoothing_spline(self.RPM_data, self.eta_data, lam = 0)
        return funkyTime(self.RPM)/100
    


    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)
        # TYP the RPM will always be defined first as the POH usually dictates the RPM
        if name == "RPM":
            self.Get_Power() 
            # RPM affects power, so if the RPM changes, then so must the power
    
    def Get_Power(self):
        if self.Condition == "Peak":
            self.Power = self.RPM * 0.05207458633766463*1e3 * self.N_motors
        elif self.Condition == "Continuous":
            self.Power = self.RPM * 0.022055423626601994*1e3 * self.N_motors
        else:
            raise ValueError("Does not recognize Condition: {}\nself.Condition must be either 'Peak' or 'Continuous'".format(self.Condition))

    def __repr__(self) -> str:
          return "EMRAX 268" # Should just be the engine model
    def __str__(self) -> str:
        return "Electric"
    

# import matplotlib.pyplot as plt
# from matplotlib.gridspec import GridSpec
# import scienceplots

# plt.style.use(["science","grid"])
# textsize = 18
# plt.rcParams.update({'font.size': textsize})