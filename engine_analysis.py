print("This file is used to validate the engine model.\nEdits are made to the Engine.py file from the work here.")
print("Ideas current as of 03/26 - what is the idle thrust of the engine??")
print("Maybe use the gliding flight path from POH as a way to ensure a proper throttle ratio is achieved - R_m")

import os
from ImportAPCSE import *
import numpy as np
from time import *
np.set_printoptions(suppress=True)


from Plotting.Plotting import CruisePlot, Descent_Plot, TakeOff_Plot, Pattern_Plot

from PiperArcherIII_Blueprint import ArcherAircraft, ElectricArcherAircraft

from PiperArcherIII_Blueprint import ArcherEngine
import scienceplots


plt.style.use(["science","grid"])
textsize = 18
plt.rcParams.update({'font.size': textsize})




dRPM = 50
RPM_arr = np.arange(250, 2700 + dRPM, dRPM)

thrustList = []
dragList = []

ArcherAircraft.Altitude = 700
ArcherAircraft.V_infty = 90 * ArcherAircraft.knots_to_mps



for RPM in RPM_arr:
    ArcherAircraft.Set_RPM(RPM)
    ArcherAircraft.Set_Lift()
    thrustList.append(ArcherAircraft.Thrust)
    dragList.append(ArcherAircraft.Drag)
thrustArr = np.array(thrustList)
dragArr = np.array(dragList)

plt.plot(RPM_arr, thrustArr * ArcherAircraft.N_to_lbf, label = "Thrust")
plt.plot(RPM_arr, dragArr * ArcherAircraft.N_to_lbf, label = "Drag")
plt.legend()
plt.xlabel("RPM Setting")
plt.ylabel("Forces [lb]")
plt.show()