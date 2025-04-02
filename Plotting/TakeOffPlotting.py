import os
import sys
image_dir = os.getcwd()
main_dir = image_dir[:-9]
excel_dir = main_dir + ""
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

filepath = "DataFiles\\{}\\".format(date)

# dataTO = pd.read_excel("ExcelFiles\\03_20_2025\\Conventional_Full_Pattern_Mission.xlsx".format(""), sheet_name = "Take-Off", header=None).to_numpy()
# dataClimb = pd.read_excel("ExcelFiles\\03_20_2025\\Conventional_Full_Pattern_Mission.xlsx".format(""), sheet_name = "Climb", header=None).to_numpy()
# dataCruise = pd.read_excel("ExcelFiles\\03_20_2025\\Conventional_Full_Pattern_Mission.xlsx".format(""), sheet_name = "Climb", header=None).to_numpy()
# dataDescent = pd.read_excel("ExcelFiles\\03_20_2025\\Conventional_Full_Pattern_Mission.xlsx".format(""), sheet_name = "Climb", header=None).to_numpy()
# dataLanding = pd.read_excel("ExcelFiles\\03_20_2025\\Conventional_Full_Pattern_Mission.xlsx".format(""), sheet_name = "Climb", header=None).to_numpy()

dataTO = pd.read_csv(filepath + "Take-Off.csv", header=None).to_numpy()

attrTO = dataTO[0,1:].astype(str)

dataTO = dataTO[1:,1:].astype(float).T


timeArr, ThrustArr, LiftArr, DragArr, WeightArr, PercentArr, VelocityArr, AltArr, RangeArr, RPMArr, GroundRollArr, AOAArr = dataTO



fig, ax = plt.subplots(2,2,constrained_layout = True, figsize = (10,10))

ax[0,0].plot(VelocityArr, ThrustArr, label = "Thrust")
ax[0,0].plot(VelocityArr, LiftArr, label = "Lift")
ax[0,0].plot(VelocityArr, DragArr, label = "Drag")
ax[0,0].plot(VelocityArr, WeightArr, label = "Weight")
ax[0,0].set_xlabel("Velocity [kts]")
ax[0,0].set_ylabel("Forces [lb]")
ax[0,0].legend()

ax[0,1].plot(timeArr, VelocityArr)
ax[0,1].set_xlabel("Time [s]")
ax[0,1].set_ylabel("Velocity [kts]")



ax[1,0].plot(VelocityArr, AOAArr)

plt.show()
