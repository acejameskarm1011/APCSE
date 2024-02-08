#Engine
import os
engine_dir = os.getcwd()
main_dir = "C:\APCSE"
os.chdir(main_dir)
from AtmosphereFunction import AtmosphereFunctionSI
os.chdir(engine_dir)


class Powerplant:
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







class EngineTest:
    def __init__(self, Name, mass, HF) -> None:
        self.Name = Name
        self.mass = mass
        self.HF = HF
        self.h = 0
    def __repr__(self) -> str:
        return f'EngineTest({self.Name}, {self.mass}, {self.HF})'

