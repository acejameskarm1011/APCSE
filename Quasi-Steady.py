import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from PiperArcherIII_Blueprint import ArcherAircraft




# ArcherAircraft.TotalMass *= 0.84

# RPM = [2265, 2406, 2515, 2700]
# Power_des = []
# # RPM = np.linspace(0,2700, 100)
# PowerRat = []
# for rpm in RPM:
#     ArcherAircraft.Engine.RPM = rpm
#     print("RPM: {}".format(rpm))
#     print("Power rating: {}".format(ArcherAircraft.Engine.PowerRating*100))
#     PowerRat.append(ArcherAircraft.Engine.PowerRating)
# plt.plot(RPM, PowerRat)
# plt.show()




# n = 7000
# Altitude_Arr = np.array([0, 1000, 5000, 10000, 15000], float) # 1000 -> 0.0224586284093120
# Pitch_Arr = np.linspace(-20,0,n)/180*np.pi         # 1000 -> 0.1066374803233
# V_infty = 70*sp.constants.knot

# color = ["r", "y", "g", "k", "b"]

# fig, axs = plt.subplots(1, 1, constrained_layout=True, figsize = (8,6))
# ArcherAircraft.V_infty = V_infty
# ArcherAircraft.Set_RPM(1500)
# ArcherAircraft.Wings.Flaps(40)
# for (h, c) in zip(Altitude_Arr, color):
#     ArcherAircraft.Altitude = h
    
#     # Power_calc = .5*ArcherAircraft.rho*V_infty**3*ArcherAircraft.Wings.S_wing*(ArcherAircraft.Get_C_D()+ArcherAircraft.Wings.Get_C_L()*np.tan(Pitch_Arr))
#     # Power_model = V_infty*ArcherAircraft.Thrust*np.ones(n)
#     Power_calc = []
#     for gamma in Pitch_Arr:
#         ArcherAircraft.Pitch = gamma
#         ArcherAircraft.Set_Lift()    
#         Power_calc.append(V_infty*(ArcherAircraft.Drag+ArcherAircraft.Weight*np.sin(gamma)))
#     Power_calc = np.array(Power_calc)
#     Power_model = ArcherAircraft.Engine.Power*np.ones(n)
    
#     axs.plot(Pitch_Arr*180/np.pi, Power_model/sp.constants.hp, color = c, label = "h = {} ft".format(h))
#     axs.plot(Pitch_Arr*180/np.pi, Power_calc/sp.constants.hp, "--", color = c)
#     plt.plot(Pitch_Arr[np.abs(Power_calc-Power_model).argmin()]*180/np.pi, Power_model[np.abs(Power_calc-Power_model).argmin()]/sp.constants.hp, c+"+", markersize = 3)
# axs.set_xlabel("Pitch [deg]")
# axs.set_ylabel("Power [hp]")
# axs.set_title("Full Throttle Climb Performance")
# plt.legend()
# plt.show()


n = 500
Altitude_Arr = np.array([30, 2000, 4000, 6000, 8000], float) # 1000 -> 0.0224586284093120
# Altitude_Arr = np.array([700], float) # 1000 -> 0.0224586284093120
Velocity_Arr = np.linspace(60,140,n)*sp.constants.knot     # 1000 -> 0.1066374803233
RPM_Arr = np.linspace(0,2700,n)

RPM_Cruise = 2300
V_cruise = 90*sp.constants.knot

color = ["r", "y", "g", "k", "b"]

fig, axs = plt.subplots(1, 2, constrained_layout=True, figsize = (11,6))
ArcherAircraft.Pitch = 0
ArcherAircraft.Set_RPM(RPM_Cruise)
for (h, c) in zip(Altitude_Arr, color):
    ArcherAircraft.Altitude = h
    
    Thrust_Arr = []
    Drag_Arr = []
    for v in Velocity_Arr:
        ArcherAircraft.V_infty = v
        ArcherAircraft.Set_Lift()    
        Thrust_Arr.append(ArcherAircraft.Thrust)
        Drag_Arr.append(ArcherAircraft.Drag)
    Thrust_Arr = np.array(Thrust_Arr)        
    Drag_Arr = np.array(Drag_Arr)
    axs[0].plot(Velocity_Arr[4:]/sp.constants.knot, Thrust_Arr[4:]/Drag_Arr[4:], color = c, label = "h = {} ft".format(h))

    ArcherAircraft.V_infty = V_cruise
    Thrust_Arr = []
    Drag_Arr = []
    for RPM in RPM_Arr:
        ArcherAircraft.Set_RPM(RPM)
        ArcherAircraft.Set_Lift()    
        Thrust_Arr.append(ArcherAircraft.Thrust)
        Drag_Arr.append(ArcherAircraft.Drag)
    
    Thrust_Arr = np.array(Thrust_Arr)        
    Drag_Arr = np.array(Drag_Arr)

    axs[1].plot(RPM_Arr, Thrust_Arr/Drag_Arr, color = c, label = "h = {} ft".format(int(h)))



axs[0].set_title(r"$T/D$ at $RPM={}$".format(RPM_Cruise))
axs[1].set_title(r"$T/D$ at $V_\infty={}$ kts".format(int(V_cruise/sp.constants.knot)))
axs[0].set_xlabel(r"$V_\infty$ [knot]")
axs[1].set_xlabel(r"RPM")
axs[0].set_ylabel("$T/D$")
axs[0].set_ylim(0,2)
fig.suptitle("$T/D$ - Cruise Performance")
plt.legend(fontsize = "small")
plt.show()