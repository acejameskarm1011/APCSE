import numpy as np
from matplotlib import pyplot as plt
from AtmosphereFunction import AtmosphereFunctionSI
import os


class Aviation: 
    m_to_ft = 1/0.3048
    ft_to_m = 0.3048
    m_to_nmi = 1/1852
    nmi_to_m = 1852
    knots_to_mps = 0.51444
    mps_to_knots = 1/0.51444
    fps_to_knots = 0.592484
    knots_to_fps = 1/0.592484 

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
    
    def EvaluateC_D(self):
        return None
        
    def __str__(self):
        return f"This aircraft is the {self.AircraftName}, and it can fly a maximum of {self.Endurance}nmi for {self.Range} minutes and a cruise speed of {self.Mach} Mach"
    
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
        #self.gamma = -np.arctan(2*np.sqrt(C_D0*k))
        self.C_L = C_L
        return C_L
    def Atmosphere_attr(self):
        self.acousic_v, self.g, self.Pressure, self.Temperature, self.rho, self.mu = AtmosphereFunctionSI(self.Altitude, ['a','g','P','T', 'rho','mu'])               
    def Dictionary_setattr(self, Dictionary):
        for key in Dictionary:
            setattr(self, key, Dictionary[key])
        return None
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
        
    def Add_Components(self, Parts): # This is an older function, all Part_Import() to do it's thing
        if type(Parts) == type([]):
            for Part in Parts:
                self.__setattr__(Part.Name, Part)
        else:
            Parts.Mach = self.Mach
            self.__setattr__(Parts.PartName, Parts)