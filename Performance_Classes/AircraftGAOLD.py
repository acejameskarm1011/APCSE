from Performance_Classes.AircraftOLD import Aircraft
import numpy as np

class AircraftGA(Aircraft):
    def __init__(self, AircraftName, CruiseMach, CruiseAltitude, AircraftType, AircraftDictionary) -> None:
        super().__init__(AircraftName, CruiseMach, CruiseAltitude, AircraftType, AircraftDictionary)
        self.MaxHP = 180
        self.MaxPower = 745.7 * self.MaxHP
    def Climb(self, dt=10):
        self.Atmosphere_attr()
        self.Power_Thrust = self.MaxPower
        #Evaluation
        self.v = 76 * self.knots_to_mps
        self.Thrust = self.Power_Thrust/self.v
        self.Drag = self.Thrust
        self.C_D = self.Drag/(self.DynamicPressure * self.S)

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
