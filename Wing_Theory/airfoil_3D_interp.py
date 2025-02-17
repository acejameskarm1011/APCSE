import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from time import time

import sys
sys.path.append("\\Airfoils")

import os
current_dir = os.getcwd()


Airfoil_dir = current_dir + "\\Airfoils"

os.chdir(Airfoil_dir)

# np.set_printoptions(suppress=True)

# Utilizes a timer so that costly functions are avoided
# t0 = time()


Reynolds_Numbers = (np.array([50,100,200,500,1000])*1e3).astype(int)

alpha = []
C_l = []


for Re_str in Reynolds_Numbers.astype(str):
    filename = "xf-naca652415-il-" + Re_str + ".csv"
    AirfoilTools = pd.read_csv(filename, header=None)
    AFT_df = pd.DataFrame(AirfoilTools).to_numpy()[10:,:]

    AFT_alpha = AFT_df[1:,0].astype(float)
    AFT_C_l = AFT_df[1:,1].astype(float)

    AOA_min = -9.75
    AOA_max = 13.75

    AFT_ideal = np.arange(AOA_min, AOA_max+0.25, 0.25)
    AFT_C_l = AFT_C_l[AFT_alpha >= AOA_min]
    AFT_alpha = AFT_alpha[AFT_alpha >= AOA_min]
    
    AFT_C_l = AFT_C_l[AFT_alpha <= AOA_max]
    AFT_alpha = AFT_alpha[AFT_alpha <= AOA_max]



    if len(AFT_alpha) < 95:
        list = []
        for i in range(95):
            if AFT_ideal[i] != AFT_alpha[i]:
                if list == [] or list.__contains__(i-1):
                    list.append(i)
                else:
                    AFT_C_l = np.insert(AFT_C_l, list[0], np.linspace(AFT_C_l[list[0]-1], AFT_C_l[list[0]], len(list)+2)[1:-1])
                    list = [i]
                AFT_alpha = np.insert(AFT_alpha, i, AFT_ideal[i])
        AFT_C_l = np.insert(AFT_C_l, list[0], np.linspace(AFT_C_l[list[0]-1], AFT_C_l[list[0]], len(list)+2)[1:-1])
    C_l.append(AFT_C_l)


os.chdir(current_dir)

alpha = AFT_ideal
C_l = np.array(C_l)

def ThreeDim_Interp(Re, **kwargs):
    # if Re < 50000 or Re > 1000000:
    #     raise ValueError("Currently unable to handle Reynolds number outside of 50,000 to 1,000,000")

    if Re < 50000:
        Re = 50000
    if Re > 1000000:
        Re = 1000000

    i = len(Reynolds_Numbers[Reynolds_Numbers <= Re])-1

    if i == C_l.shape[0]-1:
        C_l_Re = C_l[i]
    else:
        C_l_Re = (C_l[i+1]-C_l[i])/(Reynolds_Numbers[i+1]-Reynolds_Numbers[i])*(Re-Reynolds_Numbers[i]) + C_l[i]
    if kwargs.__contains__("C_l"):
        target = kwargs["C_l"]
        y = C_l_Re
        x = alpha
    elif kwargs.__contains__("AOA"):
        target = kwargs["AOA"]
        y = alpha
        x = C_l_Re
    else:
        raise KeyError("Must define a term 'C_l' or 'AOA'")
    j = len(y[y <= target])-1
    result = (x[j+1]-x[j])/(y[j+1]-y[j])*(target-y[j]) + x[j]
    return result



"""
C_l_test = .2
for i in range(int(300)):
    AOA_test = ThreeDim_Interp(150000, C_l = C_l_test)
print(AOA_test)


t1 = time()
print("Took {} s to load".format(t1-t0))
fig, ax = plt.subplots(1, 2, constrained_layout = True, figsize = (12,8))
ax[0].plot(AFT_alpha, AFT_C_l, "r.", label = "Test Data at $Re=1,000,000$")
ax[0].set_xlabel("Angle of Attack [deg]")
ax[0].set_ylabel(r"$C_l$")
ax[0].legend()
ax[0].grid()


ax[1].set_xlabel("Angle of Attack [deg]")
ax[1].set_ylabel(r"error [$\Delta C_l$]")
ax[1].grid()
# ax[1].set_ylim(-100,100)
# fig.savefig("C_l_vs_AOA.png")
# plt.show()





# print(np.round(constants_MAC,5))"""