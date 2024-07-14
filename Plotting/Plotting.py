import matplotlib.pyplot as plt
from ImportAPCSE import *
import time
import os
main_dir = os.getcwd()
image_dir = main_dir + "\\Images_From_Code"
import scipy as sp
from matplotlib.gridspec import GridSpec
import scienceplots
from Plotting.Descent_Plot import Descent_Plot


plt.style.use(["science","grid"])
textsize = 18
plt.rcParams.update({'font.size': textsize})

def Pattern_Plot(Control, title = "Pattern Work Plot"):
    """
    Using the Control Class, we plot the state of the aircraft through a loop through the pattern
    """
    if isinstance(Control.Aircraft.Engine, ElectricEngineTest):
        title = "Electric " + title
    linewidth = 3
    time = Control.Time_Arr / 60 # min
    Distance = Control.Position_x_Arr / sp.constants.nautical_mile
    Altitude = Control.Position_z_Arr / sp.constants.foot
    V_infty = Control.Velocity_Arr / sp.constants.knot
    Pitch = Control.Pitch_Arr / np.pi*180
    Lift = Control.Lift_Arr # N
    Thrust = Control.Thrust_Arr # N
    Weight = Control.Weight_Arr # N
    Drag = Control.Drag_Arr # N
    RPM = Control.RPM_Arr # rev/min
    Percent = Control.Percent_Arr 

    # Alt v Dist + 
    # V_infty v time + 
    # Pitch v time +
    # Lift v time + 
    # Thrust v time + 
    # Lift/Weight v time
    # Drag v time + 
    # RPM v time
    # Percent v time


    fig, axes = plt.subplots(3, 3, constrained_layout=True, figsize = (14,8))
    axes[0,0].plot(Distance, Altitude, "g-", linewidth=linewidth)
    axes[0,0].set_ylabel(r"Altitude - $h$ [ft]")
    axes[0,0].set_xlabel(r"Distance - $d$ [nmi]")
    axes[0,0].set_xlim((0,Distance.max()))


    axes[0,1].plot(time, V_infty, linewidth=linewidth)
    axes[0,1].set_ylabel(r"Velocity - $V_\infty$ [kts]")
    axes[0,1].set_xlim((0,time.max()))

    axes[0,2].plot(time, Pitch, linewidth=linewidth)
    axes[0,2].set_ylabel(r"Pitch - $\gamma$ [deg]")
    axes[0,2].set_xlim((0,time.max()))
    axes[0,2].set_ylim(top = 10)

    axes[1,0].plot(time, Lift, "g", linewidth=linewidth)
    axes[1,0].set_ylabel(r"Lift - $L$ [N]")
    axes[1,0].set_xlim((0,time.max()))

    axes[1,1].plot(time, Thrust, "r-", linewidth=linewidth)
    axes[1,1].set_ylabel(r"Thrust - $T$ [N]")
    axes[1,1].set_xlim((0,time.max()))

    axes[1,2].plot(time, Lift/Weight, "g", linewidth=linewidth)
    axes[1,2].set_ylabel(r"$L/W$ [N/a]")
    axes[1,2].set_xlim((0,time.max()))

    axes[2,0].plot(time, Drag, "r--", linewidth=linewidth)
    axes[2,0].set_ylabel(r"Drag - $D$ [N]")
    axes[2,0].set_xlim((0,time.max()))


    axes[2,1].plot(time, RPM, "y--", linewidth=linewidth)
    axes[2,1].set_ylabel(r"RPM [rev/min]")
    axes[2,1].set_xlim((0,time.max()))

    axes[2,2].plot(time, Percent, "y--", linewidth=linewidth)
    axes[2,2].set_ylabel("Percent [\\%]")
    axes[2,2].set_xlim((0,time.max()))
    
    
    axes[0,2].set_xlabel(r"Time - $t$ [min]")
    axes[0,1].set_xlabel(r"Time - $t$ [min]")
    axes[1,2].set_xlabel(r"Time - $t$ [min]")
    axes[1,1].set_xlabel(r"Time - $t$ [min]")
    axes[1,0].set_xlabel(r"Time - $t$ [min]")
    axes[2,2].set_xlabel(r"Time - $t$ [min]")
    axes[2,1].set_xlabel(r"Time - $t$ [min]")
    axes[2,0].set_xlabel(r"Time - $t$ [min]")

    # axes[1,0].set_ylim((0, Thrust.max()*1.2))
    # axes[1,1].set_ylim((0, Percent.max()*1.2))
    fig.suptitle(title)
    plt.savefig(image_dir + "\\Pattern_Performance\\" + title.replace(" ", "_") + ".png")
    plt.show()
    



