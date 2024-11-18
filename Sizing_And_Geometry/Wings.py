import sys
sys.path.append("./Drag_Model/AE-298")
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
        self.taper = self.c_tip/self.c_root
        self.e_0 = 1.78*(1-0.045*self.AR**(0.68)) - 0.64
        self.Flaps(0)

        self.C_L_0 = self.C_l_0

        ################
        self.alpha_crit = 12
        self.alpha_0 = 2.5 # Make sure it stays at 3 deg for Landing ground roll
        self.alpha = self.alpha_0
        # self.alpha = 0
        self.tau = 0
        self.C_L_alpha = self.C_l_alpha/(1 + self.C_l_alpha/(np.pi*self.AR)*(1 + self.tau))
        # There is a better equation to use for evaluating C_L_alpha in Raymer 7th p414
        
        ###########

        self.Ground_Effect = 1
        self.Phase = ""

    def reset(self):
        self.alpha = self.alpha_0

    def Get_C_D0(self):
        raise Exception("This function shouldn't be called anymore!")
        CDo_wing_calc(re, mach, sweep, tc_avg, sref, swet, maxtcloc, Weight, vinf, rho, tcmax, ctip, croot, Wsref, Span)


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
        raise Exception("This function shouldn't be called anymore!")



        C_D_0 = 0.08 + self.C_D_flaps
        C_Di = self.Get_C_Di()
        C_D = C_D_0 + C_Di
        self.C_D = C_D

        if self.Phase == "Cruie":
            print("C_D_0: {}\nC_Di: {}\nC_D: ".format(C_D_0, C_Di))
            exit()

        # Total Drag should around 0.86 at sea level and at 90 knots / 1.135 Mach
        return C_D
    
    def Get_C_Di(self):
        raise Exception("This function shouldn't be called anymore!")

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
        C_L = self.C_L_0 + self.C_l_alpha*self.alpha + self.C_L_flaps
        self.C_L = C_L
        return C_L
    


    def Set_C_L(self, C_L):
        """
        This method sets the aircraft's current angle of attack based on a desired coefficient of lift. Using the linear approximation for
        for how C_L scales with AOA, we solve for the AOA. However, if the found AOA is larger than the critical AOA, then the AOA will be forced
        to stay at or below the critical value. 

        Parameters
        ---------

        """
        self.C_L = C_L
        self.alpha = (C_L - self.C_L_0-self.C_L_flaps)/(self.C_l_alpha)
        if self.alpha > self.alpha_crit:
            pass
            # print(self.C_L)
        elif self.alpha > self.alpha_crit*1.2:
            raise Exception("Angle Attack Value: {} deg is not valid".format(self.alpha))
        #     self.alpha = self.alpha_crit

    def Flaps(self, deg):
        factor = deg / 40
        self.C_L_flaps = 0.02 * factor
        self.C_D_flaps = 0.08 * factor



    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)
        if name == "Altitude":
            if value < self.b_wing:
                self.Ground_Effect = (16*(value+10)/self.b_wing)**2/(1 + (16*(value+10)/self.b_wing)**2) # McCormick Appoximation for Ground Effect
            self.Atmosphere_attr()
        if name == "Phase":
            if name == "Take-Off":
                self.alpha = self.alpha_0
            if name == "Landing":
                self.alpha = self.alpha_0

    def __repr__(self) -> str:
          return "Wings: {}".format(self.Name)
    