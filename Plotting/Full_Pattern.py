import os
import sys
image_dir = os.getcwd()
main_dir = image_dir[:-9]
csv_dir = main_dir + ""
os.chdir(main_dir)
sys.path.append(main_dir)

import matplotlib.pyplot as plt
import pandas as pd
from ImportAPCSE import *
import scipy as sp
from matplotlib.gridspec import GridSpec
import scienceplots
from matplotlib.ticker import MaxNLocator
from labellines import labelLine, labelLines


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

missionType = "Conventional"


dataTO = pd.read_csv(filepath + "Take-Off{}.csv".format(missionType), header=None).to_numpy()
dataClimb = pd.read_csv(filepath + "Climb{}.csv".format(missionType), header=None).to_numpy()
dataCruise = pd.read_csv(filepath + "Cruise{}.csv".format(missionType),  header=None).to_numpy()
dataDescent = pd.read_csv(filepath + "Descent{}.csv".format(missionType),  header=None).to_numpy()
dataLanding = pd.read_csv(filepath + "Landing{}.csv".format(missionType),  header=None).to_numpy()


dataTO_attr = dataTO[0,1:].astype(str)
dataClimb_attr = dataClimb[0,1:].astype(str)
dataCruise_attr = dataCruise[0,1:].astype(str)
dataDescent_attr = dataDescent[0,1:].astype(str)
dataLanding_attr = dataLanding[0,1:].astype(str)


dataTO = dataTO[1:,1:].astype(float).T
dataClimb = dataClimb[1:,1:].astype(float).T
dataCruise = dataCruise[1:,1:].astype(float).T
dataDescent = dataDescent[1:,1:].astype(float).T
dataLanding = dataLanding[1:,1:].astype(float).T


Time_TO = dataTO[0][-1]
Time_Climb = dataClimb[0][-1]
Time_Cruise = dataCruise[0][-1]
Time_Descent = dataDescent[0][-1]
Time_Landing = dataLanding[0][-1]


Time = np.block([dataTO[0], dataClimb[0], dataCruise[0], dataDescent[0], dataLanding[0]])
Thrust = np.block([dataTO[1], dataClimb[1], dataCruise[1], dataDescent[1], dataLanding[1]])
Lift = np.block([dataTO[2], dataClimb[2], dataCruise[2], dataDescent[2], dataLanding[2]])
Drag = np.block([dataTO[3], dataClimb[3], dataCruise[3], dataDescent[3], dataLanding[3]])
Weight = np.block([dataTO[4], dataClimb[4], dataCruise[4], dataDescent[4], dataLanding[4]])
Percent = np.block([dataTO[5], dataClimb[5], dataCruise[5], dataDescent[5], dataLanding[5]])
V_infty = np.block([dataTO[6], dataClimb[6], dataCruise[6], dataDescent[6], dataLanding[6]])
Altitude = np.block([dataTO[7], dataClimb[7], dataCruise[7], dataDescent[7], dataLanding[7]])
Range = np.block([dataTO[8], dataClimb[8], dataCruise[8], dataDescent[8], dataLanding[8]])
RPM = np.block([dataTO[9], dataClimb[9], dataCruise[9], dataDescent[9], dataLanding[9]])
AOA = np.block([dataTO[-1], dataClimb[-1], dataCruise[-1], dataDescent[-1], dataLanding[-1]])
Pitch = np.block([np.zeros(len(dataTO[-1])), dataClimb[-2], np.zeros(len(dataCruise[-1])), dataDescent[-2], np.zeros(len(dataLanding[-1]))])



fig, ax = plt.subplots(2, 2, constrained_layout = True, figsize = (10,10))

scale = 1.2


phases = [Time_TO,Time_Climb,Time_Cruise,Time_Descent]
phases_label = ["Take-Off", "Climb", "Cruise", "Descent"]
for phase, label in zip(phases, phases_label):
    ax[0,0].plot([phase/60, phase/60], [Altitude.min(), scale*Altitude.max()], "k--", label = label, lw = 1)
