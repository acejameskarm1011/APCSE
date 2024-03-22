from Aviation import Aviation

class Mass(Aviation):
    def __init__(self, AircraftDict, MaxMass = 1e10, MaxFuelMass = 1e10) -> None:
        self.Dictionary_setattr(AircraftDict["Mass"])
        if MaxMass >= self.MGTOW:
            self.MaxMass = self.MGTOW
        elif MaxMass < self.EmptyMass:
            self.MaxMass = MaxMass
        else:
            self.MaxMass = MaxMass
        if MaxFuelMass > self.MaxFuel:
            self.MaxFuelMass = MaxFuelMass
        self.reset()
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

