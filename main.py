#main
from ImportAPCSE import *
from Performance_Classes.AircraftElectric import AircraftElectric
from Plotting import *

main_dir = os.getcwd()

from ImportAPCSE import *

#LINES ABOVE CANNOT BE DELETED, unless something breaks

CruiseMach = .6
CruiseAltitude = 25000

CS1 = 1000 #ft/min
CS2 = [(1000, 10000), 2000] #ft/min
CS3 = [(1000, 10000), (2000, 15000), 500] #ft/min
CS4 = [(250, 10000, "kts"), (300, 25000), (0.7, 30000, "Mach"), 1000]
CS5 = [(250, 1000, 10000, "kts"), (300, 2000, 25000, "kts"), (0.7, 500, 30000, "Mach")]


ERJ175 = AircraftConventional("ERJ175", CruiseMach, CruiseAltitude, "Embraer_175", Embraer175_Dict)
ERJ175_EV = AircraftElectric("ERJ175 EV", CruiseMach, CruiseAltitude, "Embraer_175", Embraer175_Dict)
PA28 = AircraftConventional("PA28", 0.18, 8500, "Piper_Archer_III", PA28_Dict['PA'])

ERJ175_control = Control(ERJ175, CS4)
ERJ175_EV_control = Control(ERJ175_EV, CS4)

ERJ175_control.TimestepBeta(dt = 1)
ERJ175_EV_control.TimestepBeta(dt = 1)

MyCurrentPlot(ERJ175_EV_control, "Range up to 25,000 ft")
MyCurrentPlot(ERJ175_control, "Range up to 25,000 ft")

print(f'C_D ranges from {ERJ175_control.C_DArr.min()} to {ERJ175_control.C_DArr.max()} ')