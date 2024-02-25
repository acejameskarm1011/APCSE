from ImportAPCSE import *
AircraftName = "Piper_testv0"



ArcherWings = Wings(AircraftName, PiperArcherIII_Dict)
ArcherHorizontalStabilizer = HorizontalStabilizer(AircraftName, PiperArcherIII_Dict)
ArcherVerticalStabilizer = VerticalStabilizer(AircraftName, PiperArcherIII_Dict)
ArcherFuselage = Fuselage(AircraftName, PiperArcherIII_Dict)
ArcherPropeller = Propeller("Sensenich", "76EM8S14-0-62", 76, 76/8)
ArcherEngine = EngineTest(AircraftName, ArcherPropeller)
ArcherAircraft = Aircraft(AircraftName, ArcherWings, ArcherHorizontalStabilizer, ArcherFuselage, ArcherVerticalStabilizer, ArcherEngine)
ArcherAircraft.Dictionary_setattr(PiperArcherIII_Dict["Performance"])

