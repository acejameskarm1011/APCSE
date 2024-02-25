import matplotlib.pyplot as plt
from ImportAPCSE import *
import os
main_dir = os.getcwd()
image_dir = main_dir + "\\Images_From_Code"
import scipy as sp
from matplotlib.gridspec import GridSpec
import scienceplots
plt.style.use(["science","grid"])
textsize = 18
plt.rcParams.update({'font.size': textsize})
def TakeOff_Plot(TakeOff, title = "Take-Off Plots"):
    """
    Using the TakeOff class, we can use the data stored within it in order to plot how each of the paramters are changing over time.

    Parameters
    ----------
    TakeOff : Instance of the TakeOff class

    Notes: Images with be stored in the Take_Off_Performance directory in Images_From_Code
    """
    linewidth = 3
    V_infty = TakeOff.Velocity_x / sp.constants.knot
    Distance = TakeOff.Position_x / sp.constants.foot
    time = TakeOff.Times
    V_NE = TakeOff.aircraft.NeverExceedSpeed
    Thrust = TakeOff.Thrust
    Weight = TakeOff.Weight
    Lift = TakeOff.Lift
    Drag = TakeOff.Drag

    fig, axs = plt.subplots(3, 2, constrained_layout=True, figsize = (16,10))
    axs[0,0].plot(time, Distance, "g-", linewidth=linewidth)
    axs[0,0].set_ylabel(r"Ground Roll - $d$ [ft]")
    axs[0,0].set_xlim((0,time.max()))
    axs[0,1].plot(time, V_infty, linewidth=linewidth)
    axs[0,1].set_ylabel(r"Velocoity - $V_\infty$ [kts]")
    axs[0,1].set_xlim((0,time.max()))
    axs[1,0].plot(time, Thrust, "r-", linewidth=linewidth)
    axs[1,0].set_ylabel(r"Thrust - $T$ [N]")
    axs[1,0].set_xlim((0,time.max()))
    axs[1,1].plot(time, Weight, "y--", linewidth=linewidth)
    axs[1,1].set_ylabel(r"Weight - $W$ [N]")
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
    axs[1,1].set_ylim((0, Weight.max()*1.2))
    fig.suptitle(title)
    plt.savefig(image_dir + r"\\Take_Off_Performance\\" + title+".png")
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
    if isinstance(control.aircraft, AircraftConventional):
        title = "Conventional " + title
        power = control.EnergyMassArr
        label5x = "Fuel Mass (kg)"
    if isinstance(control.aircraft, AircraftElectric):
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
    if isinstance(control.aircraft, AircraftConventional):
        title = "Conventional " + title
        power = control.EnergyMassArr * 2.20462/6
        label5x = "Fuel Mass (gal)"
    elif isinstance(control.aircraft, AircraftElectric):
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