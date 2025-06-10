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









###########################################################################################
# Inputs Section
missionType = "Piston"
missionType = "Electric"
collected = False
###########################################################################################








figurePath = os.getcwd() + "\\Images_From_Code\\Full_Pattern\\" + date + "\\"

if not os.path.exists(figurePath):
    os.makedirs(figurePath)

Time = np.array([])
Thrust = np.array([])
Lift = np.array([])
Drag = np.array([])
Weight = np.array([])
Percent = np.array([])
V_infty = np.array([])
Altitude = np.array([])
Range = np.array([])
RPM = np.array([])
AOA = np.array([])
Pitch = np.array([])
Time_TO = []
Time_Climb = []
Time_Cruise = []
Time_Descent = []
Time_Landing = []

for i in range(1,4):
    print(i)

    dataTO = pd.read_csv(filepath + "Take-Off{}-lap-{}.csv".format(missionType,i), header=None).to_numpy()
    dataClimb = pd.read_csv(filepath + "Climb{}-lap-{}.csv".format(missionType,i), header=None).to_numpy()
    dataCruise = pd.read_csv(filepath + "Cruise{}-lap-{}.csv".format(missionType,i), header=None).to_numpy()
    dataDescent = pd.read_csv(filepath + "Descent{}-lap-{}.csv".format(missionType,i), header=None).to_numpy()
    dataLanding = pd.read_csv(filepath + "Landing{}-lap-{}.csv".format(missionType,i), header=None).to_numpy()


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


    Time_TO.append(dataTO[0][-1])
    Time_Climb.append(dataClimb[0][-1])
    Time_Cruise.append(dataCruise[0][-1])
    Time_Descent.append(dataDescent[0][-1])
    Time_Landing.append(dataLanding[0][-1])

    Time = np.block([Time, dataTO[0], dataClimb[0], dataCruise[0], dataDescent[0], dataLanding[0]])
    Thrust = np.block([Thrust, dataTO[1], dataClimb[1], dataCruise[1], dataDescent[1], dataLanding[1]])
    Lift = np.block([Lift, dataTO[2], dataClimb[2], dataCruise[2], dataDescent[2], dataLanding[2]])
    Drag = np.block([Drag, dataTO[3], dataClimb[3], dataCruise[3], dataDescent[3], dataLanding[3]])
    Power = np.block([Weight, dataTO[4], dataClimb[4], dataCruise[4], dataDescent[4], dataLanding[4]])
    Weight = np.block([Weight, dataTO[5], dataClimb[5], dataCruise[5], dataDescent[5], dataLanding[5]])
    Percent = np.block([Percent, dataTO[6], dataClimb[6], dataCruise[6], dataDescent[6], dataLanding[6]])
    V_infty = np.block([V_infty, dataTO[7], dataClimb[7], dataCruise[7], dataDescent[7], dataLanding[7]])
    Altitude = np.block([Altitude, dataTO[8], dataClimb[8], dataCruise[8], dataDescent[8], dataLanding[8]])
    Range = np.block([Range, dataTO[9], dataClimb[9], dataCruise[9], dataDescent[9], dataLanding[9]])
    RPM = np.block([RPM, dataTO[10], dataClimb[10], dataCruise[10], dataDescent[10], dataLanding[10]])
    AOA = np.block([AOA, dataTO[-1], dataClimb[-1], dataCruise[-1], dataDescent[-1], dataLanding[-1]])
    Pitch = np.block([Pitch, np.zeros(len(dataTO[-1])), dataClimb[-2], np.zeros(len(dataCruise[-1])), dataDescent[-2], np.zeros(len(dataLanding[-1]))])



