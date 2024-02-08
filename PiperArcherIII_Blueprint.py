from ImportAPCSE import *
AircraftName = "Piper_testv0"



ArcherWings = Wings(AircraftName, PiperArcherIII_Dict)
ArcherHorizontalStabilizer = HorizontalStabilizer(AircraftName, PiperArcherIII_Dict)
ArcherVerticalStabilizer = VerticalStabilizer(AircraftName, PiperArcherIII_Dict)
ArcherFuselage = Fuselage(AircraftName, PiperArcherIII_Dict)
ArcherAircraft = Aircraft(AircraftName, ArcherWings, ArcherHorizontalStabilizer, ArcherFuselage, ArcherVerticalStabilizer)