from Aviation import Aviation
import numpy as np

class Mass(Aviation):
    def __init__(self, AircraftDict, FrontSeatMass, RearSeatMass = 0, BaggageMass = 0, fuelMass=None, Tabs = False, massOarms = None) -> None:
        self.Dictionary_setattr(AircraftDict["Mass"])
        FrontSeatMass *= self.lbf_to_kg
        RearSeatMass *= self.lbf_to_kg
        BaggageMass *= self.lbf_to_kg
        self.FrontSeatMass = FrontSeatMass
        self.RearSeatMass = RearSeatMass
        self.BaggageMass = BaggageMass
        self.Electric = False
        if Tabs:
            self.initialFuelMass = self.MaxFuel*2/3
        else:
            if fuelMass==None:
                self.initialFuelMass = self.MaxFuel
            else:
                self.initialFuelMass = fuelMass
        Masses = [self.EmptyMass, self.FrontSeatMass, self.RearSeatMass, self.BaggageMass, self.initialFuelMass]
        Arms = [self.EmptyMass_Arm, self.FrontSeat_Arm, self.RearSeat_Arm, self.Baggage_Arm, self.Fuel_Arm]

        if massOarms != None:
            for massarms in massOarms:
                mass, arm = massarms
                Masses.append(mass)
                Arms.append(arm)

        Masses = np.array(Masses)
        Arms = np.array(Arms)

        self.checkEnvelope(Masses, Arms)
        self.etc = 0

    def electrify(self, motorMass, motorArm, inverterMass, inverterArm, ECUMass, ECUArm, BMSMass, BMSArm, energyDensity, packs):
        self.energyDensity = energyDensity
        self.Electric = True
        self.EmptyMass -= 315*self.lbf_to_kg
        Masses = [self.EmptyMass, self.FrontSeatMass, self.RearSeatMass, self.BaggageMass, self.initialFuelMass, motorMass, inverterMass, ECUMass, BMSMass]
        Arms = [self.EmptyMass_Arm, self.FrontSeat_Arm, self.RearSeat_Arm, self.Baggage_Arm, self.Fuel_Arm, motorArm, inverterArm, ECUArm, BMSArm]
        batteryMass = 0
        for pack in packs:
            m, a = pack
            batteryMass += m
            Masses.append(m)
            Arms.append(a)
        self.batteryMass = batteryMass
        Masses = np.array(Masses)
        Arms = np.array(Arms)
        self.checkEnvelope(Masses, Arms)
        self.reset()

    def checkEnvelope(self, Masses, Arms):
        self.MaxMass = sum(Masses)
        self.CG = sum(Masses*Arms)/sum(Masses)

        if self.CG > self.aftCG:
            raise Exception("CG: {} in is too aft the limit of {} in".format(round(self.CG*self.m_to_ft*12), round(self.aftCG*self.m_to_ft*12)))
        elif self.CG < self.forCG:
            raise Exception("CG: {} in is too forward the limit of {} in".format(round(self.CG*self.m_to_ft*12), round(self.forCG*self.m_to_ft*12)))
        elif self.MaxMass > self.MGTOW:
            print(Masses/self.lbf_to_kg)
            raise Exception("Inital mass: {} lb is over the MGTOW limit of {} lb".format(round(self.MaxMass/self.lbf_to_kg), round(self.MGTOW/self.lbf_to_kg)))
        elif self.MaxMass > (self.MGTOW - self.massForCG)/(self.midCG-self.forCG)*(self.CG-self.forCG) + self.massForCG:
            if not self.Electric:
                raise Exception("Initial mass {} lb is over the MGTOW limit of {} lb for a CG of {} in".format(round(self.MaxMass/self.lbf_to_kg), round(((self.MGTOW - self.massForCG)/(self.midCG-self.forCG)*(self.CG-self.forCG) + self.massForCG)/self.lbf_to_kg), round(self.CG*self.m_to_ft*12)))


        self.Altitude = 0
        self.Atmosphere_attr()  
        self.reset()
        self.Weight = self.g * self.TotalMass


    def reset(self):
        self.Altitude = 0
        self.Atmosphere_attr()
        self.TotalMass = self.MaxMass
        self.FuelMass = self.initialFuelMass
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