import os
from AtmosphereFunction import AtmosphereFunctionSI
from Aviation import Aviation
import scipy as sp
import numpy as np

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

        self.Name = Name + ": Piston Engine"
        # Since this is a test class, we will use the general "Name" to keep track of what the class is
        self.Propeller = AircraftPropeller
        # Propeller information is different between props, so we have a class for those properties
        self.MaxBreakHorsePower = MaxBreakHorsePower
        # Units in Horse Power
        self.eta = 0.92
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
        self.Mixture = "lean"
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
        self.Atmosphere_attr()
        A_2, eta_A = self.Propeller.Get_Area_and_AreaEfficiency()
        # Get the disk area of the propeller, and get the efficiency of the area that accounts for blockage effects
        Thrust_Static = 0.85*self.Power**(2/3)*(2*self.rho*A_2)**(1/3)*eta_A
        # Using Disk Momentum theory, we get the thrust for a stationary aircraft
        return Thrust_Static

    def Get_Thrust(self, Velocity_infty, Velocity_NE):
        """
        Utilizing a quadradic interpolation of the 
        """
        V = Velocity_infty
        Velocity_Max = Velocity_NE
        Thrust_Max = self.Power/Velocity_Max
        Thrust_Static = self.Thrust_Static()
        self.Thrust = Thrust_Static + (3*Thrust_Max-2*Thrust_Static)/Velocity_Max*V + (Thrust_Static-2*Thrust_Max)/Velocity_Max**2*V**2
        return self.Thrust
    
    def Set_Thrust(self, Thrust, V_des, Velocity_NE, tol = 5, P_min = 0):
        """
        Using Thrust, Velocity, and the chosen RPM, we can evaluate what the power output of the engine is in Break Horse Power
        and set those parameters within the class.

        Parameters
        ----------
        Thrust : float or int
            Desired thrust for the state that the aircraft is in. Used in cases where required thrust is known based on the EOM.

        V_des : float or int
            Similar to thrust; based on the desired state of the aircraft, we use the aircraft's current velocity

        RPM : float or int
            This is used to update the aircraft's RPM setting, which is important for determining the fuel drain

        Velocity_NE : float or int
            Maximum velocity possible for the aircraft

        Returns
        -------
        None
        """
        Velocity_Max = Velocity_NE
        Thrust_Max = self.Power/Velocity_Max
        nu = V_des/Velocity_NE
        A_2, eta_A = self.Propeller.Get_Area_and_AreaEfficiency()
        # PArr = np.arange(P_min, self.Power + tol*2, tol)
        PArr = self.PArr
        Left = (Thrust + (2*nu**2-3*nu)*PArr/Velocity_Max)/(nu**2-2*nu+1)
        Right = 0.85*PArr**(2/3)*(2*self.rho*A_2)**(1/3)*eta_A
        TrueDiff = Left-Right
        Diff = np.abs(TrueDiff)
        min_1 = Diff.min()
        Diffm1 = Diff.tolist()
        Diffm1.remove(min_1)
        Diffm1 = np.array(Diffm1)
        min_2 = Diffm1.min()
        val_1 = TrueDiff[Diff == min_1][0]
        val_2 = TrueDiff[Diff == min_2][0]
        x_percent = (0-val_1)/(val_2-val_1)
        P_1 = PArr[Diff == min_1][0]
        P_2 = PArr[Diff == min_2][0]
        P_est = P_1 + (P_2-P_1)*x_percent
        self.RPM = self.MaxRPM*(P_est/self.MaxPower)**(1/4)

        # Use an assumption for how power scales with RPM
        # (P/P_max) = (RPM/RPM_max)^4 
        # Note: There is no real world basis for this to be correct whatsoever. The engine model for the air inside the chamber
        # still has much further to go to be of an adequate fidelity

    def Get_Power(self):
        """
        This is the function that should be called when the power should be 

        Returns
        -------
        self.Power : float
            Current power output of the propeller [W]
        """
        sigma = self.rho/self.rho_SL
        R_m = np.sin(self.Throttle**3*np.pi/2)
        if np.isclose(1.0, self.Throttle):
            self.Power = self.MaxPower*sigma
        else:
            self.Power = self.MaxPower_SL*(R_m*(sigma-R_m**(0.8097))+(R_m**(0.8097)-0.117)/0.883*(1-sigma))/(1-R_m)
        return self.Power

    def Get_FuelConsumption(self):
        """
        The fuel consumption is derived from the air and fuel density ratio, volume of the chambers [compression ratio corrected], and the RPM.
        The output is in terms of kg/s so that other methods can determine the exact mass draw for a time step.
        """
        self.V_Fuel = self.V_displacement/(1+self.AirFuel_ratio*self.Fuel_Density/self.rho) # m^3
        self.Fuel_Consumption = self.V_Fuel*self.Fuel_Density*(self.RPM/2)/60  # kg/s
        mdot = - self.Fuel_Consumption
        return mdot
    


    def __setattr__(self, name, value):
        # It is helpful to define the attributes first since that allows us to use it's specific name rather than the term "value"
        if name == "RPM":
            max = self.MaxRPM
            min = 250
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
