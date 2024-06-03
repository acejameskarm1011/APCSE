#Control
from Aviation import Aviation
import numpy as np



class Control(Aviation):
    """
    This class handles and operates on the aircraft class.

    Parameters
    ----------
    AircraftInstance : Aircraft
        Must input an instance of an aircraft so that the control class will be able to employ methods that will update the characteristics of the aircraft.
   
    Schedule : List of phase objects
        The list of phases that the plane will be required to fly. Based on engine and aerodynamic limitations, the aircraft may not follow the exact planned course.

    Notes
    ----
    This class is still currently under development, and it should not be used until all other components are completed
    """
    def __init__(self, AircraftInstance, Schedule) -> None:
        self.aircraft = AircraftInstance
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
    '''  This code right here does not work as intended, and the hope is that some time we will be able to add extra aircraft simulations within this control object

    def CreateNewAircraft(self, index, CruiseMach, CruiseAltitude):
        oldm = self.aircraft.CruiseMach
        olda = self.aircraft.CruiseAltitude
        self.aircraft.CruiseMach = CruiseMach
        self.aircraft.CruiseAltitude = CruiseAltitude
        self.__setattr__(f'{self.aircraft.AircraftName}_{index}',self.aircraft)
        self.aircraft.CruiseMach = oldm
        self.aircraft.CruiseAltitude = olda
    '''
    def No_Energy(self):
        if isinstance(self.aircraft):
            self.aircraft.Fuel = 0
            self.Phase = "Glide"
        if isinstance(self.aircraft):
            self.aircraft.BattEnergy = 0
            self.Phase = "Glide"
    def ClimbScheduleCheck(self):
        check = True
        self.aircraft.Atmosphere_attr()
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
            self.aircraft.v_h = self.Schedule * self.ft_to_m / 60
        else:
            if len(self.Schedule[0]) == 2:
                for i in range(len(self.Schedule)-1):
                    if self.aircraft.Altitude < self.Schedule[i][-1]:
                        self.aircraft.v_h = self.Schedule[i][0]
                        check = False
                        break
                if check:
                    self.aircraft.v_h = self.Schedule[-1]
            if len(self.Schedule[0]) == 3:
                self.aircraft.v_h = self.Schedule[-1]
                for i in range(len(self.Schedule)-1):
                    if type(self.Schedule[i][-1]) == str:
                        factor = self.Schedule[i][-1]
                        if factor == "kts":
                            factor = self.knots_to_mps
                        if factor == "Mach":
                            self.Mach = self.Schedule[i][0]
                            factor = self.aircraft.acousic_v 
                    if self.aircraft.Altitude < self.Schedule[i][1]:
                        if type(self.Schedule[i][-1]) == str:
                            factor = self.Schedule[i][-1]
                            if factor == "kts":
                                factor = self.knots_to_mps
                            if factor == "Mach":
                                self.Mach = self.Schedule[i][0]
                                factor = self.aircraft.acousic_v
                        speed = self.Schedule[i][0]
                        self.aircraft.v = speed * factor
                        break

    def Add_Parameter(self, Run = True):
        if Run:
            self.AltitudeArr = np.append(self.AltitudeArr,self.aircraft.Altitude)
            self.vArr = np.append(self.vArr, self.aircraft.v * self.mps_to_knots)
            self.RangeArr = np.append(self.RangeArr, self.aircraft.Range)
            self.Power_ThrustArr = np.append(self.Power_ThrustArr, self.aircraft.Power_Thrust)
            self.ThrustArr = np.append(self.ThrustArr,self.aircraft.Thrust)
            self.percentArr = np.append(self.percentArr, self.aircraft.percent)
            self.EnduranceArr = np.append(self.EnduranceArr, self.aircraft.Endurance)
            self.EnergyMassArr = np.append(self.EnergyMassArr, self.aircraft.EnergyMass)
            self.C_DArr = np.append(self.C_DArr, self.aircraft.C_D)
        else:
            pass
    def TimestepBeta(self, dt = 10, AddPar = True):

        self.RangeArr = np.array([])
        self.PercArr = np.array([])

        while self.aircraft.Altitude < self.aircraft.CruiseAltitude and self.aircraft.Emergency == None:
            self.ClimbScheduleCheck()
            self.aircraft.Climb(dt = dt)
            self.aircraft.Range += self.aircraft.v_x * dt * self.m_to_nmi
            self.aircraft.Endurance += dt
            self.Add_Parameter(AddPar)
            self.aircraft.Emergency_Check()   
            if self.aircraft.Emergency != None:
                print("The Engines have failed")
                break
            if self.aircraft.Altitude > self.aircraft.CruiseAltitude:
                self.aircraft.Altitude = self.aircraft.CruiseAltitude
                self.Phase = "Cruise"
                print(f"{self.aircraft.AircraftName} is now cruising")
        while self.Phase == "Cruise" and self.aircraft.Emergency == None:
            self.aircraft.Cruise(dt = dt)
            self.aircraft.Range += self.aircraft.v_x * dt * self.m_to_nmi
            self.aircraft.Endurance += dt
            self.Add_Parameter(AddPar)
            self.aircraft.Emergency_Check()
            if round(self.aircraft.Endurance % 3600) == 0:
                print(self.aircraft.Endurance / 3600)

            if self.aircraft.EnergyMass < 0 or self.aircraft.Emergency != None:
                print("The Engines have failed")
                break
        while self.aircraft.Emergency == "No_Energy" and self.aircraft.Altitude > 0:
            self.aircraft.ZeroThrustGlide(dt = dt)
            self.aircraft.Range += self.aircraft.v_x * dt * self.m_to_nmi
            self.aircraft.Endurance += dt
            self.Add_Parameter(AddPar)
            self.aircraft.Emergency_Check
        print("Done")












"""
CS1 = 1000 #ft/min
CS2 = [(1000, 10000), 2000] #ft/min
CS3 = [(1000, 10000), (2000, 15000), 500] #ft/min
CS4 = [(250, 10000, "kts"), (300, 25000), (0.7, 30000, "Mach"), 1000]
CSPip = [(76, 10000, "kts"), 1000]
CS5 = [(250, 1000, 10000, "kts"), (300, 2000, 25000, "kts"), (0.7, 500, 30000, "Mach")]
"""