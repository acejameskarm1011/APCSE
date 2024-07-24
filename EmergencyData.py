import matplotlib.pyplot as plt 
import scipy as sp
from matplotlib.gridspec import GridSpec
import scienceplots
from Plotting.Descent_Plot import Descent_Plot
import numpy as np


plt.style.use(["science","grid"])
textsize = 18
plt.rcParams.update({'font.size': textsize})


MGTOW_Arr = np.array([1, 0.960784314, 0.921568627, 0.882352941, 0.843137255, 0.799215686])
Model_GR = np.array([824.6105773, 786.8311399, 749.796873, 712.9574493, 676.3192327, 636.8294333])
POH_GR = np.array([1075, 950, 875, 800, 725, 625])

E_Emissios = {
    "CO2" : np.array([0.249098138, 0.23781243, 0.226707294, 0.215692444, 0.204858164, 0.192850171]),
    "CH4" : np.array([2.31E-05, 2.21E-05, 2.10E-05, 2.00E-05, 1.90E-05, 1.79E-05]),
    "N2O" : np.array([3.27E-06, 3.12E-06, 2.97E-06, 2.83E-06, 2.69E-06, 2.53E-06]),
    "Pb"  : np.array([0,0,0,0,0,0])/1.,
}

C_Emissios = {
    "CO2" : np.array([504.942978, 482.0658949, 459.5548452, 437.2268121, 415.0817956, 390.9235959]),
    "CH4" : np.array([7.32591164, 6.994001906, 6.667402728, 6.343458828, 6.022170206, 5.671673527]),
    "N2O" : np.array([0.529185491, 0.50521007, 0.481618256, 0.458218245, 0.435010037, 0.409691993]),
    "Pb"  : np.array([0.122377175, 0.116832722, 0.11137698, 0.105965593, 0.100598563, 0.09474362]),
}

fig, axes = plt.subplots(1, 2, constrained_layout=True, figsize = (11,6))

axes[0].plot(MGTOW_Arr, Model_GR, ".", label = "Code")
axes[0].plot(MGTOW_Arr, POH_GR, "+", label = "POH")

for key in E_Emissios:
    axes[1].plot(MGTOW_Arr, C_Emissios[key], "^", label = "Conv - " +key)
    axes[1].plot(MGTOW_Arr, E_Emissios[key], "+", label = "Elec - " + key)
axes[0].set_xlabel("MGTOW Percent")
axes[1].set_xlabel("MGTOW Percent")

axes[0].set_ylabel("Ground roll [ft]")
axes[1].set_ylabel("Amount of Emissions [g]")
axes[1].set_yscale('log')
fig.suptitle("Take-Off Ground Roll and Emissions")
axes[0].legend(fontsize="small")
axes[1].legend(fontsize="small")
plt.show()
