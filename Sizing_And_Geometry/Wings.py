import sys
sys.path.append("./Drag_Model/AE-298")
from Aircraft import Aircraft
import numpy as np
from Wing_Theory.airfoil_3D_interp import ThreeDim_Interp
# from Airfoils.airfoil_analysis import C_l_0


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
        self.S_ref = self.S_wing
        self.taper = self.c_tip/self.c_root
        self.e_0 = 1.78*(1-0.045*self.AR**(0.68)) - 0.64
        self.Flaps(0)

        self.C_L_0 = self.C_l_0

        ################
        self.alpha_crit = 12
        self.alpha_0 = 3 # Make sure it stays at 3 deg for Landing ground roll
        self.alpha = self.alpha_0
        # self.alpha = 0
        self.tau = 0
        self.C_L_alpha = self.C_l_alpha/(1 + self.C_l_alpha/(np.pi*self.AR)*(1 + self.tau))
        # There is a better equation to use for evaluating C_L_alpha in Raymer 7th p414


        #######################
        # Wing Theory evaluation
        from Wing_Theory.wing_analysis import C_l_max
        self.method = "AVL"
        if self.method == "LLT":
            from Wing_Theory.wing_analysis import C_L_0, C_L_alpha
        elif self.method == "AVL":
            from AVL.wing_analysis import C_L_0, C_L_alpha
            print("Using AVL code for lift performance")
        self.C_L_0 = C_L_0
        self.C_L_alpha = C_L_alpha
        self.C_L_max = C_l_max
        self.C_L_max = 2550 / (0.002377 * 0.5 * (60 * self.knots_to_fps)**2 * (self.S_ref * self.m_to_ft**2))
        self.alpha_crit = int((self.C_L_max - self.C_L_0)/self.C_L_alpha)
        #######################

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

        # method = "threeD"

        if self.method == "threeD":
            Re = self.V_infty*self.rho*self.c_bar/self.mu
            self.C_l = ThreeDim_Interp(Re, AOA = self.alpha)
            self.C_L = self.C_l*self.AR/(self.AR+2)
            return self.C_L
        else:
            self.C_L_clean = self.C_L_0 + self.C_l_alpha*self.alpha
            self.C_L = self.C_L_clean + self.C_L_flaps
            return self.C_L
    


    def Set_C_L(self, C_L):
        """
        This method sets the aircraft's current angle of attack based on a desired coefficient of lift. Using the linear approximation for
        for how C_L scales with AOA, we solve for the AOA. However, if the found AOA is larger than the critical AOA, then the AOA will be forced
        to stay at or below the critical value. 

        Parameters
        ---------

        """
        method = "threeD"

        if self.method == "threeD":
            self.C_L = C_L
            C_l = self.C_L*(self.AR+2)/self.AR
            self.alpha = ThreeDim_Interp(Re = self.V_infty*self.rho*self.c_bar/self.mu, C_l = C_l)
        else:
            self.C_L_clean = C_L - self.C_L_flaps
            self.alpha = (C_L - self.C_L_0-self.C_L_flaps)/(self.C_L_alpha)


        if self.alpha > self.alpha_crit*1.2:
            raise Exception("Angle Attack Value: {} deg is not valid".format(self.alpha))
        #     self.alpha = self.alpha_crit

    def Flaps(self, deg):
        factor = deg / 40
        
        self.C_L_flaps = 0.9 * self.dCl_max * self.S_flapped / self.S_ref * np.cos(self.Sweep_HL) * factor
        if deg < 10:
            deg = 10
        self.C_D0_flaps = self.F_flap * self.c_f/self.c_root * self.S_flapped/self.S_ref * (deg - 10)
        self.C_Di_flaps = self.k_f**2 * (self.C_L_flaps)**2 * np.cos(self.Sweep_HL)
        self.C_D_flaps = self.C_D0_flaps + self.C_Di_flaps
        # self.C_L_flaps = 0.02 * factor
        # self.C_D_flaps = 0.08 * factor



    def __setattr__(self, name, value):
        if name == "V_infty":
            self.Mach = value / self.acousic_v 
        object.__setattr__(self, name, value)
        if name == "Altitude":
            if value < self.b_wing:
                h_archer = 2.1352 * self.ft_to_m
                self.Ground_Effect = (16*(value+h_archer)/self.b_wing)**2/(1 + (16*(value+h_archer)/self.b_wing)**2) # McCormick Appoximation for Ground Effect
                limit = 0.5
                if self.Ground_Effect < limit:
                    self.Ground_Effect = limit
            self.Atmosphere_attr()
            if hasattr(self, "V_infty"):
                self.Mach = self.V_infty / self.acousic_v
        if name == "Phase":
            if name == "Take-Off":
                self.alpha = self.alpha_0
            if name == "Landing":
                self.alpha = self.alpha_0
       



    def __repr__(self) -> str:
          return "Wings: {}".format(self.Name)