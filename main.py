import os
from ImportAPCSE import *
import numpy as np
from Plotting import TakeOff_Plot
np.set_printoptions(suppress=True)

from PiperArcherIII_Blueprint import ArcherAircraft
from PiperArcherIII_Blueprint import ElectricArcherAircraft

# ArcherTakeOffSim = Take_Off(ArcherAircraft)
# solution = ArcherTakeOffSim.Ground_Roll_Sim_ODESolve()

ElectricArcherTakeOffSim = Take_Off(ElectricArcherAircraft)
Electricsolution = ElectricArcherTakeOffSim.Ground_Roll_Sim_ODESolve()

# TakeOff_Plot(ArcherTakeOffSim)
# TakeOff_Plot(ElectricArcherTakeOffSim)
print(ElectricArcherAircraft.BatteryRatio*100)
