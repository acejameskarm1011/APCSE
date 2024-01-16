import numpy as np
from matplotlib import pyplot as plt
from AtmosphereFunction import AtmosphereFunctionSI
import os

class Aviation: 
    """
    Stores data that needs to be held within every class in the program. 
     - Contains the unit conversions
     - Contains class methods that update specific variables that are shared within the system
     - Contains instance methods which are used throughout
    """

    # Multiply by these factors to go from the left units to the right units
    m_to_ft = 1/0.3048
    ft_to_m = 0.3048
    m_to_nmi = 1/1852
    nmi_to_m = 1852
    knots_to_mps = 0.51444
    mps_to_knots = 1/0.51444
    fps_to_knots = 0.592484
    knots_to_fps = 1/0.592484 

    def __init__(self, Name, Altitude = 0) -> None:
        self.AircraftName = Name
        self.Altitude = Altitude
    def __str__(self):
        return f"This aircraft is the {self.AircraftName}, and it can fly a maximum of {self.Endurance}nmi for {self.Range} minutes and a cruise speed of {self.Mach} Mach"

    def Atmosphere_attr(self) -> None:
        """
        Updates the atmospheric attributes of the object based on altitude
        """
        self.acousic_v, self.g, self.Pressure, self.Temperature, self.rho, self.mu = AtmosphereFunctionSI(self.Altitude, ['a','g','P','T', 'rho','mu'])               

    def Dictionary_setattr(self, Dictionary):
        for key in Dictionary:
            setattr(self, key, Dictionary[key])
        return None
test = Aviation('test')
test.Atmosphere_attr()
print(test.__dict__)