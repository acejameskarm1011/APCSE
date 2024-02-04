#AtmosphereFunction
import numpy as np

def AtmosphereFunction(h_G, want = ['h_G']):
    """
    This function evaluates the properties of the atmosphere using the standard atmosphere model.

    Parameters
    ----------
    h_G : int/float/numpy.ndarray
        This is the position in altitude in units of feet.
    want : list
        possible properites that can be inputted are:         
        'h_G' : h_G, 
            Altitude [ft]
        'h' : h,   
            Altitude from center of earth [ft]
        'T' : T, 
            Temperature [R]
        'P' : P,
            Pressure [psf]
        'g' : g_hG,
            Gravity [ft/s^2]
        'rho' :rho,
            Air density [slugs/ft^3]
        'a' : a,
            Acoustic Velocity [ft/s]
        'mu' : mu
            Dynamic Viscousity [psf * s]
    Notes
    ----
    See also AtmosphereFunctionSI if you want terms in SI units
    """
    array = True
    if type(h_G) != np.ndarray:
        h_G = np.array([h_G])
        array = False
    r_e = 3959*5280                     #miles to feet
    R = 1716.5                          #ft2/R-sec
    g0 = 32.174                         #ft/s^2
    T0 = 518.69                         #deg R    
    g_hG = g0*(r_e/(r_e+h_G))**2        #gravity acceleration based on geopotential altitude
    h = (r_e/(r_e+h_G))*h_G             #altitude from geopotential altitude and earth radius    

    empty = np.zeros(h_G.shape)
    T, P, rho = np.array([empty, empty, empty])

    Under = h < 36000
    Over = h > 36000
                      # standard atmosphere maths up until tropopause
    h0 = 0                          # initial altitude of comparison is sea level
    P0 = 2116.22                    #psf
    rho0 = 2.3769e-3                #slugs/ft3
    a1 =-3.57/1000                  #deg R/ft
    T[Under] = T0 + a1*(h[Under]-h0)              # calculate temperature from linear distribution
    P[Under] = P0*(T[Under]/T0)**(-g0/(R*a1))     #pressure from temperature
    rho[Under] = rho0*(T[Under]/T0)**(-((g0/(R*a1))+1))       #density from temperature
    
    h0trop = 36000                        #tropopause altitude (ft)
    P0trop = 4.760119191888137e+2         #from anderson appendix B
    rho0trop =7.103559955456123e-4        #from running code at 36000
    T[Over] = 389.99                        # constant temperature
    P[Over] = P0trop*np.exp((-g0/(R*T[Over])*(h[Over]-h0trop)))           #pressure from temperature
    rho[Over] = rho0trop*np.exp(-(g0/(R*T[Over])*(h[Over]-h0trop)))       #density from temperature
    mu0 = 3.62e-7                         # viscosity at SL
    a = np.sqrt(1.4*P/rho)                # speed of sound
    mu = mu0*(T/T0)**(1.5)*((T0+198.72)/(T+198.72))   # viscosity from temperature

    Datadict = dict({
        'h_G' : h_G,
        'h' : h,
        'T' : T,
        'P' : P,
        'g' : g_hG,
        'rho' :rho,
        'a' : a,
        'mu' : mu
    })
    if len(want) == 1:
        if not array:
            return Datadict[want[0]][0]
        return Datadict[want[0]]
    data = []
    if not array:
        for i in want:
            data.append(Datadict[i][0])
    else:
        for i in want:
            data.append(Datadict[i])
    return data

def AtmosphereFunctionSI(hSI, want = ['h_G'], units = "ft"):
    
    """
    This function evaluates the properties of the atmosphere using the standard atmosphere model.

    Parameters
    ----------
    h_G : int/float/numpy.ndarray
        This is the position in altitude in units of feet as default
    want : list
        possible properites that can be inputted are:         
        'h_G' : h_G, 
            Altitude [m]
        'h' : h,   
            Altitude from center of earth [m]
        'T' : T, 
            Temperature [K]
        'P' : P,
            Pressure [Pa]
        'g' : g_hG,
            Gravity [m/s^2]
        'rho' :rho,
            Air density [kg/m^3]
        'a' : a,
            Acoustic Velocity [m/s]
        'mu' : mu
            Dynamic Viscousity [Pa * s]
    units : str
        May want to measure input altitude in meters, so use units = 'm', for that case.

    Notes
    ----
    See also AtmosphereFunction if you want terms in Imperial units
    """
    if units == "ft":
        h_g = hSI
    elif units == "m":
        h_g = hSI/0.3048   #m to ft
    else:
        print("I do not know what this unit is")
        return
    data = AtmosphereFunction(h_g, want)
    l = len(want)
    if l > 1:
        for i in range(l):
            if want[i] == "h_G" or want[i] == "h" or want[i] == "g" or want[i] == "a":
                    data[i] *= 0.3048
            elif want[i] == "T":
                data[i] *= 5/9
            elif want[i] == "P":
                data[i] *= 4.44822162/0.3048**2
            elif want[i] == "rho":
                data[i] *= 14.5939029372/0.3048**3
            elif want[i] == "mu":
                data[i] *= 14.5939029372/0.3048
            else:
                print("The function ran into an unexpected error!")
                break
    else:
        want = want[0]
        if want == "h_G" or want == "h" or want == "g" or want == "a":
                data *= 0.3048
        elif want == "T":
            data *= 5/9
        elif want == "P":
            data *= 4.44822162/0.3048**2
        elif want == "rho":
            data *= 14.5939029372/0.3048**3
        elif want == "mu":
            data *= 14.5939029372/0.3048
        else:
            print("The function ran into an unexpected error!")
            return       
    return data

#h = 9000
#a = AtmosphereFunctionSI(h, ['rho', "T"])
#print(a)