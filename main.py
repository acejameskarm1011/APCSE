#main
import os
from ImportAPCSE import *
from Plotting import *


#LINES ABOVE CANNOT BE DELETED, unless something breaks

CS1 = 1000 #ft/min
CS2 = [(1000, 10000), 2000] #ft/min
CS3 = [(1000, 10000), (2000, 15000), 500] #ft/min
CS4 = [(250, 10000, "kts"), (300, 25000), (0.7, 30000, "Mach"), 1000]
CSPip = [(76, 10000, "kts"), 1000]
CS5 = [(250, 1000, 10000, "kts"), (300, 2000, 25000, "kts"), (0.7, 500, 30000, "Mach")]
