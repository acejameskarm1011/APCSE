#main
import os
from ImportAPCSE import *
import numpy as np
from Plotting import TakeOff_Plot
np.set_printoptions(suppress=True)

from PiperArcherIII_Blueprint import ArcherAircraft

ArcherTakeOffSim = Take_Off(ArcherAircraft)

solution = ArcherTakeOffSim.Ground_Roll_Sim_ODESolve()

TakeOff_Plot(ArcherTakeOffSim)