def TakeOff_Plot(TakeOff, title = "Take-Off Plots"):
    """
    Using the TakeOff class, we can use the data stored within it in order to plot how each of the paramters are changing over time.

    Parameters
    ----------
    TakeOff : Instance of the TakeOff class

    Notes: Images with be stored in the Take_Off_Performance directory in Images_From_Code
    """
    if isinstance(TakeOff.Aircraft.Engine, ElectricEngineTest):
        title = "Electric " + title
    linewidth = 3
    V_infty = TakeOff.Velocity_List / sp.constants.knot
    Distance = TakeOff.Position_x / sp.constants.foot
    time = TakeOff.Time_List
    V_NE = TakeOff.Aircraft.NeverExceedSpeed
    Thrust = TakeOff.Thrust_List
    Percent = TakeOff.Percent_List
    Lift = TakeOff.Lift_List
    Drag = TakeOff.Drag_List

    fig, axs = plt.subplots(3, 2, constrained_layout=True, figsize = (14,8))
    axs[0,0].plot(time, Distance, "g-", linewidth=linewidth)
    axs[0,0].set_ylabel(r"Ground Roll - $d$ [ft]")
    axs[0,0].set_xlim((0,time.max()))
    axs[0,1].plot(time, V_infty, linewidth=linewidth)
    axs[0,1].set_ylabel(r"Velocity - $V_\infty$ [kts]")
    axs[0,1].set_xlim((0,time.max()))
    axs[1,0].plot(time, Thrust, "r-", linewidth=linewidth)
    axs[1,0].set_ylabel(r"Thrust - $T$ [N]")
    axs[1,0].set_xlim((0,time.max()))
    axs[1,1].plot(time, Percent, "y--", linewidth=linewidth)
    axs[1,1].set_ylabel(r"Percent [\\%]")
    axs[1,1].set_xlim((0,time.max()))
    axs[2,0].plot(time, Lift, "g", linewidth=linewidth)
    axs[2,0].set_ylabel(r"Lift - $L$ [N]")
    axs[2,0].set_xlim((0,time.max()))
    axs[2,1].plot(time, Drag, "r--", linewidth=linewidth)
    axs[2,1].set_ylabel(r"Drag - $D$ [N]")
    axs[2,1].set_xlim((0,time.max()))
    axs[2,1].set_xlabel(r"Time - $t$ [s]")
    axs[2,0].set_xlabel(r"Time - $t$ [s]")
    axs[1,0].set_ylim((0, Thrust.max()*1.2))
    axs[1,1].set_ylim((0, Percent.max()*1.2))
    fig.suptitle(title)
    plt.savefig(image_dir + r"\\Take_Off_Performance\\" + title.replace(" ", "_") + ".png")
    plt.show()

