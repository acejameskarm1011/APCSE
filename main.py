import os
from ImportAPCSE import *
import numpy as np
from Plotting import TakeOff_Plot, ClimbPlot, Performance_Climb_Plot, Climb_Velocity_FlightAngle_Plot
np.set_printoptions(suppress=True)

from PiperArcherIII_Blueprint import ArcherAircraft
from PiperArcherIII_Blueprint import ElectricArcherAircraft

ArcherTakeOffSim = Take_Off(ArcherAircraft)
ArcherTakeOffSim.Ground_Roll_Sim_ODESolve()
# TakeOff_Plot(ArcherTakeOffSim)


# ElectricArcherTakeOffSim = Take_Off(ElectricArcherAircraft)
# Electricsolution = ElectricArcherTakeOffSim.Ground_Roll_Sim_ODESolve()
# TakeOff_Plot(ElectricArcherTakeOffSim, title="Electric Take-Off Plots")




ArcherClimbSim = Climb(ArcherAircraft)
ArcherClimbSim.Pattern_Work_Climb_Solve()
ClimbPlot(ArcherClimbSim)
# Climb_Velocity_FlightAngle_Plot(ArcherClimbSim)
# print("Archer is at altitude: {}".format(ArcherAircraft.Altitude))
# Performance_Climb_Plot(ArcherAircraft)