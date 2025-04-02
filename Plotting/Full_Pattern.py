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

filepath = "DataFiles\\{}\\"

# dataTO = pd.read_excel("ExcelFiles\\03_20_2025\\Conventional_Full_Pattern_Mission.xlsx".format(""), sheet_name = "Take-Off", header=None).to_numpy()
# dataClimb = pd.read_excel("ExcelFiles\\03_20_2025\\Conventional_Full_Pattern_Mission.xlsx".format(""), sheet_name = "Climb", header=None).to_numpy()
# dataCruise = pd.read_excel("ExcelFiles\\03_20_2025\\Conventional_Full_Pattern_Mission.xlsx".format(""), sheet_name = "Climb", header=None).to_numpy()
# dataDescent = pd.read_excel("ExcelFiles\\03_20_2025\\Conventional_Full_Pattern_Mission.xlsx".format(""), sheet_name = "Climb", header=None).to_numpy()
# dataLanding = pd.read_excel("ExcelFiles\\03_20_2025\\Conventional_Full_Pattern_Mission.xlsx".format(""), sheet_name = "Climb", header=None).to_numpy()

dataTO = pd.read_excel(filepath + "Take-Off.xlsx", header=None).to_numpy()
dataClimb = pd.read_excel(filepath + "Climb.xlsx", header=None).to_numpy()
dataCruise = pd.read_excel(filepath + "Cruise.xlsx",  header=None).to_numpy()
dataDescent = pd.read_excel(filepath + "Descent.xlsx",  header=None).to_numpy()
dataLanding = pd.read_excel(filepath + "Landing.xlsx",  header=None).to_numpy()


dataTO = dataTO[1:,:].astype(float)
dataClimb = dataClimb[1:,:].astype(float)
dataCruise = dataCruise[1:,:].astype(float)
dataDescent = dataDescent[1:,:].astype(float)
dataLanding = dataLanding[1:,:].astype(float)



print()

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