def ClimbPlot(Climb, title = "Climb Plots"):
    """
    Using the Climb class, we can use the data stored within it in order to plot how each of the paramters are changing over time.

    Parameters
    ----------
    Climb : Instance of the Climb class

    Notes: Images with be stored in the Take_Off_Performance directory in Images_From_Code
    """
    if isinstance(Climb.Aircraft.Engine, ElectricEngineTest):
        title = "Electric " + title
    linewidth = 3
    exitpart = -50

    V_infty = Climb.Velocity_List[:exitpart] / sp.constants.knot
    Pitch = Climb.Pitch_List[:exitpart]
    Distance = Climb.Position_x[:exitpart] / sp.constants.foot
    time = Climb.Time_List[:exitpart]
    V_NE = Climb.Aircraft.NeverExceedSpeed
    Altitude = Climb.Altitude_List[:exitpart]
    Percent = Climb.Percent_List[:exitpart]
    Lift = Climb.Lift_List[:exitpart]
    Drag = Climb.Drag_List[:exitpart]

    Thrust = Climb.Thrust_List[:exitpart]

    fig, axs = plt.subplots(3, 2, constrained_layout=True, figsize = (14,8))
    axs[0,0].plot(time, Pitch*180/np.pi, "g-", linewidth=linewidth)
    axs[0,0].set_ylabel(r"Pitch - $\gamma$ [deg]")
    axs[0,0].set_xlim((0,time.max()))
    axs[0,1].plot(time, V_infty, linewidth=linewidth)
    axs[0,1].set_ylabel(r"Velocity - $V_\infty$ [kts]")
    axs[0,1].set_xlim((0,time.max()))
    axs[1,0].plot(time, Altitude, "r-", linewidth=linewidth)
    axs[1,0].set_ylabel(r"Altitude - $h$ [ft]")
    axs[1,0].set_xlim((0,time.max()))
    axs[1,1].plot(time, Percent, "y--", linewidth=linewidth)
    axs[1,1].set_ylabel(r"Percent [\%]")
    axs[1,1].set_xlim((0,time.max()))
    axs[2,0].plot(time, Lift, "g", linewidth=linewidth)
    axs[2,0].set_ylabel(r"Lift - $L$ [N]")
    axs[2,0].set_xlim((0,time.max()))
    axs[2,1].plot(time, Drag, "r--", linewidth=linewidth)
    axs[2,1].set_ylabel(r"Drag - $D$ [N]")
    axs[2,1].set_xlim((0,time.max()))
    axs[2,1].set_xlabel(r"Time - $t$ [s]")
    axs[2,0].set_xlabel(r"Time - $t$ [s]")
    # axs[1,0].set_ylim((0, Altitude.max()*1.2))
    axs[1,1].set_ylim((0, Percent.max()*1.2))
    fig.suptitle(title)
    plt.savefig(image_dir + r"\\Climb_Performance\\" + title.replace(" ", "_")+".png")
    plt.show()


def Climb_Velocity_FlightAngle_Plot(Climb, title = "Aircraft Climb Velocity Characteristics"):
    if isinstance(Climb.Aircraft.Engine, ElectricEngineTest):
        title = "Electric " + title
    linewidth = 3
    V_x = Climb.Velocity_x / sp.constants.knot
    V_z = Climb.Velocity_z / sp.constants.knot
    V_infty = np.sqrt(Climb.Velocity_x**2 + Climb.Velocity_z**2) / sp.constants.knot
    Pitch = np.array(Climb.Pitch_List)/np.pi*180
    time = Climb.Time_List
    Altitude = Climb.Altitude_List
    Percent = Climb.Percent_List

    fig, axs = plt.subplots(2, 2, constrained_layout=True, figsize = (10,7))
    axs[0,0].plot(time, Pitch, "y-", linewidth=linewidth)
    axs[0,0].set_ylabel("Flight Angle $\\gamma$ [deg]")
    axs[0,1].plot(time, V_x, "b-", linewidth=linewidth)
    axs[0,1].set_ylabel("$V_x$ [m/s]")
    axs[1,1].plot(time, V_z, "g-", linewidth=linewidth)
    axs[1,1].set_ylabel("$V_z$ [m/s]")
    axs[1,1].set_xlabel("Time [s]")
    axs[1,0].plot(time, V_infty, "k-", linewidth=linewidth)
    axs[1,0].set_ylabel("$V_\\infty$ [m/s]")
    axs[1,0].set_xlabel("Time [s]")
    fig.suptitle(title)
    plt.savefig(image_dir + r"\\Climb_Performance\\" + title.replace(" ", "_")+".png")
    plt.show()


def Performance_Climb_Plot(Aircraft, title = "Climb Performance"):
    if isinstance(Aircraft.Engine, ElectricEngineTest):
        title = "Electric " + title
    V_NE = Aircraft.NeverExceedSpeed
    V_infty = np.linspace(0,V_NE, 2000)
    Aircraft.V_infty = V_infty
    Aircraft.Aircraft_Forces()
    Lift = Aircraft.Lift
    Drag = Aircraft.Drag
    Thrust = Aircraft.Thrust
    Weight = Aircraft.Weight
    V = V_infty * Aircraft.mps_to_knots

    Data1 = Lift/Weight
    Data2 = (Thrust-Drag)/Weight

    fig, axs = plt.subplots(1, 2, constrained_layout=True, figsize = (8,6))
    axs[0].plot(V, Data1)
    axs[0].set_xlabel("Velocity - $V_\\infty$ [kts]")
    axs[0].set_ylabel("Ratio")
    axs[0].set_title("Plot of $\\frac{L}{W}$")
    axs[1].plot(V, Data2)
    axs[1].set_xlabel("Velocity - $V_\\infty$ [kts]")
    axs[1].set_title("Plot of $\\frac{T-D}{W}$")
    Altitude = str(Aircraft.Altitude)

    Vel1 = V.copy()
    Vel2 = V.copy()
    Vel1[Data1 > 1] = 0
    Vel2[Data2 < 0] = 0
    
    BestClimbVel1 = Vel1.max()
    BestClimbVel2 = Vel2.max()
    print("The best velocity for maximum lift is {}".format(BestClimbVel1))
    print("The best velocity for minimum drag is {}".format(BestClimbVel2))
    
    title = " ".join([title, "at", Altitude[:-3]+","+Altitude[-3:], "ft"])
    fig.suptitle(title)
    plt.savefig(image_dir + r"\\Climb_Performance\\" + title.replace(" ", "_") +".png")
    plt.show()
    plt.pause(3)
    plt.close()

    Aircraft.V_infty = 0.



