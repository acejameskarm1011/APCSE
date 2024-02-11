import numpy as np
import matplotlib.pyplot as plt
from AtmosphereFunction import AtmosphereFunctionSI
import os
import scipy as sp

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
    Class has very few methods, and most code work will need to built up with other child classes
    """

    # Multiply by these factors to go from the left units to the right units
    m_to_ft = 1/sp.constants.foot
    ft_to_m = sp.constants.foot
    m_to_nmi = 1/sp.constants.nautical_mile
    nmi_to_m = sp.constants.nautical_mile
    knots_to_mps = sp.constants.knot
    mps_to_knots = 1/sp.constants.knot
    fps_to_knots = sp.constants.foot/sp.constants.knot
    knots_to_fps = sp.constants.knot/sp.constants.foot

    def __init__(self, Altitude = 0) -> None:
        self.Altitude = Altitude
        self.Atmosphere_attr()

    def Atmosphere_attr(self) -> None:
        """
        Updates the atmospheric attributes within an object based on the aircraft's inheriant altitude

        Parameters
        ----------
        This function requires no parameters. Call this function in a single line within a an instance method or on an instance of a class

        Returns
        -------
        None

        Notes
        -----
        Make sure the class with this function being called within has a value for self.Altitude.
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