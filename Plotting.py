import matplotlib.pyplot as plt
from ImportAPCSE import *
import os
main_dir = os.getcwd()
image_dir = main_dir + '.\Images_From_Code'
from matplotlib.gridspec import GridSpec


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
    ax[1].set_xlabel("Velocity (m/s)")
    ax[1].set_ylabel("Altitude (ft)")

    ax[2].plot(control.RangeArr, control.vArr)
    ax[2].set_xlabel("Range (nmi)")
    ax[2].set_ylabel("Velocity (m/s)")

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



def MyCurrentPlot(control, title):
    fig = plt.figure(constrained_layout=True)
    gs = GridSpec(3, 2, figure=fig)
    if isinstance(control.aircraft, AircraftConventional):
        title = "Conventional " + title
        power = control.EnergyMassArr
        label5x = "Fuel Mass (kg)"
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
    ax1.set_xlabel("Velocity (m/s)")
    ax1.set_ylabel("Altitude (ft)")

    ax2 =  fig.add_subplot(gs[2,0])
    ax2.plot(control.RangeArr, control.vArr)
    ax2.set_xlim(left = 0)
    ax2.set_ylim(bottom = 0)
    ax2.set_xlabel("Range (nmi)")
    ax2.set_ylabel("Velocity (m/s)")

    ax3 = fig.add_subplot(gs[0,1])
    ax3.plot(control.AltitudeArr, control.Power_ThrustArr)
    ax3.set_xlim(left = 0)
    ax3.set_ylim(bottom = 0)
    ax3.set_ylabel("Power-T (W)")
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
    fig.show()