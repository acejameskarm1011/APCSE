#Aircraft

from Aviation import *

class Aircraft(Aviation):
    def __init__(self, AircraftName, CruiseMach, CruiseAltitude, AircraftType, AircraftDictionary) -> None:
        super().__init__(AircraftName, CruiseMach, CruiseAltitude, AircraftType)
        # a new change here
        self.Atmosphere_attr()
        self.Emergency = None
        self.Wings = 1
        self.AircraftType = AircraftType

        self.Dictionary_setattr(AircraftDictionary)
        self.Position = np.array([0,0,0])

        self.C_D = 0.05
        self.C_L = 1       
        self.Part_Import()
        self.Wings.Dictionary_setattr(AircraftDictionary["Fuselage"])
        self.Wings.Dictionary_setattr(AircraftDictionary["Wings"])
        self.HorizontalStabilizer.Dictionary_setattr(AircraftDictionary["Horizontal_Stabilizer"])
        self.percent = 0

    def Emergency_Check(self):
        if self.EnergyMass < 0:
            self.Thrust = 0
            self.Power_Thrust = 0
            self.Emergency = "No_Energy"

    def Dictionary_setattr(self, Dictionary):
        if "Wings" in Dictionary:
            self.S = Dictionary['Wings']['S_wing']
        if "Performance" in Dictionary:
            Dictionary = Dictionary["Performance"]
            super().Dictionary_setattr(Dictionary)
        else:
            super().Dictionary_setattr(Dictionary)
        self.EnergyMass = self.MaxFuel
        self.TotalMass = self.MGTOW
    

    def Climb(self, dt = 10): #1000 ft/min, 2 deg #On a quick GoOgle search, it was found that aircraft TYP climb at 250kts below 10k ft, and transition to 300 kts above FL10, then at FL25 AC climb at 0.7 Mach
        self.Atmosphere_attr()
        #Evaluation
        self.v_z = self.v_h * self.ft_to_m /60
        self.v_x = np.sqrt(self.v**2-self.v_z**2)
        gamma = np.arctan2(self.v_z,self.v_x) #Flight Angle
        self.DynamicPressure = .5*self.rho*self.v**2
        self.Weight = self.TotalMass * self.g
        self.Lift = self.Weight * np.cos(gamma)
        self.C_L = (self.Lift / (self.DynamicPressure * self.S))
        self.GetC_D(self.SubComponents)
        # self.C_D = .01
        self.Drag = self.DynamicPressure * self.S * self.C_D
        self.Thrust = self.Drag + (self.Weight * np.sin(gamma))
        self.GetSC()
        self.FuelBurn = -self.Thrust*self.TSFC*dt/self.g
        self.Power_Thrust = self.Thrust * self.v # Terms of W
        self.v_h = self.v_z * self.m_to_ft
        self.Altitude += self.v_h * dt
        self.EnergyMass += self.FuelBurn 
        return "Climb ran successfully"
      
    def Cruise(self, dt = 10):
        self.Atmosphere_attr()
        self.v = self.acousic_v * self.CruiseMach
        self.v_x = self.v
        self.DynamicPressure = .5*self.rho*self.v**2
        self.Weight = self.TotalMass * self.g
        self.Lift = self.Weight
        self.C_L = self.Lift/(self.DynamicPressure * self.S)
        self.GetC_D(self.SubComponents)
        self.Drag = self.DynamicPressure * self.S * self.C_D
        self.Thrust = self.Drag
        self.GetSC()
        self.FuelBurn = -self.Thrust*self.TSFC*dt/self.g
        self.EnergyMass += self.FuelBurn 
        self.Power_Thrust = self.Thrust * self.v
        
    def ZeroThrustGlide(self, dt = 10):
        self.Atmosphere_attr()
        if "PIPER" in self.AircraftType.upper():
            self.v = 76 * self.knots_to_mps
            self.v_h = -1000
            self.v_z = self.v_h*self.ft_to_m/60
            self.gamma = np.arcsin(self.v_z/self.v)
        else:
            self.GetC_L_max([self.Wings, self.HorizontalStabilizer])
            self.GetC_D(self.SubComponents)
            self.gamma = -np.arctan(self.C_D/self.C_L)
            self.TotalMass = self.MGTOW - self.MaxFuel
            self.Weight = self.TotalMass * self.g
            V_Glide = np.sqrt(2*self.Weight*np.cos(self.gamma)/(self.rho*self.S*self.C_L))
            self.v = V_Glide
        self.v_x = np.cos(self.gamma)*self.v
        self.v_y = np.zeros(self.v_x.shape)
        self.v_z = np.sin(self.gamma)*self.v
        self.v_h = self.v_z * self.m_to_ft
        self.Altitude += self.v_h * dt
        self.Velocity = np.array([self.v_x, self.v_y, self.v_z])
    def GetSC(self):
        self.GetTSFC(unit = 's')
        if "PIPER" in self.AircraftType.upper():
            self.TSFC = 19.9581/3600/self.Thrust*self.g
        return None