time_ax = ax[0,0].get_lines()
labelfont = 13
labelLines(time_ax, fontsize = labelfont*0.8)


ax_alt = ax[0,0].plot(Time/60, Altitude, "g-", label = "Altitude")

ax[0,0].set_ylim((Altitude.min(),scale*Altitude.max()))
ax[0,0].set_xlim(left=0)
ax[0,0].set_xlabel("Time [min]")
ax[0,0].set_ylabel("Altitude [ft]")
ax[0,0].xaxis.set_major_locator(MaxNLocator(prune='lower'))

twin_00 = ax[0,0].twinx()
ax_vel = twin_00.plot(Time/60, V_infty, "b-", label = "Velocity")
twin_00.set_ylim(bottom = 0)
twin_00.set_xlim(left=0)
twin_00.set_xlabel("Time [min]")
twin_00.set_ylabel("Velocity [knots]")

lns = ax_alt+ax_vel
labs = [l.get_label() for l in lns]
ax[0,0].legend(lns, labs, loc=0, fontsize = labelfont)




ax[0,1].plot(Time/60, Thrust, "b-", label  = "Thrust")
ax[0,1].plot(Time/60, Drag, "r-", label  = "Drag")
ax[0,1].plot(Time/60, Lift, "g-", label  = "Lift")
ax[0,1].plot(Time/60, Weight, color="k", label  = "Weight")
ax[0,1].set_ylim(bottom = 0)
ax[0,1].set_xlim(left=0)
ax[0,1].set_xlabel("Time [min]")
ax[0,1].set_ylabel("Forces [lb]")
ax[0,1].xaxis.set_major_locator(MaxNLocator(prune='lower'))
ax[0,1].legend(fontsize = labelfont)

for phase, label in zip(phases, phases_label):
    ax[0,1].plot([phase/60, phase/60], [0, Drag.max()*scale], "k--", label = label, lw = 1)
time_ax = ax[0,1].get_lines()[:4]
labelLines(time_ax, fontsize = labelfont*0.8)



for phase, label in zip(phases, phases_label):
    ax[1,0].plot([phase/60, phase/60], [Pitch.min()*scale, Pitch.max()*scale], "k--", label = label, lw = 1)
time_ax = ax[1,0].get_lines()
labelLines(time_ax, fontsize = labelfont*0.8)

ax_pit = ax[1,0].plot(Time/60, Pitch, "g-", label = "Pitch")
ax[1,0].set_xlim(left=0)
ax[1,0].set_xlabel("Time [min]")
ax[1,0].set_ylabel("Pitch [lb]")
ax[1,0].xaxis.set_major_locator(MaxNLocator(prune='lower'))
ax[1,0].legend(fontsize = labelfont)

twin_aoa = ax[1,0].twinx()
ax_aoa = twin_aoa.plot(Time/60, AOA, "r-", label  = "Angle of Attack")
twin_aoa.set_xlim(left=0)
twin_aoa.set_ylabel("AOA [deg]")

lns = ax_pit+ax_aoa
labs = [l.get_label() for l in lns]
ax[1,0].legend(lns, labs, loc=0, fontsize = labelfont)


for phase, label in zip(phases, phases_label):
    ax[1,1].plot([phase/60, phase/60], [Percent.min(), 100], "k--", label = label, lw = 1)
time_ax = ax[1,1].get_lines()
labelLines(time_ax, fontsize = labelfont*0.8)

ax[1,1].plot(Time/60, Percent, "y-")
# ax[1,1].set_ylim(bottom = 0)
ax[1,1].set_xlim(left=0)
ax[1,1].set_xlabel("Time [min]")
ax[1,1].set_ylabel(r"Percent [\%]")
ax[1,1].xaxis.set_major_locator(MaxNLocator(prune='lower'))
# ax[1,1].xaxis.set_major_locator(MaxNLocator(prune='lower'))
# ax[1,1].legend(fontsize = labelfont)

plt.show()
os.chdir(image_dir)