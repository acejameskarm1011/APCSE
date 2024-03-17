from Aviation import Aviation

class Weight(Aviation):
    def __init__(self, WeightDict, MaxMass, FuelMass) -> None:
        self.Dictionary_setattr(WeightDict)
        if MaxMass >= self.MGTOW:
            self.MaxMass = self.MGTOW
        elif MaxMass < self.EmptyMass:
            self.MaxMass = MaxMass
        else:
            self.MaxMass = MaxMass
        if FuelMass > self.MaxFuel:
            self.FuelMass = FuelMass

class Balance(Aviation):
    pass