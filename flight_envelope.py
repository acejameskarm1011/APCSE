import os
from ImportAPCSE import *
import numpy as np
from time import *
np.set_printoptions(suppress=True)


from Plotting.Plotting import CruisePlot, Descent_Plot, TakeOff_Plot, Pattern_Plot

from PiperArcherIII_Blueprint import *


import scienceplots

def rho(h):
    return AtmosphereFunctionSI(h, ["rho"])

def q(h, V_infty):
    return 0.5*rho(h)*V_infty**2

def mu(h):
    return AtmosphereFunctionSI(h, ["mu"])

def Re(h,V_infty):
    return rho(h)*V_infty*ArcherAircraft.Wings.c_bar["c_bar"] / mu(h)

S_ref = ArcherAircraft.Wings.S_ref
Weight = ArcherAircraft.Weight
stallSpeed_seaLevel = 60 * knots_to_mps # knots
C_L_max = Weight / (q(0,stallSpeed_seaLevel)*S_ref)
KTAS_NE = 182




h_arr = np.arange(0,20000,100)

vInfty_Stall = np.sqrt(Weight/(.5*rho(h_arr)*S_ref*C_L_max))
KTAS_Stall = vInfty_Stall*mps_to_knots

PA28_service_ceiling = 13240.

stretch = 1.1
PsTensor = []
EPsTensor = []
vTensor = []
ArcherAircraft.Set_RPM(2700)
ElectricArcherAircraft.Set_RPM(2700)

ArcherAircraft.Altitude = 0
ElectricArcherAircraft.Altitude = 0

ArcherAircraft.Pitch = 0
ArcherAircraft.alpha = 0


hTensor = np.outer(np.ones(len(h_arr)), h_arr).T




for h, Vs in zip(h_arr, KTAS_Stall):
    V_arr = np.linspace(Vs, KTAS_NE, len(h_arr))
    vTensor.append(V_arr.tolist())
    ArcherAircraft.Altitude = h
    ElectricArcherAircraft.Altitude = h
    for KTAS in V_arr:
        vInfty = KTAS * knots_to_mps
        ArcherAircraft.V_infty = vInfty
        ElectricArcherAircraft.V_infty = vInfty
        ArcherAircraft.Set_Lift()
        ElectricArcherAircraft.Set_Lift()
        Ps = (ArcherAircraft.Thrust - ArcherAircraft.Drag) * KTAS * knots_to_fps / Weight
        EPs = (ElectricArcherAircraft.Thrust - ElectricArcherAircraft.Drag) * KTAS * knots_to_fps / Weight
        PsTensor.append(Ps)
        EPsTensor.append(EPs)

vTensor = np.array(vTensor)
# print(vTensor[-1])
# exit()
PsTensor = np.array(PsTensor).reshape(vTensor.shape).T
convMax = PsTensor.max()
PsTensor[PsTensor < 0] = np.nan
EPsTensor = np.array(EPsTensor).reshape(vTensor.shape).T
eMax = EPsTensor.max()
EPsTensor[EPsTensor < 0] = np.nan

vmax = convMax
if eMax > convMax:
    vmax = eMax

figsize = (6,7)

plt.figure(figsize=figsize)
plt.plot([np.sqrt(Weight/(0.5*rho(PA28_service_ceiling)*S_ref*C_L_max))*mps_to_knots, KTAS_NE], [PA28_service_ceiling, PA28_service_ceiling], "--", color = "k", label = "POH Service Ceiling")
plt.plot(KTAS_Stall, h_arr, "k--", label = "Stall")
plt.plot(KTAS_NE*np.ones(h_arr.shape), h_arr, "k--", label = "Structural Limit")
lines = plt.gca().get_lines()
labelLines(lines, fontsize = 14, xvals=[119, 68.9, 182], yoffsets=[0,0,10000])
contour = plt.contourf(vTensor, hTensor, PsTensor, levels = 50, cmap="plasma", vmin = 0, vmax = vmax)
bar = plt.colorbar(contour)
bar.set_label("$P_s$ [ft/s]")
plt.gca().yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
plt.ylim(bottom = 0)
plt.xlabel(r"KTAS ($V_\infty$) [knots]")
plt.ylabel(r"Altitude ($h$) [ft]")
plt.xlim(0,KTAS_NE*stretch)
plt.gca().xaxis.set_major_locator(MaxNLocator(prune='lower'))
plt.savefig("Images_From_Code\\Flight_Envelope\\Flight_Envelope_Piston.png")
# plt.show()

plt.figure(figsize=figsize)
plt.plot([np.sqrt(Weight/(0.5*rho(PA28_service_ceiling)*S_ref*C_L_max))*mps_to_knots, KTAS_NE], [PA28_service_ceiling, PA28_service_ceiling], "--", color = "k", label = "POH Service Ceiling")
plt.plot(KTAS_Stall, h_arr, "k--", label = "Stall")
plt.plot(KTAS_NE*np.ones(h_arr.shape), h_arr, "k--", label = "Structural Limit")
lines = plt.gca().get_lines()
labelLines(lines, fontsize = 11, xvals=[119, 68.9, 182], yoffsets=[0,0,10000])
contour = plt.contourf(vTensor, hTensor, EPsTensor, levels = 50, cmap="plasma", vmin = 0, vmax = vmax)
bar = plt.colorbar(contour)
bar.set_label("$P_s$ [ft/s]")
plt.gca().yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
plt.ylim(bottom = 0)
plt.xlabel(r"KTAS ($V_\infty$) [knots]")
plt.ylabel(r"Altitude ($h$) [ft]")
plt.xlim(0,KTAS_NE*stretch)
plt.gca().xaxis.set_major_locator(MaxNLocator(prune='lower'))
plt.savefig("Images_From_Code\\Flight_Envelope\\Flight_Envelope_Electric.png")
# plt.show()