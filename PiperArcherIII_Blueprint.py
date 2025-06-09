from ImportAPCSE import *
AircraftName = "Piper Archer III"


ArcherWings = Wings(AircraftName, PiperArcherIII_Dict)
ArcherHorizontalStabilizer = HorizontalStabilizer(AircraftName, PiperArcherIII_Dict)
ArcherVerticalStabilizer = VerticalStabilizer(AircraftName, PiperArcherIII_Dict)
ArcherFuselage = Fuselage(AircraftName, PiperArcherIII_Dict)
# ArcherLandingGear = LandingGear()
ArcherPropeller = Propeller("Sensenich", "76EM8S14-0-62", 76, 10.9409) # Spinner Diameter measured from Three View
ArcherEngine = PistonEngine(AircraftName, ArcherPropeller)

##########################################################
# Mass Properties Testing
from scipy import constants
Pilot_Mass = ((150+472)*constants.lb) # ((150+472)*constants.lb)
Rear_Mass = 15*constants.lb
Baggage = 200
##########################################################








ArcherMass = Mass(PiperArcherIII_Dict, 362, 100, Baggage, Tabs=False)

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



ElectricArcherEngine = EMRAX_268_Engine(AircraftName, ArcherPropeller)

MGTOWCase = Mass(PiperArcherIII_Dict, 340, 0, 0, 0)
Motor = [21, 90/12*0.3048]
Inverter = [10, 90/12*0.3048]
BP = [[262.18, 91/12*0.3048]]
ECU = [86.5, 90/12*0.3048]
BMS = [39.8, 90/12*0.3048]
energyDensity = 265
energyDensity_ESS = energyDensity * 0.6238738739 # Wh/kg
MGTOWCase.electrify(*Motor, *Inverter, *ECU, *BMS, energyDensity_ESS, BP)

ElectricArcherAircraft = Aircraft(AircraftName, PiperArcherIII_Dict, 
                          Wings = ArcherWings, 
                          HorizontalStabilizer = ArcherHorizontalStabilizer, 
                          Fuselage = ArcherFuselage, 
                          VerticalStabilizer = ArcherVerticalStabilizer, 
                          Engine = ElectricArcherEngine,
                          Mass = MGTOWCase)