import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from time import time
cwd = os.getcwd()
print(cwd)

if cwd == r"C:\APCSE\Wing_Theory":

    from solve_ls import solve_ls
    from lifting_line_theory import solve_fourier_coefficients
else:
    from Wing_Theory.solve_ls import solve_ls
    from Wing_Theory.lifting_line_theory import solve_fourier_coefficients
from matplotlib.gridspec import GridSpec
import scienceplots
plt.style.use(["science","grid"])


textsize = 15
linewidth = 2
plt.rcParams.update({'font.size': textsize,
                     "lines.linewidth" : linewidth})

np.set_printoptions(suppress=True)

# Utilizes a timer so that costly functions are avoided
t0 = time()

# Takes in airfoil dat file and turns the coordinates into a numpy array
if cwd == r"C:\APCSE\Wing_Theory":
    data = pd.read_csv("naca652415.dat", header=None)
    AirfoilTools = pd.read_csv("xf-naca652415-il-1000000.csv", header=None)

else:
    data = pd.read_csv("Wing_Theory\\naca652415.dat", header=None)
    AirfoilTools = pd.read_csv("Wing_Theory\\xf-naca652415-il-1000000.csv", header=None)

dataframe = pd.DataFrame(data).to_numpy()[1:]
data = []
for i, df in enumerate(dataframe):
    data.append(np.array(df[0].split("   ")).astype(float))
data = np.array(data)

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
printing = False
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




C_l_alpha = 2*np.pi
C_l_0 = 2*np.pi*(- 1/(np.pi-dtheta)*np.trapz(dz_dx, theta[:-1])) + np.pi*(A_1)


C_l = C_l_0 + alpha*C_l_alpha

alpha_ZL = - C_l_0/C_l_alpha * (180/np.pi)
if printing:
    print(alpha_ZL)




# Defining the PA-28-181 Wing from POH diagram - Including frontal extension

span = 35.5                # ft
c_tip = 3+6.2/12           # ft
c_root = 5.25              # ft
delta_c = 0.9596           # ft
l_1 = 3.7906/2             # ft
l_3 = span/2 - 9.0447+l_1  # ft
l_2 = l_3 - 7.0534  +l_1   # ft

Sref = 2*(l_1*(c_root+delta_c) + 1/2*(l_2-l_2)*(2*c_root+delta_c) + (l_3-l_2)*(c_root) + 1/2*(span/2-l_3)*(c_root+c_tip))
AR = span**2/Sref
# print(AR)
print(Sref)
print("DOUBLE CHECK THE AREA CALCULATION HERE!!!")
exit()
# print("Pringing aspect ratio in wing analysis")
# exit()
def chord_y(y):
    y = np.abs(y)
    chord = c_tip*np.ones(y.shape)
    chord[y < span/2] = c_root + (c_tip-c_root)/(span/2-l_3)*(y[y<span/2]-l_3)
    chord[y < l_3] = c_root
    chord[y < l_2] = c_root + delta_c - delta_c/(l_2-l_1)*(y[y<l_2]-l_1)
    chord[y < l_1] = c_root + delta_c
    return chord

points = 201
y_arr = span/2*np.linspace(-1,1,points)
chord = chord_y(y_arr)


if plotting:
    plt.figure(figsize=(10,7))
    plt.plot(y_arr, chord)
    plt.ylim(bottom = 0)
    plt.xlabel("Span (y) [ft]")
    plt.ylabel("Chord Length (c) [ft]")
    plt.savefig("Piper_Planform")
    plt.show()


def chord_theta(theta):
    y = span/2*np.cos(theta)
    return chord_y(y)


alpha_5 = 5 # deg
alpha_0 = 2 # deg

def alpha_theta_5(theta):
    return alpha_5*np.ones(theta.shape)

def alpha_theta_0(theta):
    return alpha_0*np.ones(theta.shape)

def alpha_ZL_func(theta):
    return alpha_ZL*np.ones(theta.shape)

N = 1001

A_n, theta = solve_fourier_coefficients(N, C_l_alpha, chord_theta, span, alpha_theta_5, alpha_ZL_func)
C_L_5 = np.pi*AR*A_n[0]


A_n, theta = solve_fourier_coefficients(N, C_l_alpha, chord_theta, span, alpha_theta_0, alpha_ZL_func)
C_L_0 = np.pi*AR*A_n[0]

sigma = np.pi*AR*sum(A_n[1:]**2)/A_n[0]**2
spaneff = 1/(1+sigma)
# print(spaneff)


C_L_alpha = (C_L_5 - C_L_0)/(alpha_5-alpha_0) # 1/deg

alpha_arr = np.linspace(-8, 12, points)
C_L_arr = C_L_0 + C_L_alpha*alpha_arr



if printing:
    print("C_L_0: ", C_L_0)
    print("C_L_alpha: ", C_L_alpha, "[1/deg]")


C_l_max = AFT_C_l.max()



if plotting:
    plt.figure(figsize = (6,8))
    plt.plot(alpha_arr, C_L_arr, label = r"Lift Curve" + "\n" + r"$C_{L_0}=0.572$" + "\n" + r"$C_{L_\alpha}=0.108$ [1/deg]")
    plt.plot(alpha_arr, C_l_max*np.ones(points), "k--", label = r"$C_{l_\text{max}}$="+str(round(C_l_max, 2)))
    plt.legend()
    plt.xlabel(r"Angle of Attack [deg]")
    plt.ylabel(r"Wing Lift $C_L$")
    plt.savefig("C_L_vs_alpha_PA28Wing")
    plt.show()






if plotting:
    t1 = time()

    fig, ax = plt.subplots(1, 1, constrained_layout = True, figsize = (12,8))
    ax.plot(AOA, C_l, label = "Thin Airfoil Theory")
    ax.plot(AFT_alpha, AFT_C_l, "r.", label = "Test Data at $Re=1,000,000$")
    ax.set_xlabel("Angle of Attack [deg]")
    ax.set_ylabel(r"$C_l$")
    ax.legend()
    ax.grid()
    plt.show()

    print("Took {} s to load".format(t1-t0))