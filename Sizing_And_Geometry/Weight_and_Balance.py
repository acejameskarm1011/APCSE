from Aviation import Aviation
import numpy as np

class Mass(Aviation):
    def __init__(self, AircraftDict, FrontSeatMass, RearSeatMass = 0, BaggageMass = 0, Tabs = False) -> None:
        self.Dictionary_setattr(AircraftDict["Mass"])
        self.FrontSeatMass = FrontSeatMass
        self.RearSeatMass = RearSeatMass
        self.BaggageMass = BaggageMass
        if Tabs:
            self.MaxFuelMass = self.MaxFuel*2/3
        else:
            self.MaxFuelMass = self.MaxFuel
            
        Masses = np.array([self.EmptyMass, FrontSeatMass, RearSeatMass, BaggageMass, self.MaxFuelMass])
        Arms = np.array([self.EmptyMass_Arm, self.FrontSeat_Arm, self.RearSeat_Arm, self.Baggage_Arm, self.Fuel_Arm])        

        self.MaxMass = sum(Masses)

        self.CG = sum(Masses*Arms)/sum(Masses)

        self.Altitude = 0
        self.Atmosphere_attr()  
        self.reset()
        self.Weight = self.g * self.TotalMass
        self.etc = 0
    def reset(self):
        self.Altitude = 0
        self.Atmosphere_attr()
        self.TotalMass = self.MaxMass
        self.FuelMass = self.MaxFuelMass
        self.Weight = self.g * self.TotalMass
        self.etc = 0
    def __iadd__(self, MoreMass):
        if not isinstance(MoreMass, (float, int)):
            raise NotImplemented
        self.etc += MoreMass
        self.TotalMass = self.TotalMass + MoreMass
        
    def __isub__(self, mass):
        if not isinstance(mass, (float, int)):
            raise NotImplemented
        self.TotalMass -= mass
        self.FuelMass -= mass

class Balance(Aviation):
    pass