if collected:
    fig, ax = plt.subplots(2, 2, constrained_layout = True, figsize = (20,10))

    scale = 1.2
    phases = [Time_TO,Time_Climb,Time_Cruise,Time_Descent]
    phases_label = ["Take-Off", "Climb", "Cruise", "Descent"]
    for phase, label in zip(phases, phases_label):
        for lap in phase:
            ax[0,0].plot([lap/60, lap/60], [Altitude.min(), scale*Altitude.max()], "k--", label = label, lw = 1)
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
    # ax[0,1].legend(fontsize = labelfont)

    for phase, label in zip(phases, phases_label):
        for lap in phase:
            ax[0,1].plot([lap/60, lap/60], [0, Lift.max()*scale], "k--", label = label, lw = 1)
    forces_ax = ax[0,1].get_lines()[:4]
    time_ax = ax[0,1].get_lines()[4:]
    labelLines(time_ax, fontsize = labelfont*0.8, yoffsets=-750*np.ones(12))
    labelLines(forces_ax, fontsize = labelfont*0.8, xvals=[2.3, 6.5, 6.5, 10.7], yoffsets=[100,-100,100,-100])



    for phase, label in zip(phases, phases_label):
        for lap in phase:
            ax[1,0].plot([lap/60, lap/60], [Pitch.min()*scale, Pitch.max()*scale], "k--", label = label, lw = 1)
    time_ax = ax[1,0].get_lines()
    labelLines(time_ax, fontsize = labelfont*0.8)

    ax[1,0].set_ylim(Pitch.min()*scale, Pitch.max()*scale)
    ax_pit = ax[1,0].plot(Time/60, Pitch, "g-", label = "Pitch")
    ax[1,0].set_xlim(left=0)
    ax[1,0].set_xlabel("Time [min]")
    ax[1,0].set_ylabel("Flight Angle [deg]")
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
        for lap in phase:
            ax[1,1].plot([lap/60, lap/60], [Percent.min(), 100], "k--", label = label, lw = 1)
    time_ax = ax[1,1].get_lines()
    labelLines(time_ax, fontsize = labelfont*0.8)
    ax[1,1].set_ylim(Percent.min(), 100)
    ax[1,1].plot(Time/60, Percent, "y-")
    # ax[1,1].set_ylim(bottom = 0)
    ax[1,1].set_xlim(left=0)
    ax[1,1].set_xlabel("Time [min]")
    ax[1,1].set_ylabel(r"Percent [\%]")
    ax[1,1].xaxis.set_major_locator(MaxNLocator(prune='lower'))
    # ax[1,1].xaxis.set_major_locator(MaxNLocator(prune='lower'))
    # ax[1,1].legend(fontsize = labelfont)
    plt.savefig(figurePath + "Full_Pattern_{}.png".format(missionType))
    plt.show()



