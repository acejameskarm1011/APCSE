from Aircraft import Aircraft
import numpy as np
class Wings(Aircraft):
    """
    This class stores all necessary methods for storing the necessary geometry and data of the wings for an aircraft.

    Paramters
    ---------

    AircraftName : str
        This parameter is important so that when displaying test statements, we know what instance of the wings are being used.
    
    Notes
    -----
    This class is still under progress
    """
    PartName = "Wings"
    def __init__(self, AircraftName, AircraftDict) -> None:
        self.AircraftName = AircraftName
        self.Name = self.AircraftName + self.PartName
        self.Dictionary_setattr(AircraftDict[self.PartName])
        self.AR = self.b_wing**2/self.S_wing
        self.e_0 = 1.78*(1-0.045*self.AR**(0.68)) - 0.64
        self.K = 1/(np.pi*self.e_0*self.AR)
        self.alpha = 3/180*np.pi
    def Get_C_D(self):
        """
        Method to retrieve the coefficient of lift from the Wings

        Parameters
        ----------
        alpha : int or float
            Angle of Attack in degrees
        
        Returns
        -------
        C_D : float
            Coefficient of drag

        Notes
        -----
        This uses the airfoil approximation for the drag coefficient, and this should not be used for official end use.
        """

        C_D_0 = 0.0296
        C_D = C_D_0 + self.K*self.Get_C_L()**2
        self.C_D = C_D
        return C_D
    def Get_C_L(self):
        """
        Method to retrieve the coefficient of lift from the Wings

        Parameters
        ----------
        alpha : int or float
            Angle of Attack in degrees
        Returns
        -------
        C_L : float
            Coefficient of lift
        Notes
        -----
        This uses the airfoil approximation for the drag coefficient, and this should not be used for official end use.
        """
        C_L_0 = .7463
        C_L_0 = .45
        C_L = C_L_0 + 2*np.pi*(self.alpha)
        self.C_L = C_L
        return C_L
    def Set_C_L(self, C_L):
        C_L_0 = .7463
        self.alpha = (C_L - C_L_0)/(2*np.pi)