def CruisePlot(Cruise, title = "Cruise Plots"):
    """
    Using the Cruise class, we can use the data stored within it in order to plot how each of the paramters are changing over time.

    Parameters
    ----------
    Cruise : Instance of the Cruise class

    Notes: Images with be stored in the Take_Off_Performance directory in Images_From_Code
    """
    if isinstance(Cruise.Aircraft.Engine, ElectricEngineTest):
        title = "Electric " + title
    linewidth = 3
    V_infty = Cruise.Velocity_List / sp.constants.knot
    Distance = Cruise.Position_x / sp.constants.nautical_mile
    RPM = Cruise.RPM_List
    time = Cruise.Time
    Thrust = Cruise.Thrust_List
    Percent = Cruise.Percent_List
    Lift = Cruise.Lift_List
    Drag = Cruise.Drag_List
    RPM = Cruise.RPM_List

    Thrust = Cruise.Thrust_List

    fig, axs = plt.subplots(3, 2, constrained_layout=True, figsize = (14,8))
    axs[0,0].plot(time, np.round(np.array(RPM), 2), "g-", linewidth=linewidth)
    axs[0,0].set_ylabel(r"RPM [rev/min]")
    axs[0,0].set_ylim(0, Cruise.MaxRPM)
    axs[0,0].set_xlim((0,time.max()))
    axs[0,1].plot(time, V_infty, linewidth=linewidth)
    axs[0,1].set_ylabel(r"Velocity - $V_\infty$ [kts]")
    axs[0,1].set_xlim((0,time.max()))
    axs[1,0].plot(time, Distance, "r-", linewidth=linewidth)
    axs[1,0].set_ylabel(r"Distance - $d$ [nmi]")
    axs[1,0].set_xlim((0,time.max()))
    axs[1,1].plot(time, Percent, "y--", linewidth=linewidth)
    axs[1,1].set_ylabel(r"Percent [\%]")
    axs[1,1].set_xlim((0,time.max()))
    axs[2,0].plot(time, Lift, "g", linewidth=linewidth)
    axs[2,0].set_ylabel(r"Lift - $L$ [N]")
    axs[2,0].set_xlim((0,time.max()))
    axs[2,1].plot(time, Drag, "r--", linewidth=linewidth)
    axs[2,1].set_ylabel(r"Drag - $D$ [N]")
    axs[2,1].set_xlim((0,time.max()))
    axs[2,1].set_xlabel(r"Time - $t$ [s]")
    axs[2,0].set_xlabel(r"Time - $t$ [s]")
    # axs[1,0].set_ylim((0, Altitude.max()*1.2))
    axs[1,1].set_ylim((0, Percent.max()*1.2))
    fig.suptitle(title)
    plt.savefig(image_dir + r"\\Cruise_Performance\\" + title.replace(" ", "_")+".png")
    plt.show()











def Regular_Plot(x, y, xlabel, ylabel, title, color = 'r'):
    '''
    x is an array of x values
    y is an array of y values
    title will also be the type used for saving plots
    '''
    plt.plot(x,y,color = color)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    os.chdir(image_dir)
    plt.savefig(title + '.png')
    os.chdir(main_dir)

