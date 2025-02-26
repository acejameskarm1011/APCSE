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



plt.style.use(["science","grid"])
textsize = 18
plt.rcParams.update({'font.size': textsize})


a0 = "18_02_2025"
data = pd.read_excel("ExcelFiles\\18_02_2025\\Conventional_Up_to_Climb{}.xlsx".format(""), sheet_name = "Climb", header=None)
dataframe = pd.DataFrame(data).to_numpy()
Attributes = dataframe[0,:]

dataframe = dataframe[1:,:].astype(float)

Pitch = dataframe[1:,-2]
AOA = dataframe[1:,-1]
Time = dataframe[1:,-4]
Altitude = dataframe[1:,-6]
V_infty = dataframe[1:,6]
Thrust = dataframe[1:,1]
Lift = dataframe[1:,2]
Weight = dataframe[1:,4]




dgamma = 9.81/(V_infty*0.514444)*(Lift/Weight-np.cos(Pitch/180*np.pi)+Thrust/Weight*np.sin(AOA/180*np.pi))/np.pi*180


fig, ax = plt.subplots(2, 2, constrained_layout = True, figsize = (10,10))

twin0 = ax[0,0].twinx()
twin1 = ax[0,1].twinx()
twin2 = ax[1,0].twinx()
twin3 = ax[1,1].twinx()


for i in range(2):
    for j in range(2):
        ax[i,j].plot(Time, Pitch)
        ax[i,j].set_xlabel("Time [s]")
        ax[i,j].set_ylabel(r"Flight Angle ($\gamma$) [deg]")

twin0.plot(Time, Altitude, "--")
twin0.set_ylabel(r"Altitude ($h$) [ft]")

twin1.plot(Time, Thrust, "--")
twin1.set_ylabel(r"Thrust [lb]")

twin2.plot(Time, V_infty, "--")
twin2.set_ylabel(r"Velocity ($V_\infty$) [kts]")


twin3.plot(Time, dgamma, "--")
twin3.set_ylabel(r"Pitch Varience ($\dot{\gamma}$) [deg/s]")

title = "Alpha_is_" + a0 + ".png"
plt.savefig("Images_From_Code\\Pitch_Sensitivity\\" + title)
plt.show()



os.chdir(image_dir)