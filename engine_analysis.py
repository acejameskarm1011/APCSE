print("This file is used to validate the engine model.\nEdits are made to the Engine.py file from the work here.")
print("Ideas current as of 03/26 - what is the idle thrust of the engine??")
print("Maybe use the gliding flight path from POH as a way to ensure a proper throttle ratio is achieved - R_m")

import os
from ImportAPCSE import *
import numpy as np
from time import *
np.set_printoptions(suppress=True)


from Plotting.Plotting import CruisePlot, Descent_Plot, TakeOff_Plot, Pattern_Plot


from PiperArcherIII_Blueprint import *


MGTOWCase = Mass(PiperArcherIII_Dict, 340, 0, 0, 0)
Motor = [21, 90/12*0.3048]
Inverter = [10, 90/12*0.3048]
BP = [[262., 91/12*0.3048]]
ECU = [86.5, 90/12*0.3048]
BMS = [39.9, 90/12*0.3048]
energyDensity = 265
energyDensity_ESS = energyDensity * 0.6238738739 # Wh/kg
MGTOWCase.electrify(*Motor, *Inverter, *ECU, *BMS, energyDensity_ESS, BP)

ElectricArcherAircraft = Aircraft(AircraftName, PiperArcherIII_Dict, 
                          Wings = ArcherWings, 
                          HorizontalStabilizer = ArcherHorizontalStabilizer, 
                          Fuselage = ArcherFuselage, 
                          VerticalStabilizer = ArcherVerticalStabilizer, 
                          Engine = ElectricArcherEngine,
                          Mass = MGTOWCase)

import scienceplots


plt.style.use(["science","grid"])
textsize = 18
plt.rcParams.update({'font.size': textsize})




# dRPM = 50
# RPM_arr = np.arange(250, 2700 + dRPM, dRPM)

# thrustList = []
# dragList = []

# ArcherAircraft.Altitude = 700
# ArcherAircraft.V_infty = 90 * ArcherAircraft.knots_to_mps



# for RPM in RPM_arr:
#     ArcherAircraft.Set_RPM(RPM)
#     ArcherAircraft.Set_Lift()
#     thrustList.append(ArcherAircraft.Thrust)
#     dragList.append(ArcherAircraft.Drag)
# thrustArr = np.array(thrustList)
# dragArr = np.array(dragList)

# plt.plot(RPM_arr, thrustArr * ArcherAircraft.N_to_lbf, label = "Thrust")
# plt.plot(RPM_arr, dragArr * ArcherAircraft.N_to_lbf, label = "Drag")
# plt.legend()
# plt.xlabel("RPM Setting")
# plt.ylabel("Forces [lb]")
# plt.show()



h_arr = np.arange(0, 12e3, 2000)

V_arr = np.arange(0, 183, 1)

plt.figure(figsize=(10,7))
ArcherAircraft.Altitude = 0
ArcherAircraft.V_infty = 0
ArcherAircraft.alpha = 0
ArcherAircraft.Pitch = 0
ArcherAircraft.Set_RPM(2700)
for h in h_arr:
    thrustList = []
    ArcherAircraft.Altitude = h
    for KTAS in V_arr:
        vInfty = KTAS * knots_to_mps
        ArcherAircraft.V_infty = vInfty
        ArcherAircraft.Aircraft_Forces()
        thrustList.append(ArcherAircraft.Thrust * N_to_lbf)
    label = "Interpolated - $h = {},000$ ft".format(str(h)[0])
    if h == 0:
        label = "Interpolated - SL"
    elif h >= 10000:
        label = "Interpolated - $h = {},000$ ft".format(str(h)[:2])

    plt.plot(V_arr, thrustList, "--", label = label)
plt.plot(V_arr[1:], ArcherAircraft.Engine.MaxPower / (V_arr[1:]*knots_to_mps)*N_to_lbf, "r-", label = "Ideal Thrust")
plt.ylim(0,1200)
plt.xlabel("True Airspeed [Knots]")
plt.ylabel("Thrust Force [lb]")
plt.xlim(0,182)
plt.legend(fontsize=12)
plt.savefig("Images_From_Code\\Engine\\Ideal_vs_Interpolated.png")
# plt.show()
plt.close()


h_arr = np.linspace(0,15000, 100)
plt.figure(figsize=(8,8))

Power_arr = []
for h in h_arr:
    ArcherAircraft.Altitude = h
    Power_arr.append(ArcherAircraft.Engine.Get_Power() * watt_to_hp)
plt.plot(Power_arr, h_arr)
plt.xlabel("Power [hp]")
plt.ylabel("Altitude [ft]")
plt.show()