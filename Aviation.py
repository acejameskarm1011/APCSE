import numpy as np
from matplotlib import pyplot as plt
from AtmosphereFunction import AtmosphereFunctionSI
import os

class Aviation: 
    """
    Stores data that needs to be held within every class in the program. 
    


    Parameters
    ----------
    Altitude : int or float, optional
        Altitude is automatically set to 0 m above sea level
    
    Key Points
    ----------
     - Contains the unit conversions
     - Contains class methods that update specific variables that are shared within the system
     - Contains instance methods which are used throughout

    Notes
    -----
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

    def __init__(self, Altitude = 0) -> None:
        self.Altitude = Altitude
        self.Atmosphere_attr()
    
    def Atmosphere_attr(self) -> None:
        """
        Updates the atmospheric attributes within an object based on the aircraft's inheriant altitude

        Parameters
        ----------
        None
            Call this function in a single line within a an instance method or on an instance of a class
        Returns
        -------
        None
        """
        self.acousic_v, self.g, self.Pressure, self.Temperature, self.rho, self.mu = AtmosphereFunctionSI(self.Altitude, ['a','g','P','T', 'rho','mu'])               

    def Dictionary_setattr(self, Dictionary):
        """
        Adds the items of a dictionary to an instance of a class. All of the keys of the dictionary will become attributes for the class, 
        and the values for the keys will automatically be updated for the instance of the class.

        Parameters
        ----------

        Dictionary : dict
            A dictionary must be passed as an argument into the method

        Returns
        ------
        None
        """
        for key in Dictionary:
            setattr(self, key, Dictionary[key])
test = Aviation()
test.Atmosphere_attr()
print(test.__dict__)