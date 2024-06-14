#Engine
import os
# engine_dir = os.getcwd()
# main_dir = engine_dir[:-20]
# print(engine_dir[:-20])
# main_dir = "C:\\APCSE"
# os.chdir(main_dir)
from AtmosphereFunction import AtmosphereFunctionSI
from Aviation import Aviation
# os.chdir(engine_dir)
import scipy as sp
import numpy as np



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
        A_2 = self.Diameter**2*np.pi/4
        A_spin = self.Spinner_Diameter**2*np.pi/4
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
    def __init__(self, Name, AircraftPropeller, MaxBreakHorsePower = 180) -> None:
        self.Name = Name
        # Since this is a test class, we will use the general "Name" to keep track of what the class is
        self.Propeller = AircraftPropeller
        # Propeller information is different between props, so we have a class for those properties
        self.MaxBreakHorsePower = MaxBreakHorsePower
        # Units in Horse Power
        self.eta = 0.9
        # Current Model for the engine to propeller efficiency is unknown
        self.BreakHorsePower = self.MaxBreakHorsePower
        # Power of the engine in terms of horsepower
        self.MaxBreakPower = self.MaxBreakHorsePower * self.hp_to_watt 
        # We define the engine's max break power to be in terms of Watts so fundementals equations can be applied
        self.MaxPower = self.Power
        # Current acutual power the aircraft is experiencing
        self.Altitude = 0
        self.Atmosphere_attr()
        # Engine requires the atmospheric information
        self.RPM = 2700
        DcDP = (79-72)/(152-135)
        self.c_BHP = DcDP*(180-152) + 79

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
        Thrust_Static = 0.85*self.Power**(2/3)*(2*self.rho*A_2)**(1/3)*eta_A
        return Thrust_Static

    def Get_Thrust(self, Velocity_infty, Velocity_NE):
        V = Velocity_infty
        Velocity_Max = Velocity_NE
        Thrust_Max = self.MaxPower/Velocity_Max
        Thrust_Static = self.Thrust_Static()
        
        self.Thrust = Thrust_Static + (3*Thrust_Max-2*Thrust_Static)/Velocity_Max*V + (Thrust_Static-2*Thrust_Max)/Velocity_Max**2*V**2
        return self.Thrust
    
    def Set_Power(self, Thrust, V_des, RPM, Velocity_NE, tol = 5, P_min = 0):
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
        Thrust_Max = self.MaxPower/Velocity_Max
        nu = V_des/Velocity_NE
        A_2, eta_A = self.Propeller.Get_Area_and_AreaEfficiency()
        PArr = np.arange(P_min, self.MaxPower + tol*2, tol)
        # PArr = self.PArr
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
        self.BreakHorsePower = P_est / (self.eta * self.hp_to_watt)


    def Get_FuelConsumption(self):
        mdot = - self.c_BHP * self.lbf_to_kg / self.h_to_s
        return mdot
    def __setattr__(self, name, value):
        if name == "BreakHorsePower":
            self.Power = value * self.eta * self.hp_to_watt
        object.__setattr__(self, name, value)


class ElectricEngineTest(EngineTest):
    def Get_FuelConsumption(self):
        return 0
    def Get_EnergyDrain(self, dt, eta = 0.93):
        PowerWatt = self.Power
        Delta_Energy = -PowerWatt*dt/eta
        return Delta_Energy

ArcherProp = Propeller("Sensenich", "76EM8S14-0-62", 76, 0)
engine1 = EngineTest("test", ArcherProp)



import matplotlib.pyplot as plt
import numpy as np
import scienceplots
textsize = 18
plt.rcParams.update({'font.size': textsize})
plt.style.use(["science", "grid"])
fig = plt.figure(figsize=(10,7))
ax = fig.add_subplot(111)


Velocity_Array = np.linspace(0,180, 1000)
def Thurst_General(Velocity):
    Velocity = Velocity * sp.constants.knot
    Power = 180 * sp.constants.hp
    Velocity[Velocity == 0] = Velocity[np.where(Velocity == 0)[0]+1]
    return Power / Velocity

ThrustIdeal = Thurst_General(Velocity_Array)


Title = "Plots of Ideal Thrust vs. Acutal Thrust"

ax.set_title(Title[1:])
ax.set_xlabel(r"Velocity $V_\infty$ [kts]")
ax.set_ylabel(r"Thrust $T$ [N]")
ax.plot(Velocity_Array, ThrustIdeal, "g-", label = r"$T = \frac{P}{V}$", lw = 3)
Altitude = [0,2000,4000,6000,8000]
for h in Altitude:
    engine1.Altitude = h
    ThrustReal = engine1.Get_Thrust(Velocity_Array, Velocity_Array.max())
    ax.plot(Velocity_Array, ThrustReal, ls = "--", label = f"Actual Thrust at h = {engine1.Altitude}", lw = 3)
ax.set_ylim((-1, 0.5*10**4))
ax.set_xlim(left = 0)

ax.text(150, 3500, f"$P = {engine1.MaxBreakHorsePower}$ hp\n Altitude = {engine1.Altitude} ft",
            ha="center", va="center", rotation=0, size=textsize,
            bbox=dict(boxstyle="square,pad=.3",
                      fc="white", ec="black", lw=1))
Title = Title.replace(" ", "_") + ".png"
plt.legend()
plt.close()