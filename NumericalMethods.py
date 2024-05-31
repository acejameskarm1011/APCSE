import numpy as np
np.set_printoptions(suppress=True)
def Forward_Euler(Function, u_k, delta_t):
    u_kplus1 = u_k + Function(u_k)*delta_t
    return u_kplus1
def ab2(Function, uk, ukm1, delta_t):
    u_km1 = ukm1
    u_k = uk
    f_km1 = Function(u_km1)
    f_k = Function(u_k)
    u_kplus1 = u_k + delta_t/2*(-f_km1 + 3*f_k)
    return u_kplus1
def ab3(func, uk, ukm1, ukm2, delta_t):
    u_kminus1 = ukm1
    u_kminus2 = ukm2
    u_k = uk
    f_kminus2 = func(u_kminus2)
    f_kminus1 = func(u_kminus1)
    f_k = func(u_k)
    u_kplus1 = u_k + delta_t/12*(23*f_k-16*f_kminus1 + 5*f_k)
    return u_kplus1
def func(u_k):
    x, xdot = u_k
    udot = np.array([xdot, -x])
    return udot

u_0 = np.array([1,0])
dt = 1e-3
tArr = np.arange(0,np.pi/2,dt)
k = len(tArr)
u_solution = np.zeros((k+1, len(u_0)))
u_solution[0,:] = u_0
u_solution[1,:] = Forward_Euler(func, u_0, dt)
u_solution[2,:] = ab2(func, u_solution[1,:], u_0, dt)

for i in range(2, k):
    u_km2 = u_solution[i-2, :]
    u_km1 = u_solution[i-1, :]
    u_k = u_solution[i, :]
    u_solution[i+1,:] = ab3(func, u_k, u_km1, u_km2, dt)
u_solution = np.zeros((k+1, len(u_0)))
u_solution[0,:] = u_0
for i in range(k):
    u_solution[i+1,:] = ab3(func, u_k, u_km1, u_km2, dt)


print(u_solution[-1,:])