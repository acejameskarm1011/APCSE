import numpy as np
from matplotlib import pyplot as plt
from AtmosphereFunction import AtmosphereFunctionSI
from Aviation import Aviation
import os


class Aircraft(Aviation): 
    """
    Stores data that needs to be held within every aircraft in the program. Contains the unit conversions
    """

    def __init__(self, AircraftName, CruiseMach, CruiseAltitude, AircraftType) -> None: 
        #Required upon initalization
        self.AircraftName = AircraftName
        self.CruiseMach = CruiseMach
        self.CruiseAltitude = CruiseAltitude
        self.AircraftType = AircraftType
        #Initial States
        self.Mach = 0
        self.Altitude = 0
        self.Range = 0
        self.Endurance = 0
    
    def __str__(self):
        return f"This aircraft is the {self.AircraftName}h"
    
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
     
    def Part_Import(self):
        main_dir = os.getcwd()
        if self.AircraftType.upper().__contains__("EMBRAER"):
            Part_dir = main_dir + ".\Jet_Classes"
            os.chdir(Part_dir)
            from Jet_Classes.ImportJet import Wings, HorizontalStabilizer, Fuselage, VerticalStabilizer
            os.chdir(main_dir)
        else:
            Part_dir = main_dir + ".\GA_Classes"
            os.chdir(Part_dir)
            from GA_Classes.ImportGA import Wings, HorizontalStabilizer, Fuselage, VerticalStabilizer
            os.chdir(main_dir)
        self.Wings = Wings(self.AircraftType + '_Wings')
        self.HorizontalStabilizer = HorizontalStabilizer(self.AircraftType + '_Horizontal_Stabilizer')
        self.Fuselage = Fuselage(self.AircraftType + '_Fuselage')
        self.VerticalStabilizer = VerticalStabilizer(self.AircraftType + '_Vertical_Stabilizer')
        self.SubComponents = [self.Wings, self.HorizontalStabilizer, self.Fuselage, self.VerticalStabilizer]