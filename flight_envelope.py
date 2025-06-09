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
stallSpeed_seaLevel = 66 * knots_to_mps # knots
C_L_max = Weight / (q(0,stallSpeed_seaLevel)*S_ref)
KTAS_NE = 182



plt.figure(figsize=(5,5))

h_arr = np.arange(0,20000,50)

vInfty_Stall = np.sqrt(Weight/(.5*rho(h_arr)*S_ref*C_L_max))
KTAS_Stall = vInfty_Stall*mps_to_knots

PA28_service_ceiling = 13240.

stretch = 1.1
PsTensor = []
vTensor = []
ArcherAircraft.Set_RPM(2700)
ElectricArcherAircraft.Set_RPM(4000)
ArcherAircraft.Pitch = 0
ArcherAircraft.alpha = 0


hTensor = np.outer(np.ones(len(h_arr)), h_arr).T



# ArcherAircraft.V_infty = 100 * knots_to_mps
# ArcherAircraft.Altitude = 15000
# ArcherAircraft.Set_Lift()
# Ps = (ArcherAircraft.Thrust - ArcherAircraft.Drag) * 100 * knots_to_fps / Weight

for h, Vs in zip(h_arr, KTAS_Stall):
    V_arr = np.linspace(Vs, KTAS_NE, len(h_arr))
    vTensor.append(V_arr.tolist())
    ArcherAircraft.Altitude = h
    for KTAS in V_arr:
        vInfty = KTAS * knots_to_mps
        ArcherAircraft.V_infty = vInfty
        ArcherAircraft.Set_Lift()
        Ps = (ArcherAircraft.Thrust - ArcherAircraft.Drag) * KTAS * knots_to_fps / Weight
        PsTensor.append(Ps)

vTensor = np.array(vTensor)
# print(vTensor[-1])
# exit()
PsTensor = np.array(PsTensor).reshape(vTensor.shape).T
PsTensor[PsTensor < 0] = np.nan



contour = plt.contourf(vTensor, hTensor, PsTensor, levels = 50, cmap="plasma")
bar = plt.colorbar(contour)
bar.set_label("$P_s$ [ft/s]")
# exit()
plt.plot([np.sqrt(Weight/(0.5*rho(PA28_service_ceiling)*S_ref*C_L_max))*mps_to_knots, KTAS_NE], [PA28_service_ceiling, PA28_service_ceiling], label = "POH Service Ceiling")
plt.plot(KTAS_Stall, h_arr)
plt.plot(KTAS_NE*np.ones(h_arr.shape), h_arr)
plt.gca().yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
plt.ylim(bottom = 0)
plt.xlabel(r"KTAS ($V_\infty$) [knots]")
plt.ylabel(r"Altitude ($h$) [ft]")
plt.xlim(0,KTAS_NE*stretch)
plt.gca().xaxis.set_major_locator(MaxNLocator(prune='lower'))
plt.savefig("Flight_Envelope_GnF.png")
plt.show()