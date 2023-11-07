from Aircraft import Aircraft

class AircraftElectric(Aircraft):
    def __init__(self, AircraftName, CruiseMach, CruiseAltitude, AircraftType, AircraftDictionary, BattDensity = 500) -> None:
        super().__init__(AircraftName, CruiseMach, CruiseAltitude, AircraftType, AircraftDictionary)
        #Delete the next line once we updated the battDensity
        self.BattDensity = BattDensity #
        self.Dictionary_setattr(AircraftDictionary)
        self.BattEnergy = BattDensity * self.EnergyMass
        self.Start = self.BattEnergy
        self.Emergency = None

    def Emergency_Check(self):  # Logic check for climb components
        super().Emergency_Check()
        if self.percent < 0:
            self.Thrust = 0
            self.Power_Thrust = 0
            self.Emergency = "No_Energy"

    def Dictionary_setattr(self, Dictionary):  # We will need to redefine this to account for battery density
        return super().Dictionary_setattr(Dictionary)
    
    def Eta_Thrust(self, eta = .9): # This needs a more robust model
        self.eta = eta


    def GetSC(self):
        self.TSFC = 0
        return 0
    def Battery_Perc(self, show = False):
        percent = round(self.BattEnergy/self.Start*100, 2)
        display = str(percent)
        if percent < 10:
            display = "0" + display[:4] + ' %'
        else:
            display = display[:5] + ' %'
        if show:
            print(display)
        self.percent = percent
        
    def Climb(self, dt=10):
        super().Climb(dt)
        self.Eta_Thrust()
        self.BattEnergy += -self.Power_Thrust * dt / 3600 / self.eta#Wh
        self.Battery_Perc()
    def Cruise(self, dt=10):
        super().Cruise(dt)
        self.Eta_Thrust()
        self.BattEnergy += -self.Power_Thrust * dt / 3600 / self.eta#Wh
        self.Battery_Perc()