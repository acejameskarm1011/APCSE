import numpy as np
from Aviation import Aviation

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


    Returns
    -------
    None

    Notes
    ----
    This class builds up all of the shared data for all components.      
    """

    def __init__(self, AircraftName, AircraftDict, **Components) -> None: 
        self.AircraftName = AircraftName
        self.AircraftDict = AircraftDict
        self.Components = Components
        self.Wings = Components["Wings"]
        self.HorizontalStabilizer = Components["HorizontalStabilizer"]
        self.Fuselage = Components["Fuselage"]
        self.VerticalStabilizer = Components["VerticalStabilizer"]
        self.Engine = Components["Engine"]
        self.Mass = Components["Mass"]
        self.ExtertnalComponents = [self.Wings, self.HorizontalStabilizer, self.Fuselage, self.VerticalStabilizer]
        self.Altitude = 0
        self.Atmosphere_attr()
        self.Velocity_hat = np.array([1,0,0])
        self.Velocity = np.zeros(3)
        self.RotationSpeed = AircraftDict["VSpeed"]["RotationSpeed"]
        self.NeverExceedSpeed = AircraftDict["VSpeed"]["NeverExceedSpeed"]
        self.GlideSpeed = AircraftDict["VSpeed"]["GlideSpeed"]
        self.BestClimbSpeed = AircraftDict["VSpeed"]["BestClimbSpeed"]
        self.MaxMass = self.Mass.MaxMass
        self.FuelMass = self.Mass.FuelMass
        self.TotalMass = self.Mass.TotalMass
    def GetTotalThrust(self, Velocity_infty=""):
        if isinstance(Velocity_infty, str):
            Velocity_infty = self.V_infty
        Thrust = self.Engine.Get_Thrust(Velocity_infty, self.NeverExceedSpeed)
        return Thrust
    def GetTotalC_D(self):
        C_D = 0
        for Part in self.ExtertnalComponents:
            Part.C_L = self.C_L
            Part.Mach = self.Mach
            Part.Atmosphere_attr()
            C_D += Part.EvaluateC_D()
        self.C_D = C_D
        return C_D
    
    def HybridizeBattery(self, BatteryDensity, MassFactor = None, PowerFactor = None, eta_mass = None):
        """
        Function that transforms the aircraft from a conventional aircraft to a battery powered hybrid aircraft. 
        This function will only run if the aircraft still has the same initial mass.

        Parameters
        ----------
        BatteryDensity : float or int
            The energy density of the battery in units of Watt hours

        MassFactor : float or int
            A value betweeen 0 and 1 where the battery mass ratio is multiplied by this value

        PowerFactor : float or int
            A value betweeen 0 and 1 where the battery power ratio is multiplied by this value
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
    
    def __setattr__(self, name, value):
        if name == "Velocity":
            if not isinstance(value, np.ndarray):
                raise TypeError("Velocity attribute must be a NumPy array")
            elif len(value) != 3:
                raise ValueError("Velocity must be of size (3,)")
            print(type(np.sqrt(value.T@value)))
            self.V_infty = np.sqrt(value.T@value)
            if self.V_infty != 0:
                self.Velocity_hat = value/self.V_infty
            self.Mach = self.V_infty/self.acousic_v
        object.__setattr__(self, name, value)