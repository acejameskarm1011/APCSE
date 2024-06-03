import os
from ImportAPCSE import *
import numpy as np
from Plotting import TakeOff_Plot, ClimbPlot
np.set_printoptions(suppress=True)

from PiperArcherIII_Blueprint import ArcherAircraft
from PiperArcherIII_Blueprint import ElectricArcherAircraft

ArcherTakeOffSim = Take_Off(ArcherAircraft)
solution = ArcherTakeOffSim.Ground_Roll_Sim_ODESolve()
# TakeOff_Plot(ArcherTakeOffSim)


# ElectricArcherTakeOffSim = Take_Off(ElectricArcherAircraft)
# Electricsolution = ElectricArcherTakeOffSim.Ground_Roll_Sim_ODESolve()
# TakeOff_Plot(ElectricArcherTakeOffSim)


# Eloss = 100-ElectricArcherTakeOffSim.Percent
Closs = 100-ArcherTakeOffSim.Percent



ArcherAircraft.V_infty = ArcherAircraft.BestClimbSpeed
ArcherClimbSim = Climb(ArcherAircraft)
ArcherClimbSim.Pattern_Work_Climb_FE_Solve()
ClimbPlot(ArcherClimbSim)