import os
from ImportAPCSE import *
import numpy as np
from time import *
np.set_printoptions(suppress=True)

from PiperArcherIII_Blueprint import *

MGTOWCase = Mass(PiperArcherIII_Dict, 340, 0, 0, 0)
Motor = [21, 90/12*0.3048]
Inverter = [10, 90/12*0.3048]
BP = [[262., 91/12*0.3048]]
ECU = [86.5, 90/12*0.3048]
BMS = [39.89467616, 90/12*0.3048]
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


deflection_arr = np.array([0, 15, 30, 40]).astype(int)


velocity_arr = np.linspace(66, 125, 100)



ElectricArcherAircraft.V_infty = 90*ElectricArcherAircraft.knots_to_mps
ElectricArcherAircraft.Altitude = 00
ElectricArcherAircraft.Wings.Flaps(15)
ElectricArcherAircraft.Set_RPM(0)
ElectricArcherAircraft.Set_Lift()

# print(ElectricArcherAircraft.Lift)
# print(ElectricArcherAircraft.Drag)
# print(ElectricArcherAircraft.Thrust)



# glideSlope = 5
# RPM = 500
# flapDeg = [0, 15, 30, 40]

# for deg in flapDeg:
#     ElectricArcherAircraft.Wings.Flaps(deg)
#     ElectricArcherAircraft.Set_Lift()
#     print(ElectricArcherAircraft.Drag)

# exit()
testingDescent = Descent(ElectricArcherAircraft)








exit()





colors = ["blue", "green", "yellow", "red"]

plt.figure(figsize=(8,8))
for color, delta in zip(colors, deflection_arr):
    C_L_arr = []
    C_D_arr = []
    for v in velocity_arr:
        ElectricArcherAircraft.Wings.Flaps(delta)
        ElectricArcherAircraft.V_infty = v * ElectricArcherAircraft.knots_to_mps
        ElectricArcherAircraft.Set_Lift()
        C_L_arr.append(ElectricArcherAircraft.Wings.C_L_flaps)
        C_D_arr.append(ElectricArcherAircraft.Wings.C_D_flaps)
    C_L_arr = np.array(C_L_arr)
    C_D_arr = np.array(C_D_arr)
    # plt.plot(velocity_arr, C_L_arr, "-", color = color, label = "$C_L$ - $\delta = ${} deg".format(delta))
    plt.plot(velocity_arr, C_D_arr, "-", color = color, label = "$C_D$ - $\delta = ${} deg".format(delta))
    # twin = plt.gca().twinx()
    # twin.plot(velocity_arr, C_D_arr, "--", color = color, label = "$C_D$ - $\delta = ${} deg".format(delta))

plt.show()