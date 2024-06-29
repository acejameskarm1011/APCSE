import os
from ImportAPCSE import *
import numpy as np
from time import *
np.set_printoptions(suppress=True)

from Plotting.Plotting import Descent_Plot
from Plotting.Plotting import CruisePlot
from PiperArcherIII_Blueprint import ArcherAircraft, ElectricArcherAircraft

# ArcherAircraft.Position = np.array([0,0,213.36])
# ArcherAircraft.Pitch = 0
# ArcherAircraft.V_infty = 90*sp.constants.knot



ArcherTakeOffSim = Take_Off(ArcherAircraft)
ArcherTakeOffSim.Ground_Roll_Sim_ODESolve()

ArcherClimbSim = Climb(ArcherAircraft)
ArcherClimbSim.Pattern_Work_Climb_Solve()

ArcherCruiseSim = Cruise(ArcherAircraft)
ArcherCruiseSim.Downwind_Solve_1()

ArcherDescentSim = Descent(ArcherAircraft)
ArcherDescentSim.NoFlaps_Approach(tmax=10)
Descent_Plot(ArcherDescentSim)


exit()




# TakeOff_Plot(ArcherTakeOffSim)


# ElectricArcherTakeOffSim = Take_Off(ElectricArcherAircraft)
# Electricsolution = ElectricArcherTakeOffSim.Ground_Roll_Sim_ODESolve()
# TakeOff_Plot(ElectricArcherTakeOffSim, title="Electric Take-Off Plots")





ClimbPlot(ArcherClimbSim)
# Climb_Velocity_FlightAngle_Plot(ArcherClimbSim)
# print("Archer is at altitude: {}".format(ArcherAircraft.Altitude))
# Performance_Climb_Plot(ArcherAircraft)