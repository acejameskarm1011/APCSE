import os
ga_path = os.getcwd()
main_path = ga_path[:-23]
os.chdir(main_path)
from Aviation import *
from AtmosphereFunction import *
os.chdir(ga_path)

class GAAircraft(Aviation):
    def __init__(self, AircraftName, CruiseMach, CruiseAltitude, AircraftType) -> None:
        super().__init__(AircraftName, CruiseMach, CruiseAltitude, AircraftType)
    
