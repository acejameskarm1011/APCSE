import os
from ImportAPCSE import *
import numpy as np
from time import *
np.set_printoptions(suppress=True)


from Plotting.Plotting import CruisePlot, Descent_Plot, TakeOff_Plot
from PiperArcherIII_Blueprint import ArcherAircraft, ElectricArcherAircraft







from PiperArcherIII_Blueprint import ArcherEngine

n = 1000

# RPM = np.linspace(0,2700, n)
# Power = []
# for rpm in RPM: 
#     ArcherEngine.RPM = rpm
#     Power.append(ArcherEngine.Power)
# Power = np.array(Power)/sp.constants.hp
# print(Power.max())
# print(ArcherEngine.MaxPower/sp.constants.hp)
# plt.plot(RPM, Power)
# plt.xlabel("RPM")
# plt.ylabel("Power [hp]")
# plt.show()
# plt.close()
# exit()





ArcherTakeOffSim = Take_Off(ArcherAircraft)
ArcherTakeOffSim.Ground_Roll_Sim_ODESolve()

ArcherClimbSim = Climb(ArcherAircraft)
ArcherClimbSim.Pattern_Work_Climb_Solve()

ArcherCruiseSim = Cruise(ArcherAircraft)
ArcherCruiseSim.Downwind_Solve_1()

ArcherDescentSim = Descent(ArcherAircraft)
ArcherDescentSim.Approach_Descent()

ArcherLandingSim = Landing(ArcherAircraft)
ArcherLandingSim.Ground_Roll()
TakeOff_Plot(ArcherLandingSim)


exit()




# TakeOff_Plot(ArcherTakeOffSim)


# ElectricArcherTakeOffSim = Take_Off(ElectricArcherAircraft)
# Electricsolution = ElectricArcherTakeOffSim.Ground_Roll_Sim_ODESolve()
# TakeOff_Plot(ElectricArcherTakeOffSim, title="Electric Take-Off Plots")





ClimbPlot(ArcherClimbSim)
# Climb_Velocity_FlightAngle_Plot(ArcherClimbSim)
# print("Archer is at altitude: {}".format(ArcherAircraft.Altitude))
# Performance_Climb_Plot(ArcherAircraft)