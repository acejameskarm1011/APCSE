#Engine
import os
engine_dir = os.getcwd()
main_dir = "C:\\APCSE"
os.chdir(main_dir)
from AtmosphereFunction import AtmosphereFunctionSI
from Aviation import Aviation
os.chdir(engine_dir)
import scipy as sp

class Powerplant(Aviation):
    hp_to_watt = sp.constants.hp
    def __init__(self) -> None:
        pass

class TurboFan(Powerplant):
    pass

class TurboJet(Powerplant):
    pass

class PropEngine(Powerplant):
    pass

class TurboProp(PropEngine):
    pass
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
        A_2 = self.Diameter**2*sp.pi/4
        A_spin = self.Diameter**2*sp.pi/4
        eta_A = 1-A_spin/A_2
        return A_2, eta_A






class EngineTest(Powerplant):
    """
    This class is not completeled. Current goal is to use this as the basis for aquiring the trust, power and fuel drain from the aircraft.

    Parameters
    ---------
    Name : string
        Name of the aircraft or engine of interest
    MaxPower : int/float
        Rated power of the engine in terms of [hp]
    """
    def __init__(self, Name, AircraftPropeller, MaxPower = 180) -> None:
        self.Name = Name
        self.Propeller = AircraftPropeller
        self.BreakHorsePower = self.MaxPower
        self.MaxPower = MaxPower * self.hp_to_watt
        self.BreakPower = self.MaxPower
        self.eta = 0.9
        self.Power = self.BreakPower * self.eta
        self.Altitude = 0
        self.Atmosphere_attr()
    def Thrust_Static(self):
        A_2, eta_A = self.Propeller.Get_Area_and_AreaEfficiency()
        Thrust_Static = 0.85*self.Power**(2/3)*(2*self.rho*A_2)**(1/3)*eta_A
        return Thrust_Static

    def Get_Thrust(self, Velocity_infty, Velocity_NE):
        Velocity_Max = Velocity_NE*sp.constants.knot
        Thrust_Max = self.MaxPower/Velocity_Max
        Thrust_Static = self.Thrust_Static()
        self.Thrust = Thrust_Static + (3*Thrust_Max-2*Thrust_Static)/Velocity_Max*Velocity_infty + (Thrust_Static-2*Thrust_Max)/Velocity_Max**2*Velocity_infty**2
        return self.Thrust
    def Get_FuelConsumption(self):
        DcDP = (79-72)/(152-135)
        cmax = DcDP*(180-152) + 79
        cmax_Si = cmax * self.lbf_to_kg / self.h_to_s
        mdot = -cmax_Si

ArcherProp = Propeller("Sensenich", "76EM8S14-0-62", 76, 76/8)
engine1 = EngineTest("test", ArcherProp)
engine1.Get_Thrust(4)
engine1.Get_FuelConsumption()