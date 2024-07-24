import numpy as np
from Aviation import Aviation
from Propulsion.Engine import ElectricEngineTest
from Aerodynamic_Classes.Coefficients import Coefficients
import scipy as sp


class Aircraft(Aviation): 
    """
    Stores data that needs to be held within every aircraft in the program. 
    
    Parameters
    ---------
    AircraftName : string
        Name of the aircraft being evaluated

    Wings : instance of Wings class
        Wings of the aircraft class

    HorizontalStabilizer : instance of HorizontalStabilizer class
        HorizontalStabilizer of the aircraft class 

    Fuselage : instance of Fuselage class
        Fuselage of the aircraft class

    VerticalStabilizer : instance of VerticalStabilizer class
        VerticalStabilizer of the aircraft class
    
    Engine : Instance of the Engine class
        Engine and propeller combination for the aircraft

    Notes
    ----
    This class builds up all of the shared data for all components.      
    """

    def __init__(self, AircraftName, AircraftDict, **Components) -> None: 
        self.AircraftName = AircraftName
        self.AircraftDict = AircraftDict
        self.Components = Components
        self.Wings = Components["Wings"]
        self.alpha = (self.Wings.alpha-3)/180*np.pi
        self.HorizontalStabilizer = Components["HorizontalStabilizer"]
        self.Fuselage = Components["Fuselage"]
        self.VerticalStabilizer = Components["VerticalStabilizer"]
        self.Engine = Components["Engine"]
        self.Mass = Components["Mass"]
        self.Mass = Components["Mass"]
        self.ExtertnalComponents = [self.Wings, self.HorizontalStabilizer, self.Fuselage, self.VerticalStabilizer]
        self.Coefficients = Coefficients(self.ExtertnalComponents)
        self.Altitude = 0.
        self.Position = np.zeros(3, float)
        self.Pitch = 0

        self.Atmosphere_attr()
        self.V_infty = 0.
        self.RotationSpeed = AircraftDict["VSpeed"]["RotationSpeed"]
        self.NeverExceedSpeed = AircraftDict["VSpeed"]["NeverExceedSpeed"]
        self.GlideSpeed = AircraftDict["VSpeed"]["GlideSpeed"]
        self.BestClimbSpeed = AircraftDict["VSpeed"]["BestClimbSpeed"]
        self.MaxMass = self.Mass.MaxMass
        self.FuelMass = self.Mass.FuelMass
        self.MaxFuel = self.FuelMass
        self.FuelPercent = self.FuelMass/self.MaxFuel
        self.TotalMass = self.Mass.TotalMass
        self.MGTOW_Percent = self.MaxMass/self.Mass.MGTOW
        self.Aircraft_Forces()

        self.Masses = [self.TotalMass] # A quirk that is required so that preivous masses can be used when employing multistep methods
        self.BatteryEnergy = 0.
        self.MaxEnergy = 0.

        if isinstance(self.Engine, ElectricEngineTest):
            # If it is detected that the engine used is an electric one, then the aircraft class
            # automatically switches to an electric model of evaluation
            BatteryDensity = 250. # Wh/kg
            BatteryEta = 0.5 # A source should be used to back this up
            self.BatteryEnergy = self.FuelMass * BatteryDensity * BatteryEta * 60**2
            self.FuelMass = 0.
            self.MaxFuel = 0.
            self.MaxEnergy = self.BatteryEnergy
            self.BatteryPercent = self.BatteryEnergy/self.MaxEnergy

    def reset(self):
        self.Altitude = 0.
        self.V_infty = 0.
        self.Position = np.array([0,0,0], float)
        self.TotalMass = self.MaxMass
        self.FuelMass = self.MaxFuel
        self.BatteryEnergy = self.MaxEnergy

        self.Set_RPM(2700)
        self.Wings.reset()
        self.alpha = (self.Wings.alpha-3)/180*np.pi

        self.Aircraft_Forces()

    def Switch_Tabs(self):
        if 


    def GetTotalThrust(self):
        """
        Using the current engine on the aircraft, the total thrust output is computed in units of Netwons. The engine power output is directly
        related to the current throttle setting and atmospheric conditions. With a selected power, the thrust  
        """
        self.Thrust = self.Engine.Get_Thrust(self.V_infty, self.NeverExceedSpeed)
        return self.Thrust
    
    def Set_RPM(self, RPM):
        """
        From within the aircraft class, we set RPM of the engine to be of a specified value.

        Parameters
        ----------
        RPM : int/float
            Revolutions per minute of the engine's driveshaft. For engines with a 1:1 gear ratio, that means the RPM also corresponds to 
            the propellers RPM.
        """
        self.Engine.RPM = RPM

    def Set_Thrust(self):
        """
        For system of analysis where thrust is a known value, this method shall be called when the aircraft's thrust is updated. 
        Further reading on this method is found in the Engine class method: "Set_Thrust()"

        Returns
        -------
        None
        """
        self.Engine.Set_Thrust(self.Thrust, self.V_infty, self.NeverExceedSpeed)
        


    def FuelDraw(self, delta_t):
        """
        Is used to evaluate the fuel bruned in either fuel mass [kg] or in battery charge [J]. Depending on the type of engine on board
        strictly fuel mass, energy, or both are drawn. 

        Parameters
        ----------
        delta_t : int/float
            The time step variable that determines how much mass or energy is being lost at a given state
        
        Returns
        ------
        None
        """
        mdot = self.Engine.Get_FuelConsumption() # units are in kg/s
        self.FuelMass += mdot*delta_t
        self.TotalMass += mdot*delta_t
        self.Masses.append(self.TotalMass)
        self.FuelPercent = self.FuelMass/self.MaxFuel
        if isinstance(self.Engine, ElectricEngineTest):
            BatteryDrain = self.Engine.Get_EnergyDrain(delta_t)
            self.BatteryEnergy += BatteryDrain
            self.BatteryPercent = self.BatteryEnergy/self.MaxEnergy

    def Get_C_L(self):
        """
        Currently using only the wings, we evaluate the coefficient of lift and gain the
        """
        self.C_L = self.Wings.Get_C_L()
        return self.C_L

    def Get_C_D(self):
        """
        This method uses the aircraft's current state and evaluates the C_D for each of the exterior components.
        Code is based on Roskam calculation for drag, with work completed by Eric, et al.

        Returns
        ------
        C_D : float
            The coefficient of drag [no units]
        """
        self.Coefficients.V_infty = self.V_infty
        self.C_D = self.Coefficients.Get_C_D()
        return self.C_D
    
    def HybridizeBattery(self, BatteryDensity, MassFactor = None, PowerFactor = None, eta_mass = None):
        """
        Function that transforms the aircraft from a conventional aircraft to a battery powered hybrid aircraft. 
        This function will only run if the aircraft still has the same initial mass.

        Parameters
        ----------
        BatteryDensity : float or int
            The mass specific energy of the battery in units of Watt hours per kg

        MassFactor : float or int
            A value betweeen 0 and 1 where the battery mass ratio is multiplied by this value

        PowerFactor : float or int
            A value betweeen 0 and 1 where the battery power ratio is multiplied by this value

        eta_mass : float or int
            A value between 
        """
        if MassFactor==None or PowerFactor==None or eta_mass==None:
            return None
        if 0 > MassFactor or 1 < MassFactor:
            raise ValueError("MassFactor must be within 0 and 1")
        if 0 > PowerFactor or 1 < PowerFactor:
            raise ValueError("PowerFactor must be within 0 and 1")
        if not hasattr(object, "BatteryMass"):
            pass
        BatteryDensity *= BatteryDensity*60**2 # Units in Joules
        self.BatteryMass = MassFactor*self.FuelMass*eta_mass
        self.BatteryEnergy = self.BatteryMass*BatteryDensity

    def Set_Lift(self):
        self.GetTotalThrust()
        self.Lift = self.Weight*np.cos(self.Pitch)-self.Thrust*np.sin(self.alpha)
        S = self.Wings.S_wing
        self.C_L = self.Lift/(1/2*self.rho*self.V_infty**2*S)
        self.Wings.Set_C_L(self.C_L)
        self.alpha = (self.Wings.alpha-3)/180*np.pi

        C_D = self.Get_C_D()
        self.Drag = 1/2*self.rho*self.V_infty**2*S*C_D
        


    def Aircraft_Forces(self):
        self.GetTotalThrust()
        C_L = self.Get_C_L()
        S = self.Wings.S_wing
        self.Lift = 1/2*self.rho*self.V_infty**2*S*C_L
        self.Weight = self.TotalMass*self.g

        C_D = self.Get_C_D()
        self.Drag = 1/2*self.rho*self.V_infty**2*S*C_D

    def GetC_L_max(self, Components):
        C_L = 0
        k = 0
        C_D0 = 0
        for Part in Components:
            Part.C_L = C_L
            Part.EvaluateC_D()
            P_C_L = np.sqrt(Part.k/Part.C_D0)
            if Part.PartName == "HorizontalStabilizer":
                C_L -= P_C_L * 0.05
            if Part.PartName == "Wings":     
                C_L += P_C_L * 1.05
            k += Part.k
            C_D0 += Part.C_D0
        self.C_L = C_L
        return C_L
    
    def Emergency_Check(self):
        if self.EnergyMass < 0:
            self.Thrust = 0
            self.Power_Thrust = 0
            self.Emergency = "No_Energy"

    def GetTSFC(self, unit = 'hr'):
        TSFC = 0.78
        self.TSFC = TSFC
        if unit == 's':
             self.TSFC = self.TSFC / 3600
        return self.TSFC
    


    def __setattr__(self, name: str, value):
        if name == "V_infty":
            self.Coefficients.V_infty = value
        if name == "alpha":
            if value > 16/np.pi*180:
                raise ValueError("Angle of Attack of {} deg is not valid".format(value/np.pi*180))
        """
        if name == "Velocity":
            if not isinstance(value, np.ndarray):
                raise TypeError("Velocity attribute must be a NumPy array")
            elif len(value) != 3:
                raise ValueError("Velocity must be of size (3,)")
            self.V_infty = np.sqrt(value.T@value)
            if self.V_infty != 0:
                self.Velocity_hat = value/self.V_infty
        """
        object.__setattr__(self, name, value)
        if name == "Lift":
            self.Coefficients.Lift = value
        if name == "Altitude":
            if isinstance(value, (float, int)):
                self.Atmosphere_attr()
                self.Engine.Altitude = value
                self.Coefficients.Altitude = value
            else: 
                raise TypeError("Cannot accept value of type {}".format(type(value)))
            
        if name == "Position":
            if isinstance(value, (np.ndarray, list)):
                Alt = value[2] * self.m_to_ft
                self.Altitude = Alt
            else:
                raise TypeError("Cannot accept value of type {}".format(type(value)))





    def __repr__(self):
        return "Aircraft({}, {},\n\tWings = {},\n\tHorizontalStabilizer = {},\n\tFuselage = {},\n\tVerticalStabilizer = {},\n\tEngine = {},\n\tMass = {})".format(self.AircraftName, self.AircraftDict, self.Wings, self.HorizontalStabilizer, self.Fuselage, self.VerticalStabilizer, self.Engine, self.Mass)

    def __str__(self):
        if not isinstance(self.Engine, ElectricEngineTest):
            Battery = "0"
        else:
            Battery = self.BatteryPercent
        Forces_vals = np.round(np.array([self.Lift, self.Thrust, self.Drag, self.Weight], float))
        Forces = "\n\tLift: {} [N], \n\tThrust: {} [N], \n\tDrag: {} [N], \n\tWeight: {} [N]\n".format(*Forces_vals)
        Pos_Vel_vals = np.round(np.array([self.Altitude, self.V_infty/sp.constants.knot, self.Pitch/np.pi*180, self.alpha/np.pi*180],float))
        Pos_Vel = "\n\tAltitude: {} [ft], \n\tV_infty: {} [kts], \n\tPitch: {} [deg], \n\tAOA: {} [deg]\n".format(*Pos_Vel_vals)
        Aero_Vals = np.round(np.array([self.C_L, self.C_D],float), 5)
        Aero = "\n\tC_L: {} [None], \n\tC_D: {} [None]\n".format(*Aero_Vals)
        Engine_Status = np.round(np.array([self.Engine.RPM, self.Engine.Power/sp.constants.hp, self.FuelPercent*100, Battery*100], float))
        Engine = "\n\tRPM: {} [rev/min], \n\tPower: {} [hp], \n\tFuel: {} [%], \n\tBattery: {}".format(*Engine_Status)
        Last = "With an altitude of {} [ft], true airspeed of {} [kts], and with engine parameters being: {}\n\n".format(self.Altitude, self.V_infty/sp.constants.knot, Engine)
        return "\n\n{} is flying with state: {}".format(self.AircraftName, Forces) + Aero + Pos_Vel + Engine
    # def __repr__(self) -> str:
    #       return "Aircraft: {}".format(self.AircraftName)