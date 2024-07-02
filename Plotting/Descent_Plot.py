from Propulsion.Engine import ElectricEngineTest
import scipy as sp
import matplotlib.pyplot as plt
import numpy as np


def Descent_Plot(Descent, title = "Descent Plots"):
    """
    Using the Descent class, we can use the data stored within it in order to plot how each of the paramters are changing over time.

    Parameters
    ----------
    Descent : Instance of the Descent class

    Notes: Images with be stored in the Take_Off_Performance directory in Images_From_Code
    """
    if isinstance(Descent.Aircraft.Engine, ElectricEngineTest):
        title = "Electric " + title
    linewidth = 3
    V_infty = Descent.Velocity_List / sp.constants.knot
    Pitch = Descent.Pitch_List
    Distance = Descent.Position_x / sp.constants.foot
    time = Descent.Times
    V_NE = Descent.Aircraft.NeverExceedSpeed
    Altitude = Descent.Altitude_List
    Percent = Descent.Percent_List
    Lift = Descent.Lift_List
    Drag = Descent.Drag_List
    RPM = Descent.RPM_List
    Thrust = Descent.Thrust_List

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
    axs[1,1].plot(time, RPM, "y--", linewidth=linewidth)
    axs[1,1].set_ylabel(r"RPM [rev/min]")
    axs[1,1].set_xlim((0,time.max()))
    axs[2,0].plot(time[1:], Lift[1:], "g", linewidth=linewidth)
    axs[2,0].set_ylabel(r"Lift - $L$ [N]")
    axs[2,0].set_xlim((0,time.max()))
    axs[2,1].plot(time, Thrust, "r--", linewidth=linewidth)
    axs[2,1].set_ylabel(r"Thrust - $T$ [N]")
    axs[2,1].set_xlim((0,time.max()))
    axs[2,1].set_xlabel(r"Time - $t$ [s]")
    axs[2,0].set_xlabel(r"Time - $t$ [s]")
    # axs[1,0].set_ylim((0, Altitude.max()*1.2))
    axs[1,1].set_ylim((0, RPM.max()*1.2))
    fig.suptitle(title)
    # plt.savefig(image_dir + r"\\Descent_Performance\\" + title.replace(" ", "_")+".png")
    plt.show()