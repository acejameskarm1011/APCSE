#Control
from Aviation import Aviation
import numpy as np



class Control(Aviation):
    """
    This class handles and operates on the Aircraft class.

    Parameters
    ----------
    AircraftInstance : Aircraft
        Must input an instance of an Aircraft so that the control class will be able to employ methods that will update the characteristics of the Aircraft.
   
    Schedule : List of phase objects
        The list of phases that the plane will be required to fly. Based on engine and aerodynamic limitations, the Aircraft may not follow the exact planned course.

    Notes
    ----
    This class is still currently under development, and it should not be used until all other components are completed
    """
    def __init__(self, AircraftInstance, Schedule) -> None:
        self.Aircraft = AircraftInstance
        self.Schedule = Schedule
        self.ClimbScheduleCheck()
        self.Phase = "TakeOff"
        self.AltitudeArr = np.array([])
        self.vArr = np.array([])
        self.RangeArr = np.array([])
        self.Power_ThrustArr = np.array([])
        self.ThrustArr = np.array([])
        self.percentArr = np.array([])
        self.EnduranceArr = np.array([])
        self.EnergyMassArr = np.array([])
        self.C_DArr = np.array([])
    '''  This code right here does not work as intended, and the hope is that some time we will be able to add extra Aircraft simulations within this control object

    def CreateNewAircraft(self, index, CruiseMach, CruiseAltitude):
        oldm = self.Aircraft.CruiseMach
        olda = self.Aircraft.CruiseAltitude
        self.Aircraft.CruiseMach = CruiseMach
        self.Aircraft.CruiseAltitude = CruiseAltitude
        self.__setattr__(f'{self.Aircraft.AircraftName}_{index}',self.Aircraft)
        self.Aircraft.CruiseMach = oldm
        self.Aircraft.CruiseAltitude = olda
    '''
    def No_Energy(self):
        if isinstance(self.Aircraft):
            self.Aircraft.Fuel = 0
            self.Phase = "Glide"
        if isinstance(self.Aircraft):
            self.Aircraft.BattEnergy = 0
            self.Phase = "Glide"
    def ClimbScheduleCheck(self):
        check = True
        self.Aircraft.Atmosphere_attr()
        '''
        all v_h are in terms of ft/min & all h are in terms of h

        if want SI, units = "SI", and m/s will be used

        CS1 = v_h     :This allows for a constant speed throughout the climb

        CS2 = [(v_h1, h1), v_h2]

        CS3 = [(v_h1, h1), (v_h2, h2), (v_h3, h3), ..., v_hn] :vertical speed and height lim

        CS4 = [(v1, h1, "kts"), (v2, h2), (v3, h3, "Mach"), ..., v_hn] :Tuple allows for different speed based on units for climb schedule

        CS5 = [(v1, v_h1, h1, "kts"), (v2, v_h2, h2), (v3, v_h3, h3, "Mach"), ...] :Maximized flexibility
        '''
        if type(self.Schedule) != list:
            self.Aircraft.v_h = self.Schedule * self.ft_to_m / 60
        else:
            if len(self.Schedule[0]) == 2:
                for i in range(len(self.Schedule)-1):
                    if self.Aircraft.Altitude < self.Schedule[i][-1]:
                        self.Aircraft.v_h = self.Schedule[i][0]
                        check = False
                        break
                if check:
                    self.Aircraft.v_h = self.Schedule[-1]
            if len(self.Schedule[0]) == 3:
                self.Aircraft.v_h = self.Schedule[-1]
                for i in range(len(self.Schedule)-1):
                    if type(self.Schedule[i][-1]) == str:
                        factor = self.Schedule[i][-1]
                        if factor == "kts":
                            factor = self.knots_to_mps
                        if factor == "Mach":
                            self.Mach = self.Schedule[i][0]
                            factor = self.Aircraft.acousic_v 
                    if self.Aircraft.Altitude < self.Schedule[i][1]:
                        if type(self.Schedule[i][-1]) == str:
                            factor = self.Schedule[i][-1]
                            if factor == "kts":
                                factor = self.knots_to_mps
                            if factor == "Mach":
                                self.Mach = self.Schedule[i][0]
                                factor = self.Aircraft.acousic_v
                        speed = self.Schedule[i][0]
                        self.Aircraft.v = speed * factor
                        break

    def Add_Parameter(self, Run = True):
        if Run:
            self.AltitudeArr = np.append(self.AltitudeArr,self.Aircraft.Altitude)
            self.vArr = np.append(self.vArr, self.Aircraft.v * self.mps_to_knots)
            self.RangeArr = np.append(self.RangeArr, self.Aircraft.Range)
            self.Power_ThrustArr = np.append(self.Power_ThrustArr, self.Aircraft.Power_Thrust)
            self.ThrustArr = np.append(self.ThrustArr,self.Aircraft.Thrust)
            self.percentArr = np.append(self.percentArr, self.Aircraft.percent)
            self.EnduranceArr = np.append(self.EnduranceArr, self.Aircraft.Endurance)
            self.EnergyMassArr = np.append(self.EnergyMassArr, self.Aircraft.EnergyMass)
            self.C_DArr = np.append(self.C_DArr, self.Aircraft.C_D)
        else:
            pass
    def TimestepBeta(self, dt = 10, AddPar = True):

        self.RangeArr = np.array([])
        self.PercArr = np.array([])

        while self.Aircraft.Altitude < self.Aircraft.CruiseAltitude and self.Aircraft.Emergency == None:
            self.ClimbScheduleCheck()
            self.Aircraft.Climb(dt = dt)
            self.Aircraft.Range += self.Aircraft.v_x * dt * self.m_to_nmi
            self.Aircraft.Endurance += dt
            self.Add_Parameter(AddPar)
            self.Aircraft.Emergency_Check()   
            if self.Aircraft.Emergency != None:
                print("The Engines have failed")
                break
            if self.Aircraft.Altitude > self.Aircraft.CruiseAltitude:
                self.Aircraft.Altitude = self.Aircraft.CruiseAltitude
                self.Phase = "Cruise"
                print(f"{self.Aircraft.AircraftName} is now cruising")
        while self.Phase == "Cruise" and self.Aircraft.Emergency == None:
            self.Aircraft.Cruise(dt = dt)
            self.Aircraft.Range += self.Aircraft.v_x * dt * self.m_to_nmi
            self.Aircraft.Endurance += dt
            self.Add_Parameter(AddPar)
            self.Aircraft.Emergency_Check()
            if round(self.Aircraft.Endurance % 3600) == 0:
                print(self.Aircraft.Endurance / 3600)

            if self.Aircraft.EnergyMass < 0 or self.Aircraft.Emergency != None:
                print("The Engines have failed")
                break
        while self.Aircraft.Emergency == "No_Energy" and self.Aircraft.Altitude > 0:
            self.Aircraft.ZeroThrustGlide(dt = dt)
            self.Aircraft.Range += self.Aircraft.v_x * dt * self.m_to_nmi
            self.Aircraft.Endurance += dt
            self.Add_Parameter(AddPar)
            self.Aircraft.Emergency_Check
        print("Done")












"""
CS1 = 1000 #ft/min
CS2 = [(1000, 10000), 2000] #ft/min
CS3 = [(1000, 10000), (2000, 15000), 500] #ft/min
CS4 = [(250, 10000, "kts"), (300, 25000), (0.7, 30000, "Mach"), 1000]
CSPip = [(76, 10000, "kts"), 1000]
CS5 = [(250, 1000, 10000, "kts"), (300, 2000, 25000, "kts"), (0.7, 500, 30000, "Mach")]
"""