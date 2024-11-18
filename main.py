import os
from ImportAPCSE import *
import numpy as np
from time import *
np.set_printoptions(suppress=True)


from Plotting.Plotting import CruisePlot, Descent_Plot, TakeOff_Plot, Pattern_Plot
from PiperArcherIII_Blueprint import ArcherAircraft, ElectricArcherAircraft

from PiperArcherIII_Blueprint import ArcherEngine




# Plot each of the drag components to find where
# n = 100
# ArcherAircraft.Lift = ArcherAircraft.Weight
# V_arr = np.linspace(0, 180, n)*sp.constants.knot
# alt = np.array([0, 1, 2, 3, 700, 2000, 5000, 10000], float)
# MaxC_D = 7

# for h in alt:
#     C_D = []
#     Mach = []
#     ArcherAircraft.Altitude = h
#     for v in V_arr:
#         ArcherAircraft.V_infty = v
#         C_D.append(ArcherAircraft.Coefficients.Get_C_D())
#         Mach.append(ArcherAircraft.Coefficients.Mach)
        
#     plt.plot(Mach, C_D, label = "Altitude: {}ft".format(round(h)))
# # plt.plot([90, 90], [0, MaxC_D], "k--", label = "Max Sim Velocity")
# plt.xlabel(r"$V_{\infty}$ [kts]")
# plt.xlabel(r"M [None]")
# plt.ylabel(r"$C_D$")
# plt.title(r"$C_D$ vs. $V_\infty$")
# plt.title(r"$C_D$ vs. Mach")
# plt.ylim(0,MaxC_D)
# plt.ylim(bottom = 0)
# plt.legend()
# plt.show()
# exit()

# N = 5
# Mass_Arr_Tabs = np.linspace(1912.5, 2550, N)



# Alt_arr = np.array([0, 2000, 4000, 6000, 8000])

# n = 5
# V_arr = np.linspace(0.001,180,n)*sp.constants.knot

# ArcherPropeller = Propeller("Sensenich", "76EM8S14-0-62", 76, 76/8)
# EngTest = PistonEngine("Test", ArcherPropeller)
# EngTest.RPM = 2700
# fig, axes = plt.subplots(1, 1, constrained_layout=True, figsize = (10,6))
# for h in Alt_arr:
#     EngTest.Altitude = h
#     Thrust = []
#     for V in V_arr:
#         Thrust.append(EngTest.Get_Thrust(V, V_arr[-1]))
#     axes.plot(V_arr/sp.constants.knot, Thrust, "--", label = "Actual Thrust at h = {} ft".format(h))
# Thrust_Ideal = EngTest.Power/V_arr
# axes.plot(V_arr/sp.constants.knot, Thrust_Ideal, label = r"Ideal")
# axes.set_xlabel(r"$V_\infty$ [knots]")
# axes.set_ylabel("$T$ [N]")
# axes.set_title(r"Plots of Actual and Idea Thrust vs. $V_\infty$")
# axes.set_ylim((0, 5000))
# plt.legend()
# plt.show()
# exit()





ControlArcher = Control(ElectricArcherAircraft)
ControlArcher.Pattern_Cycle()
V = ControlArcher.Velocity_Arr
T = ControlArcher.Time_Arr
# print(round(ArcherAircraft.FuelPercent*100, 2))

Pattern_Plot(ControlArcher)

exit()




# TakeOff_Plot(ArcherTakeOffSim)


# ElectricArcherTakeOffSim = Take_Off(ElectricArcherAircraft)
# Electricsolution = ElectricArcherTakeOffSim.Ground_Roll_Sim_ODESolve()
# TakeOff_Plot(ElectricArcherTakeOffSim, title="Electric Take-Off Plots")





# ClimbPlot(ArcherClimbSim)
# Climb_Velocity_FlightAngle_Plot(ArcherClimbSim)
# print("Archer is at altitude: {}".format(ArcherAircraft.Altitude))
# Performance_Climb_Plot(ArcherAircraft)