'''
def MyCurrentPlot(control, title):
    fig, ax = plt.subplots(nrows=6, ncols=1)
    if isinstance(control.Aircraft, AircraftConventional):
        title = "Conventional " + title
        power = control.EnergyMassArr
        label5x = "Fuel Mass (kg)"
    if isinstance(control.Aircraft, AircraftElectric):
        title = "Electric " + title
        power = control.percentArr
        label5x = "Battery Percent (%)"
    else:
        print("This object is not defined")
        return None
    #fig.subplot_tool()
    #plt.subplots_adjust(top = .9, bottom = .1, wspace= .1, hspace=.1)
    #ax.rcParams['figure.figsize'] = [4, 10]
    fig.suptitle(title)
    ax[0].plot(control.RangeArr, control.AltitudeArr)
    ax[0].set_xlabel("Range (nmi)")
    ax[0].set_ylabel("Altitude (ft)")

    ax[1].plot(control.vArr, control.AltitudeArr)
    ax[1].set_xlabel("Velocity (kts)")
    ax[1].set_ylabel("Altitude (ft)")

    ax[2].plot(control.RangeArr, control.vArr)
    ax[2].set_xlabel("Range (nmi)")
    ax[2].set_ylabel("Velocity (kts)")

    ax[3].plot(control.AltitudeArr, control.Power_ThrustArr)
    ax[3].set_ylabel("Power from Thrust (W)")
    ax[3].set_xlabel("Altitude (ft)")

    ax[4].plot(control.AltitudeArr, control.ThrustArr)
    ax[4].set_ylabel("Thrust (N)")
    ax[4].set_xlabel("Altitude (ft)")

    ax[5].plot(power, control.AltitudeArr)
    ax[5].set_xlabel(label5x)
    ax[5].set_ylabel("Altitude (ft)")
    
    os.chdir(image_dir)
    plt.savefig(title + '.png')
    os.chdir(main_dir)
    fig.show()
'''


"""
def MyCurrentPlot(control, title):
    fig = plt.figure(constrained_layout=True)
    gs = GridSpec(3, 2, figure=fig)
    if isinstance(control.Aircraft, AircraftConventional):
        title = "Conventional " + title
        power = control.EnergyMassArr * 2.20462/6
        label5x = "Fuel Mass (gal)"
    elif isinstance(control.Aircraft, AircraftElectric):
        title = "Electric " + title
        power = control.percentArr
        label5x = "Battery Percent (%)"
    else:
        print("This object is not defined")
        return None
    #plt.subplots_adjust(top = .9, bottom = .1, wspace= .1, hspace=.1)
    #plt.figure(figsize=(100,10))
    fig.suptitle(title)
    ax0 = fig.add_subplot(gs[0,0])
    ax0.plot(control.RangeArr, control.AltitudeArr)
    ax0.set_xlim(left = 0)
    ax0.set_ylim(bottom = 0)
    ax0.set_xlabel("Range (nmi)")
    ax0.set_ylabel("Altitude (ft)")

    ax1 = fig.add_subplot(gs[1,0])
    ax1.plot(control.vArr, control.AltitudeArr)
    ax1.set_xlim(left = 0)
    ax1.set_ylim(bottom = 0)
    ax1.set_xlabel("Velocity (kts)")
    ax1.set_ylabel("Altitude (ft)")

    ax2 =  fig.add_subplot(gs[2,0])
    ax2.plot(control.RangeArr, control.vArr)
    ax2.set_xlim(left = 0)
    ax2.set_ylim(bottom = 0)
    ax2.set_xlabel("Range (nmi)")
    ax2.set_ylabel("Velocity (kts)")

    ax3 = fig.add_subplot(gs[0,1])
    ax3.plot(control.AltitudeArr, control.Power_ThrustArr * 0.00134102)
    ax3.set_xlim(left = 0)
    ax3.set_ylim(bottom = 0)
    ax3.set_ylabel("Power-T (hp)")
    ax3.set_xlabel("Altitude (ft)")

    ax4 = fig.add_subplot(gs[1,1])
    ax4.plot(control.AltitudeArr, control.ThrustArr)
    ax4.set_xlim(left = 0)
    ax4.set_ylim(bottom = 0)
    ax4.set_ylabel("Thrust (N)")
    ax4.set_xlabel("Altitude (ft)")

    ax5 = fig.add_subplot(gs[2,1])
    ax5.plot(power, control.AltitudeArr)
    ax5.set_xlim(left = 0)
    ax5.set_ylim(bottom = 0)
    ax5.set_xlabel(label5x)
    ax5.set_ylabel("Altitude (ft)")
    
    os.chdir(image_dir)
    plt.savefig(title + '.png')
    os.chdir(main_dir)
    fig.show()"""