from ImportAPCSE import *
AircraftName = "Piper_testv0"



ArcherWings = Wings(AircraftName, PiperArcherIII_Dict)
ArcherHorizontalStabilizer = HorizontalStabilizer(AircraftName, PiperArcherIII_Dict)
ArcherVerticalStabilizer = VerticalStabilizer(AircraftName, PiperArcherIII_Dict)
ArcherFuselage = Fuselage(AircraftName, PiperArcherIII_Dict)
# ArcherLandingGear = LandingGear()
ArcherPropeller = Propeller("Sensenich", "76EM8S14-0-62", 76, 76/8)
ArcherEngine = PistonEngine(AircraftName, ArcherPropeller)


from scipy import constants
Pilot_Mass = (150+472)*constants.lb
Rear_Mass = 15*constants.lb
Baggage = 25*constants.lb








ArcherMass = Mass(PiperArcherIII_Dict, Pilot_Mass, Rear_Mass, Baggage, Tabs=False)

ArcherAircraft = Aircraft(AircraftName, PiperArcherIII_Dict, 
                          Wings = ArcherWings, 
                          HorizontalStabilizer = ArcherHorizontalStabilizer, 
                          Fuselage = ArcherFuselage, 
                          VerticalStabilizer = ArcherVerticalStabilizer, 
                          Engine = ArcherEngine,
                          Mass = ArcherMass)


AircraftName = "Electric " + AircraftName
EmptyFactor = 1
PiperArcherIII_Dict["Mass"]["EmptyMass"] *= EmptyFactor
ArcherMass = Mass(PiperArcherIII_Dict, Pilot_Mass, Rear_Mass, Baggage, Tabs=False)



ElectricArcherEngine = ElectricEngineTest(AircraftName, ArcherPropeller)
ElectricArcherAircraft = Aircraft(AircraftName, PiperArcherIII_Dict, 
                          Wings = ArcherWings, 
                          HorizontalStabilizer = ArcherHorizontalStabilizer, 
                          Fuselage = ArcherFuselage, 
                          VerticalStabilizer = ArcherVerticalStabilizer, 
                          Engine = ElectricArcherEngine,
                          Mass = ArcherMass)