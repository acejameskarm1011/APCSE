import os
from ImportAPCSE import *
import numpy as np
from time import *
np.set_printoptions(suppress=True)


from Plotting.Plotting import CruisePlot, Descent_Plot, TakeOff_Plot, Pattern_Plot
from PiperArcherIII_Blueprint import ArcherAircraft, ElectricArcherAircraft

from PiperArcherIII_Blueprint import ArcherEngine


n = 1000
ArcherAircraft.Lift = ArcherAircraft.Weight
V_arr = np.linspace(0, 180, n)*sp.constants.knot
alt = np.arange(0, 12000, 6)

for h in alt:
    for v in V_arr:
        
    plt.plot()






exit()
ControlArcher = Control(ArcherAircraft)
ControlArcher.Pattern_Cycle()
V = ControlArcher.Velocity_Arr
T = ControlArcher.Time_Arr


Pattern_Plot(ControlArcher)








exit()




# TakeOff_Plot(ArcherTakeOffSim)


# ElectricArcherTakeOffSim = Take_Off(ElectricArcherAircraft)
# Electricsolution = ElectricArcherTakeOffSim.Ground_Roll_Sim_ODESolve()
# TakeOff_Plot(ElectricArcherTakeOffSim, title="Electric Take-Off Plots")





ClimbPlot(ArcherClimbSim)
# Climb_Velocity_FlightAngle_Plot(ArcherClimbSim)
# print("Archer is at altitude: {}".format(ArcherAircraft.Altitude))
# Performance_Climb_Plot(ArcherAircraft)