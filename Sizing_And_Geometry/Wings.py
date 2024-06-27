from Aircraft import Aircraft
import numpy as np

# from Aerodynamic_Classes.C_D import * 


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


        ################
        self.alpha = 3
        # self.alpha = 0
        self.tau = 0
        self.C_l_alpha = 0.11031
        self.C_L_alpha = self.C_l_alpha/(1 + self.C_l_alpha/(np.pi*self.AR)*(1 + self.tau))
        self.C_L_0 = .6
        ###########



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



        C_D_0 = 0.0296*1.4
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
        C_L = self.C_L_0 + self.C_L_alpha*self.alpha
        self.C_L = C_L
        return C_L
    def Set_C_L(self, C_L):
        self.C_L = C_L
        self.alpha = (C_L - self.C_L_0)/(self.C_L_alpha)
        
    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)
        if name == "Altitude":
            self.Atmosphere_attr()

    