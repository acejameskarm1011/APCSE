#Performance
import os
perf_dir = os.getcwd()
main_dir = perf_dir[:-20]

os.chdir(main_dir)
from Aviation import *
os.chdir(perf_dir)

class PerformanceOLD(Aviation):
    
    def __init__(self, AircraftName, CruiseMach, CruiseAltitude, AircraftType) -> None:
        super().__init__(AircraftName, CruiseMach, CruiseAltitude, AircraftType)
        self.Mach = Mach
        self.Position = 0
        self.Plots = 0
        self.rPlots = 0
        self.ePlots = 0
        self.SimTest = False
        self.AircraftType = AircraftType
        self.Altitude = Altitude
        self.TotalMass = TotalMass
    
    def Dictionary_setattr(self, Dictionary):
        super().Dictionary_setattr(Dictionary)
        self.TotalMass = self.MGTOW
        self.Fuel = self.MaxFuel
        
    def Climb(self, ClimbRate = 1000, dt = 10, CruiseType = True): #1000 ft/min, 2 deg #On a quick GoOgle search, it was found that aircraft TYP climb at 250kts below 10k ft, and transition to 300 kts above FL10, then at FL25 AC climb at 0.7 Mach
        dtype = type(self.CruiseAltitude)
        if dtype == int or dtype == float:
            Number = 1
        else:
            Number = len(self.CruiseAltitude)

        Ones = np.ones(Number)
        self.Altitude *= Ones
        knots = Ones
        self.v_fps = Ones
        self.v = Ones
        dt /= 10
        self.v_h = ClimbRate / 60 * Ones 
        self.v_z = self.v_h * self.ft_to_m 
        self.Endurance *= Ones
        dt = dt * Ones

        x = 0
        y = 0
        xarr = np.array([])
        yarr = np.array([])
        while (self.CruiseAltitude - self.Altitude).max() > 0:
                
            self.a, self.g, self.rho = AtmosphereFunctionSI(self.Altitude, ['a','g','rho'])

            knots[self.Altitude < 10000] = 250
            
            knots[np.logical_and(self.Altitude > 10000,self.Altitude < 25000)] = 300
            self.v = knots * self.knots_to_mps
 
            self.v[self.Altitude > 25000] = 0.7 * self.a[self.Altitude > 25000]

            
            FlightAngle = np.arcsin(self.v_z/self.v)

            gamma = FlightAngle 
            self.v_x = self.v * np.cos(gamma)
            self.v_z = self.v * np.sin(gamma)
            self.v_y = np.zeros(Number)
            self.DynamicPressure = .5*self.rho*self.v**2
            self.Weight = self.TotalMass * self.g
            self.Lift = self.Weight * np.cos(gamma)
            self.C_L = (self.Lift / (self.DynamicPressure * self.S))
            self.GetC_D(self.EmbraerComponents)
            self.Drag = self.DynamicPressure * self.S * self.C_D
            self.Thrust = self.Drag + (self.Weight * np.sin(gamma))
            self.GetTSFC(unit = 's')
            self.FuelBurn = -self.Thrust*self.TSFC*dt/self.g
            self.v_h = self.v_z * self.m_to_ft
            self.Altitude += self.v_h * dt

            Check = self.CruiseAltitude - self.Altitude < 0
            notcheck = self.CruiseAltitude - self.Altitude >= 0
            self.Altitude[Check] = self.CruiseAltitude[Check]
            self.v_x[Check] = 0
            self.v_y[Check] = 0
            self.v_z[Check] = 0

            x += self.v_x[-1] * dt[-1]
            y += self.v_z[-1] * dt[-1]
            xarr = np.append(xarr, x)
            yarr = np.append(yarr, y)

            self.FuelBurn[Check] = 0
            dt[Check] = 0
            self.Fuel += self.FuelBurn 
            self.TotalMass += self.FuelBurn 
            self.Endurance += dt
            self.Range += self.v_x*dt
            # print(f"fuel{self.Fuel[0]}")
            # self.Velocity = np.array([self.v_x,self.v_y,self.v_z])
            # self.Position += self.Velocity * dt
        print("Climb complete")
        return xarr * self.m_to_nmi, yarr * self.m_to_ft  
    
    def GlideDescent(self, dt = 10):
        timertest = 0
        self.Altitude = np.outer(self.Altitude, np.ones(len(self.CruiseMach)))
        dtarray = np.ones((self.AltitudeSize, self.MachSize)) * dt
        while self.Altitude.max() > 0:
            self.a, self.g, self.rho = AtmosphereFunctionSI(self.Altitude, ['a','g','rho'])
            self.GetC_L_max([self.EmbraerWings, self.EmbraerHorizontalStabilizer])
            self.GetC_D(self.EmbraerComponents)
            self.gamma = -np.arctan(self.C_D/self.C_L)
            self.TotalMass = self.MGTOW - self.MaxFuel
            self.Weight = self.TotalMass * self.g
            V_Glide = np.sqrt(2*self.Weight*np.cos(self.gamma)/(self.rho*self.S*self.C_L))
            self.v = V_Glide
            # print((self.v * self.mps_to_knots)[0,0])
            self.v_x = np.cos(self.gamma)*self.v
            self.v_y = np.zeros(self.v_x.shape)
            self.v_z = np.sin(self.gamma)*self.v
            
            self.v_h = self.v_z * self.m_to_ft
            self.Altitude += self.v_h * dt

            self.Altitude[self.Altitude < 0] = 0
            self.v_x[self.Altitude == 0] = 0
            self.v_z[self.Altitude == 0] = 0
            dtarray[self.Altitude == 0] = 0
            self.Endurance += dtarray
            self.Velocity = np.array([self.v_x, self.v_y, self.v_z])
            self.Range += self.v_x * dt
            # self.Position += self.Velocity * dt
            
            # timertest += 1

        print("Glide complete")
        return None
    
    def ConventionalSlufSimulation(self, dt = 10):
        if np.ndarray != type(self.CruiseAltitude):
            self.CruiseAltitude = np.array([self.CruiseAltitude])
        if np.ndarray != type(self.CruiseMach):
            self.CruiseMach = np.array([self.CruiseMach])
        self.AltitudeSize = len(self.CruiseAltitude)
        self.MachSize = len(self.CruiseMach)
        self.MachOnes = np.ones(self.MachSize)
        
        self.Mach = self.CruiseMach
        self.Altitude = self.CruiseAltitude
        self.a, self.g, self.rho = AtmosphereFunctionSI(self.Altitude, ['a','g','rho'])
        self.v = np.outer(self.a, self.Mach)
        self.DynamicPressure = (.5*self.rho*(self.v.T)**2).T
        self.Fuel = np.outer(self.Fuel, self.MachOnes)
        # print(self.Fuel[0,0])
        self.TotalMass = np.outer(self.TotalMass, self.MachOnes)
        self.Range = np.outer(self.Range, self.MachOnes)
        self.Endurance = np.outer(self.Endurance, self.MachOnes)   
        dtarray = np.ones((self.AltitudeSize, self.MachSize)) * dt
        # empty = np.array([])
        # for i in range(3):
        #     empty = np.append(empty, np.outer(self.Position[i], self.MachOnes))
        # self.Position = empty.reshape(3,self.AltitudeSize, self.MachSize)

        self.v_x = self.v
        self.v_y = np.zeros((self.AltitudeSize, self.MachSize))
        self.v_z = self.v_y
        while np.any(self.Fuel > 0):
            self.Weight = (self.TotalMass.T * self.g).T
            self.Lift = self.Weight
            self.C_L = (self.Lift/(self.DynamicPressure * self.S))
            self.GetC_D(self.EmbraerComponents)
            self.Drag = self.DynamicPressure * self.S * self.C_D
            self.Thrust = self.Drag
            self.GetTSFC(unit = 's')
            self.FuelBurn = ((-self.Thrust*self.TSFC * dt).T / self.g).T
            self.Fuel += self.FuelBurn
            if np.any(self.Fuel < 0):
                self.Fuel[self.Fuel < 0] = 0
                self.v[self.Fuel == 0] = 0
                self.FuelBurn[self.Fuel == 0] = 0
                self.TotalMass[self.Fuel == 0] = self.MGTOW - self.MaxFuel
                dtarray[self.Fuel ==0] = 0
            self.Endurance += dtarray
            # print(f'fuel{self.Fuel}')
            # print(self.Endurance[0,0])
            self.TotalMass += self.FuelBurn
            
            self.Range += self.v_x * dt
            # self.Velocity = np.array([self.v_x, self.v_y, self.v_z])
            # self.Position += self.Velocity * dt
        pass
    
    def Breguet(self, dt = 10):
        if np.ndarray != type(self.CruiseAltitude):
            self.CruiseAltitude = np.array([self.CruiseAltitude])
        if np.ndarray != type(self.CruiseMach):
            self.CruiseMach = np.array([self.CruiseMach])
        self.AltitudeSize = len(self.CruiseAltitude)
        self.MachSize = len(self.CruiseMach)
        self.MachOnes = np.ones(self.MachSize)
        self.Mach = self.CruiseMach
        self.Altitude = self.CruiseAltitude
        self.a, self.g, self.rho = AtmosphereFunctionSI(self.Altitude, ['a','g','rho'])
        self.v = np.outer(self.a, self.Mach)
        self.DynamicPressure = (.5*self.rho*(self.v.T)**2).T
        self.Fuel = self.MaxFuel * np.ones((self.AltitudeSize, self.MachSize))

        
        self.TotalMass = self.MGTOW * np.ones((self.AltitudeSize, self.MachSize))
        self.Range = np.zeros((self.AltitudeSize, self.MachSize))

        self.C_Larr = np.zeros(self.Fuel.shape)
        self.C_Darr = np.zeros(self.Fuel.shape)
        self.v_x = self.v
        tic = 0
        while np.any(self.Fuel > 0):
            if tic == 5:
                break
            tic += 1
            self.Weight = (self.TotalMass.T * self.g).T
            self.Lift = self.Weight
            self.C_L = (self.Lift/(self.DynamicPressure * self.S))
            self.GetC_D(self.EmbraerComponents)
            self.Drag = self.DynamicPressure * self.S * self.C_D
            self.Thrust = self.Drag
            self.GetTSFC(unit = 's')
            self.FuelBurn = ((-self.Thrust*self.TSFC * dt).T / self.g).T
            print(self.FuelBurn.shape)
            self.Fuel += self.FuelBurn
            if self.Fuel.min() < 0:
                self.Fuel[self.Fuel < 0] = 0
                self.v[self.Fuel == 0] = 0
                self.FuelBurn[self.Fuel == 0] = 0
                self.TotalMass[self.Fuel == 0] = self.MGTOW - self.MaxFuel

            self.TotalMass += self.FuelBurn
            
            self.Range += self.v_x * dt
            self.C_Larr = np.append(self.C_Larr, self.C_L)
            self.C_Darr = np.append(self.C_Darr, self.C_D)



            #self.C_Larr = np.append(self.C_Larr, np.array([self.C_L]), axis=0)
            #self.C_Darr = np.append(self.C_Darr, np.array([self.C_D]), axis=0)
            '''
            if np.any(self.Fuel < 0):
                    for i in range(N):
                        if self.Fuel[i] < 0:
                            self.time = np.append(self.time, self.timer)
                            self.Fuel[i] = 0
                            self.v[i] = 0
                            self.FuelBurn[i] = 0
                            '''
            self.TotalMass += self.FuelBurn
            self.Range += self.v_x*dt
        #self.C_Larr = np.delete(self.C_Larr, 0, 0)
        #self.C_Darr = np.delete(self.C_Darr, 0, 0)
        return "Breguet Test is completed"
    
    def MaxRangeFly(self, dt = 10):
        #When defining singular vs parametric simulations, Singular = True & Parametric = False
        self.Endurance = 0
        Singular = True
        Parametric = False
        self.Position = 0
        MissionPhase = "Take-Off"
        self.Altitude = 0
        self.Range = 0
        self.TotalMass = self.MGTOW
        self.Fuel = self.MaxFuel
        print(f'Time step is running at dt = {dt}s')
        if self.HybridFactor == 0:
            while MissionPhase != "Finished":
                if MissionPhase == "Take-Off": #Take-Off Mission Phase
                    # print("Take-Off has not been coded, now running Climb sim")
                    MissionPhase = "Climb"
                elif MissionPhase == "Climb": #Climb Mission Phase
                    self.Climb()
                    self.ClimbRange = self.Range
                    MissionPhase = "Cruise2Zero"
                elif MissionPhase == "Cruise2Zero":
                    print(f"{self.AircraftName} is now at cruising altitude {float(self.Altitude[0])}-{float(self.CruiseAltitude[-1])}ft")
                    self.ConventionalSlufSimulation(dt = dt)
                    MissionPhase = "Glide"
                elif MissionPhase == "Glide":
                    print("Fuel Empty, now gliding")
                    self.GlideDescent(dt = dt)
                    MissionPhase = "Finished"
            self.MaxRange = self.Range.max() * self.m_to_nmi
            print(f'The maximum range for this aircaft found was {round(self.MaxRange, 4)}nmi')
            self.SimTest = True
        return None