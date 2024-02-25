import numpy as np
from matplotlib import pyplot as plt
from AtmosphereFunction import AtmosphereFunctionSI
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

    def __init__(self, AircraftName, Wings, HorizontalStabilizer, VerticalStabilizer, Fuselage, Engine) -> None: 
        self.AircraftName = AircraftName
        self.Wings = Wings
        self.HorizontalStabilizer = HorizontalStabilizer
        self.Fuselage = Fuselage
        self.VerticalStabilizer = VerticalStabilizer
        self.Engine = Engine
        self.SubComponents = [Wings, HorizontalStabilizer, Fuselage, VerticalStabilizer, Engine]
        self.Altitude = 0
        self.Atmosphere_attr()
    def GetC_D(self, Components):
        C_D = 0
        for Part in Components:
            Part.C_L = self.C_L
            Part.Mach = self.Mach
            Part.rho = self.rho
            C_D += Part.EvaluateC_D()
        self.C_D = C_D
        return C_D
    

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