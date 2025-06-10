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

ControlArcher = Control(ArcherAircraft)
ControlArcher.Pattern_Cycle()


ControlArcher = Control(ElectricArcherAircraft)
ControlArcher.Pattern_Cycle()

