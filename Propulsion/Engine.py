#Engine
import os
engine_dir = os.getcwd()
main_dir = "C:\APCSE"
os.chdir(main_dir)
from AtmosphereFunction import AtmosphereFunctionSI
from Aviation import Aviation
os.chdir(engine_dir)
import scipy as sp

class Powerplant(Aviation):
    hp_to_watt = sp.constants.hp
    def __init__(self) -> None:
        pass

class TurboFan(Powerplant):
    pass

class TurboJet(Powerplant):
    pass

class PropEngine(Powerplant):
    pass

class TurboProp(PropEngine):
    pass







class EngineTest(Powerplant):
    """
    This class is not completeled. Current goal is to use this as the basis for aquiring the trust, power and fuel drain from the aircraft.

    Parameters
    ---------
    Name : string
        Name of the aircraft or engine of interest
    MaxPower : int/float
        Rated power of the engine in terms of [hp]
    """
    def __init__(self, Name, MaxPower = 180) -> None:
        self.Name = Name
        self.MaxPower = MaxPower * self.hp_to_watt

    def Get_Thrust(self, v_infty):
        v_j = 5 # m/s
        Idle_Trust = self.MaxPower / v_j
        if v_infty <= 5:
            Thrust = Idle_Trust
        else: 
            Thrust = self.MaxPower / v_infty
        return Thrust