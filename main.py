import os
from ImportAPCSE import *
import numpy as np
from time import *
from Plotting import TakeOff_Plot, ClimbPlot, Performance_Climb_Plot, Climb_Velocity_FlightAngle_Plot
np.set_printoptions(suppress=True)

from PiperArcherIII_Blueprint import ArcherAircraft
from PiperArcherIII_Blueprint import ElectricArcherAircraft


ArcherAircraft.V_infty = 100*sp.constants.knot
Thrust = ArcherAircraft.Drag
P1 = ArcherAircraft.Engine.Power
print(P1)
t1  = time()
ArcherAircraft.Set_Throttle(2200)
t2 = time()
P2 = ArcherAircraft.Engine.Power
print("Time elapsed: {} seconds".format(t2-t1))
print("Error in Power: {}".format(P2-P1))
exit()



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