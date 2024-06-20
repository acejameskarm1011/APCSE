from Plotting.Plotting import *

n = 400

T_std = 300
T_oat = 300
R_m = np.linspace(0,1-1e-4,n)
R_f = 0

sigma_std = 1

P_BHP_max = 180
P_BHP = P_BHP_max*np.sqrt(T_std/T_oat)*((R_m-R_f*(1-R_m))*(sigma_std-R_m**0.8097)+(R_m**0.8097-0.117)/0.883*(1-sigma_std))/(1-R_m**0.8097)
Max = np.ones(n)*180



plt.figure(figsize=(10,10))
plt.plot(R_m, P_BHP)
plt.plot(R_m, Max, "k--")
plt.xlabel("$R_m$")
plt.ylabel("$P_{BHP}$")
plt.show()
