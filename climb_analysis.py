import os
from ImportAPCSE import *
import numpy as np
from time import *
from Plotting.Plotting import CruisePlot, Descent_Plot, TakeOff_Plot, Pattern_Plot
np.set_printoptions(suppress=True)


from PiperArcherIII_Blueprint import ArcherAircraft, ElectricArcherAircraft
from PiperArcherIII_Blueprint import ArcherEngine
import scienceplots


plt.style.use(["science","grid"])
textsize = 18
plt.rcParams.update({'font.size': textsize})




