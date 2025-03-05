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


vInfty = 76 # knots
vInfty *= ArcherAircraft.knots_to_mps
ArcherAircraft.V_infty = vInfty 
ArcherAircraft.Altitude = 700

ArcherAircraft.Set_Lift()

flightAngle = 5/180*np.pi
i=0
while i < 20:
    ArcherAircraft.Set_Lift()

    # print(flightAngle/np.pi*180)
    flightAngle = np.arcsin((ArcherAircraft.Thrust*np.cos(ArcherAircraft.alpha)-ArcherAircraft.Drag)/ArcherAircraft.Weight)
    ArcherAircraft.Pitch = flightAngle
    # print(flightAngle/np.pi*180)
    i+=1

print("Flight Angle at {} ft: ".format(ArcherAircraft.Altitude), round(flightAngle/np.pi*180, 2), "deg")
print("AOA at {} ft: ".format(ArcherAircraft.Altitude), round(ArcherAircraft.alpha/np.pi*180, 2), "deg")
print("m dv_dt: ", ArcherAircraft.Thrust*np.cos(ArcherAircraft.alpha)-ArcherAircraft.Drag-ArcherAircraft.Weight*np.sin(flightAngle))
print("m V dgamma_dt: ", ArcherAircraft.Lift + ArcherAircraft.Thrust*np.sin(ArcherAircraft.alpha)-ArcherAircraft.Weight*np.cos(flightAngle))

"""
Well it seems that for the zero case of velocity change, then there needs to be some kind of increase of drag from the elevator to 
prevent any more increase in the dgamma_dt
"""

climbRateFPM_arr = np.array([730, 684, 620, 590])

def get_POH_flightAngle(h_p):
    """
    Function that returns the POH expected flight path angle based on the current altitude
    The aircraft flies at Gross weight, Full Throttle, 76 KIAS
    """
    vInfty = 76 * ArcherAircraft.knots_to_mps
    climbRateFPM_arr = np.array([730, 684, 620, 590])
    h_p_arr = np.array([0,1,2,3])*1e3
    a, b = np.polyfit(h_p_arr, climbRateFPM_arr, 1)
    climbRateFPM = a*h_p+b
    climbRate = climbRateFPM * ArcherAircraft.ft_to_m / 60
    flightAngle = np.arcsin(climbRate/vInfty)
    plt.plot(h_p_arr, climbRateFPM_arr, ".")
    plt.plot(h_p_arr, h_p_arr*a+b)
    plt.show()
    return flightAngle



print("PA28-181 flight angle expected", get_POH_flightAngle(0)/np.pi*180)

flightAngle = 2. / 180 * np.pi
ArcherAircraft.V_infty = vInfty
currentClimbRate = np.sin(flightAngle)*vInfty
h_p_arr = np.arange(5,701).astype(float)


ArcherAircraft.Pitch = flightAngle
drag_arr = []
thrust_arr = []
lift_arr = []
dv_dt = []
alpha_arr = []
for h_p in h_p_arr:
    ArcherAircraft.Altitude = h_p
    ArcherAircraft.Set_Lift()
    thrust_arr.append(ArcherAircraft.Thrust*ArcherAircraft.N_to_lbf)
    drag_arr.append(ArcherAircraft.Drag*ArcherAircraft.N_to_lbf)
    drag_arr.append(ArcherAircraft.Drag*ArcherAircraft.N_to_lbf)
    alpha_arr.append(ArcherAircraft.alpha/np.pi*180)
    dv_dt.append((ArcherAircraft.Thrust*np.cos(ArcherAircraft.alpha)-ArcherAircraft.Drag-ArcherAircraft.Weight*np.sin(flightAngle))/(ArcherAircraft.Weight/ArcherAircraft.g))

print("Ideal climb thrust: ", round(132390/vInfty*ArcherAircraft.N_to_lbf, 4), "lb")
vInfty_arr = np.arange(1,180)*ArcherAircraft.knots_to_mps
idealThrust = 132390/vInfty_arr*ArcherAircraft.N_to_lbf
actualThrust = []
for v in vInfty_arr:
    ArcherAircraft.V_infty = v
    actualThrust.append(ArcherAircraft.GetTotalThrust()*ArcherAircraft.N_to_lbf)
actualThrust = np.array(actualThrust)
plt.plot(vInfty_arr*ArcherAircraft.mps_to_knots, idealThrust, label = "Ideal thrust")
plt.plot(vInfty_arr*ArcherAircraft.mps_to_knots, actualThrust, label = "Actual thrust")
plt.xlabel("Velocity [knots]")
plt.ylabel("Thrust [lb]")
plt.title("Ideal and actual thrust")
plt.ylim(0, actualThrust.max())
plt.legend()
plt.show()


plt.plot(drag_arr, h_p_arr, label = "Drag")
plt.plot(thrust_arr, h_p_arr, label = "Thrust")
plt.xlabel("Forces [lb]")
plt.ylabel("Altitdue [ft]")
plt.legend()
plt.title("Thrust and Drag during climb")
plt.show()

plt.plot(dv_dt, h_p_arr)
plt.xlabel("Speed rate change [m/s$^2$]")
plt.ylabel("Altitdue [ft]")
plt.title("Acceleration over altitude")
plt.show()



"""
Notes: 
 - Check out the GA textbook equation for GE induced drag for different GE equation

 - Patchwork the thrust plot such that the ideal thrust case is met at 76 knots rather than

 - What is drag required based on aircraft, compare to actual

 - Message Eric about span eff
 - Lift on plot

"""