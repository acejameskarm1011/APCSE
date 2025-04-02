import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from time import time
from solve_ls import solve_ls

np.set_printoptions(suppress=True)

# Utilizes a timer so that costly functions are avoided
t0 = time()

# Takes in airfoil dat file and turns the coordinates into a numpy array
data = pd.read_csv("naca652415.dat", header=None)
dataframe = pd.DataFrame(data).to_numpy()[1:]
data = []
for i, df in enumerate(dataframe):
    data.append(np.array(df[0].split("   ")).astype(float))
data = np.array(data)

AirfoilTools = pd.read_csv("xf-naca652415-il-1000000.csv", header=None)
AFT_df = pd.DataFrame(AirfoilTools).to_numpy()[10:,:]

AFT_alpha = AFT_df[1:,0].astype(float)
AFT_C_l = AFT_df[1:,1].astype(float)


# Sorting the airfoil top and bottom surfaces
num = len(data[:,0])
upper = data[:int((num+1)/2),:][::-1]
lower = data[int((num-1)/2):,:]

x_upper = upper[:,0]
y_upper = upper[:,1]
x_lower = lower[:,0]
y_lower = lower[:,1]



# Using a least square polynomial the approximate function is returned
# Future iterations hopes to compare this to a fit of cubic splines
p = 8

N = 100
x_lower_ls, y_lower_ls, constants_lower = solve_ls(x_lower, y_lower,p, n=N)
x_upper_ls, y_upper_ls, constants_upper = solve_ls(x_upper, y_upper,p, n=N)

t_c = y_upper-y_lower

# print("Maximum Thickness: {} %".format(round(t_c.max()*100)))

# Plots the data
plotting = False
if plotting:
    fig, ax = plt.subplots(1, 1, constrained_layout = True, figsize = (10,10))
    color_data = "b."
    ax.plot(x_lower, y_lower, color_data)
    ax.plot(x_upper, y_upper, color_data)

    ax.plot(x_lower_ls, y_lower_ls, "g--")
    ax.plot(x_upper_ls, y_upper_ls, "g--")

    ax.plot(x_lower_ls, (y_lower_ls+y_upper_ls)/2, "r--")
    ax.set_ylim((-0.4,0.4))
    plt.grid()
    plt.show()


# Thin airfoil theory section. 
constants_MAC = (constants_upper + constants_lower)/2

dtheta = np.pi*1e-2
theta = np.arange(0,np.pi + dtheta,dtheta)
x_MAC = 1/2*(1-np.cos(theta))

z_MAC = np.zeros(x_MAC.shape)
for i, c in enumerate(constants_MAC):
    z_MAC += c*x_MAC**(i)

dz_dx = 1




AOA = AFT_alpha.copy()
alpha = AOA/180*np.pi
dz_dx = (z_MAC[1:] - z_MAC[:-1])/(x_MAC[1:] - x_MAC[:-1])


C_l_0 = - 1/(np.pi-dtheta)*np.trapz(dz_dx, theta[:-1])*2*np.pi + 2/(np.pi-dtheta)*np.trapz(dz_dx*np.cos(theta[:-1]), theta[:-1])*np.pi




A_0 = alpha - 1/(np.pi-dtheta)*np.trapz(dz_dx, theta[:-1])
A_1 = 2/(np.pi-dtheta)*np.trapz(dz_dx*np.cos(theta[:-1]), theta[:-1])
A_2 = 2/(np.pi-dtheta)*np.trapz(dz_dx*np.cos(2*theta[:-1]), theta[:-1])



C_l = 2*np.pi*A_0 + np.pi*A_1
error = (C_l-AFT_C_l)


t1 = time()

fig, ax = plt.subplots(1, 2, constrained_layout = True, figsize = (12,8))
ax[0].plot(AOA, C_l, label = "Thin Airfoil Theory")
ax[0].plot(AFT_alpha, AFT_C_l, "r.", label = "Test Data at $Re=1,000,000$")
ax[0].set_xlabel("Angle of Attack [deg]")
ax[0].set_ylabel(r"$C_l$")
ax[0].legend()
ax[0].grid()


ax[1].plot(AOA, error)
ax[1].set_xlabel("Angle of Attack [deg]")
ax[1].set_ylabel(r"error [$\Delta C_l$]")
ax[1].grid()
# ax[1].set_ylim(-100,100)
fig.savefig("C_l_vs_AOA.png")
# plt.show()



print("Took {} s to load".format(t1-t0))

