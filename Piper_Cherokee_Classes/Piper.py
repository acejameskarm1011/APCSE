import os
piper_path = os.getcwd()
main_path = piper_path[:-23]
os.chdir(main_path)
from Aviation import *
from AtmosphereFunction import *
os.chdir(piper_path)

class Piper(Aviation):
    def __init__(self, AircraftName, CruiseMach, CruiseAltitude, AircraftType) -> None:
        super().__init__(AircraftName, CruiseMach, CruiseAltitude, AircraftType)
    