else:
    figsize = (11,7)
    plt.figure(figsize=figsize)
    scale = 1.2
    phases = [Time_TO,Time_Climb,Time_Cruise,Time_Descent]
    phases_label = ["Climb", "Cruise", "Descent", "Landing/T-O"]
    for phase, label in zip(phases, phases_label):
        for lap in phase:
            plt.plot([lap/60, lap/60], [Altitude.min(), scale*Altitude.max()], "k--", label = label, lw = 1)
    time_ax = plt.gca().get_lines()
    labelfont = 13


    labelLines(time_ax, fontsize = labelfont*0.8)
    ax_alt = plt.plot(Time/60, Altitude, "g-", label = "Altitude")
    plt.ylim((Altitude.min(),scale*Altitude.max()))
    plt.xlim(left=0)
    plt.xlabel("Time [min]")
    plt.ylabel("Altitude [ft]")
    plt.gca().xaxis.set_major_locator(MaxNLocator(prune='lower'))

    twin_00 = plt.gca().twinx()
    ax_vel = twin_00.plot(Time/60, V_infty, "b-", label = "Velocity")
    twin_00.set_ylim(bottom = 0)
    twin_00.set_xlim(left=0)
    twin_00.set_xlabel("Time [min]")
    twin_00.set_ylabel("Velocity [knots]")

    lns = ax_alt+ax_vel
    labs = [l.get_label() for l in lns]
    plt.legend(lns, labs, loc=0, fontsize = labelfont)
    plt.savefig(figurePath + "Full_Pattern_{}_Profile.png".format(missionType))


    plt.figure(figsize=figsize)
    for phase, label in zip(phases, phases_label):
        for lap in phase:
            plt.plot([lap/60, lap/60], [Pitch.min()*scale, Pitch.max()*scale], "k--", label = label, lw = 1)
    time_ax = plt.gca().get_lines()
    labelLines(time_ax, fontsize = labelfont*0.8)

    plt.ylim(Pitch.min()*scale, Pitch.max()*scale)
    ax_pit = plt.plot(Time/60, Pitch, "g-", label = "Pitch")
    plt.xlim(left=0)
    plt.xlabel("Time [min]")
    plt.ylabel("Flight Angle [deg]")
    plt.gca().xaxis.set_major_locator(MaxNLocator(prune='lower'))

    twin_aoa = plt.gca().twinx()
    ax_aoa = twin_aoa.plot(Time/60, AOA, "r-", label  = "Angle of Attack")
    twin_aoa.set_xlim(left=0)
    twin_aoa.set_ylabel("AOA [deg]")

    lns = (ax_pit+ax_aoa)
    labs = [l.get_label() for l in lns]
    plt.legend(lns, labs, loc=0, fontsize = labelfont)
    plt.savefig(figurePath + "Full_Pattern_{}_Angles.png".format(missionType))





    plt.figure(figsize=figsize)
    t = plt.plot(Time/60, Thrust, "b-", label  = "Thrust")
    d = plt.plot(Time/60, Drag, "r-", label  = "Drag")
    l = plt.plot(Time/60, Lift, "g-", label  = "Lift")
    w = plt.plot(Time/60, Weight, color="violet", label  = "Weight")
    plt.ylim(bottom = 0)
    plt.xlim(left=0)
    plt.xlabel("Time [min]")
    plt.ylabel("Forces [lb]")
    plt.gca().xaxis.set_major_locator(MaxNLocator(prune='lower'))
    # plt.legend(fontsize = labelfont)

    for phase, label in zip(phases, phases_label):
        for lap in phase:
            plt.plot([lap/60, lap/60], [0, Lift.max()*scale], "k--", label = label, lw = 1)
    forces_ax = plt.gca().get_lines()[:4]
    time_ax = plt.gca().get_lines()[4:]
    labelLines(time_ax, fontsize = labelfont*0.8, yoffsets=-750*np.ones(12))
    # labelLines(forces_ax, fontsize = labelfont*0.8, xvals=[2.3, 6.5, 6.5, 10.7], yoffsets=[100,-100,100,-100])
    lns = (t + d + l + w)
    labs = [l.get_label() for l in lns]
    plt.legend(lns, labs, loc=0, fontsize = labelfont)
    plt.savefig(figurePath + "Full_Pattern_{}_Forces.png".format(missionType))


    plt.figure(figsize=figsize)
    for phase, label in zip(phases, phases_label):
        for lap in phase:
            plt.plot([lap/60, lap/60], [Percent.min(), 100], "k--", label = label, lw = 1)
    time_ax = plt.gca().get_lines()
    labelLines(time_ax, fontsize = labelfont*0.8)
    plt.ylim(Percent.min(), 100)
    plt.plot(Time/60, Percent, "y-")
    # plt.ylim(bottom = 0)
    plt.xlim(left=0)
    plt.xlabel("Time [min]")
    plt.ylabel(r"Percent [\%]")
    plt.gca().xaxis.set_major_locator(MaxNLocator(prune='lower'))
    # plt.xaxis.set_major_locator(MaxNLocator(prune='lower'))
    # plt.legend(fontsize = labelfont)
    plt.savefig(figurePath + "Full_Pattern_{}_Percent.png".format(missionType))
    plt.show()
os.chdir(image_dir)