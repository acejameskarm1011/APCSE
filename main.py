import os
from ImportAPCSE import *
import numpy as np
from time import *
from Plotting import TakeOff_Plot, ClimbPlot, Performance_Climb_Plot, Climb_Velocity_FlightAngle_Plot
np.set_printoptions(suppress=True)

from PiperArcherIII_Blueprint import ArcherAircraft
from PiperArcherIII_Blueprint import ElectricArcherAircraft

ArcherAircraft.Altitude = 5000
ArcherAircraft.V_infty = 110*sp.constants.knot
ArcherAircraft.Aircraft_Forces()
Thrust = ArcherAircraft.Drag
ArcherAircraft.Thrust = Thrust
print(Thrust)
ArcherAircraft.Get_Power()
print(ArcherAircraft.Engine.Power/ArcherAircraft.Engine.MaxPower_SL)



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