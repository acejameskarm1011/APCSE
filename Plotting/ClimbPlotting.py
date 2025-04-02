print("WARNING: EXIT STATEMENTS IN CLIMBPLOTTING.PY")
import os
import sys

curdir = os.getcwd()
main_dir = curdir[:-9]


os.chdir(main_dir)
sys.path.append(main_dir)

import matplotlib.pyplot as plt
import pandas as pd
from ImportAPCSE import *
import scipy as sp
from matplotlib.gridspec import GridSpec
import scienceplots

import time
year, month, day, *excer = time.localtime()
if day < 10:
    day = "0" + str(day)
if month < 10:
    month = "0" + str(month)

plt.style.use(["science","grid"])
textsize = 18
plt.rcParams.update({'font.size': textsize})

date = "{}_{}_{}".format(month,day,year)

savefig_dir = main_dir + r"\Images_From_Code\Climb_Performance\\" + date

if not os.path.exists(savefig_dir):
    os.makedirs(savefig_dir)


filepath = "DataFiles\\{}\\".format(date)


dataClimb = pd.read_csv(filepath + "Climb.csv", header=None).to_numpy()

attrClimb = dataClimb[0,1:].astype(str)

dataClimb = dataClimb[1:,1:].astype(float).T


timeArr, ThrustArr, LiftArr, DragArr, WeightArr, PercentArr, VelocityArr, AltArr, RangeArr, RPMArr, PitchArr, AOAArr = dataClimb



fig, ax = plt.subplots(2,2,constrained_layout = True, figsize = (10,10))

ax[0,0].plot(timeArr, ThrustArr, label = "Thrust")
ax[0,0].plot(timeArr, LiftArr, label = "Lift")
ax[0,0].plot(timeArr, DragArr, label = "Drag")
ax[0,0].plot(timeArr, WeightArr, label = "Weight")
ax[0,0].set_xlabel("Time [s]")
ax[0,0].set_ylabel("Forces [lb]")
ax[0,0].legend(fontsize=10)

ax[0,1].plot(timeArr, VelocityArr)
ax[0,1].set_xlabel("Time [s]")
ax[0,1].set_ylabel("Velocity [kts]")


ax[1,0].plot(timeArr, AltArr)
ax[1,0].set_xlabel("Time [s]")
ax[1,0].set_ylabel("Altitude [ft]")

ax[1,1].plot(timeArr, PitchArr)
ax[1,1].set_xlabel("Time [s]")
ax[1,1].set_ylabel("Pitch [deg]")


os.chdir(savefig_dir)
plt.savefig("Climb Plots.png")
plt.show()

os.chdir(curdir)