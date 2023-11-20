import os
from Aviation import *
from AtmosphereFunction import *


class GAAircraft(Aviation):
    def __init__(self, AircraftName, CruiseMach, CruiseAltitude, AircraftType) -> None:
        super().__init__(AircraftName, CruiseMach, CruiseAltitude, AircraftType)
    
