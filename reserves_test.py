import os
from ImportAPCSE import *
import numpy as np
from time import *
np.set_printoptions(suppress=True)


from Plotting.Plotting import CruisePlot, Descent_Plot, TakeOff_Plot, Pattern_Plot

from PiperArcherIII_Blueprint import *
import scienceplots


plt.style.use(["science","grid"])
textsize = 18
plt.rcParams.update({'font.size': textsize})

# controlArcher = Control(ElectricArcherAircraft)

reserves = Cruise(ArcherAircraft)


vInfty_upper = 70
vInfty_lower = 69

l = [vInfty_lower, vInfty_upper]
for vInfty in l:
    reserves.Reserves(vInfty)
    print(reserves.Percent)
    reserves.reset()
    ArcherAircraft.reset(type = "else")