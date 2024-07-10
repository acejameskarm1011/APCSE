import scipy as sp
from Aviation import Aviation
from Aerodynamic_Classes.Aerodynamics import Aerodynamics


import sys
sys.path.append("./Drag_Model/AE-298")

from CDo_wing import CDo_wing_calc
from CDo_vtail import CDo_vtail
from CDo_htail import CDo_htail
from CDo_fus import CDo_fus
from CDi_wing import CDi_wing_calc
from CDi_wing import induced_drag_htail
from CDi_wing import fuse_induced_drag
from CD_misc import CD_misc_calc

class Coefficients(Aviation):
    def __init__(self, External_Components) -> None:
        """
        Class used to evaluate the aircraft coefficients based on the airplane's current state.

        Parameters
        ---------
        External_Components : list
            All of the currently known external components for the aircraft
        """
        from Sizing_And_Geometry.ImportComponents import Wings, HorizontalStabilizer, VerticalStabilizer, Fuselage, LandingGear
        
        self.External_Components = External_Components
        for Component in External_Components:
            if isinstance(Component, LandingGear):
                self.LandingGear = Component
            if isinstance(Component, Wings):
                self.Wings = Component
            elif isinstance(Component, HorizontalStabilizer):
                self.HorizontalStabilizer = Component
            elif isinstance(Component, VerticalStabilizer):
                self.VerticalStabilizer = Component
            elif isinstance(Component, Fuselage):
                self.Fuselage = Component
            else:
                raise Exception("This Component is required")
        self.Freedom_Units()
        self.acousic_v = 1
        self.V_infty = 0
        self.Altitude = 0
        self.Ground_Effect = 1
        



    def Re(self):
        V_infty = self.V_infty
        L = self.Wings.c_bar
        Reynolds_Number = self.rho*L*V_infty/self.mu
        return Reynolds_Number

    def C_f(self):
        """
        WARNINGS!!! 
        Reynolds number and Mach number are currently not coded into this class as of yet
        """
        from CDo_fus import calcCf
        C_f = calcCf(self.Re(), self.Mach)
        for Component in self.External_Components:
            Component.C_f = C_f


    def Get_CD0_Wing(self):
        C_D0 = CDo_wing_calc(self.Re(), self.Mach, self.L_c_4_wing, self.tc_avg, self.S_wing, self.S_wet, self.tc_max_loc,
                             self.Lift_Force, self.vinf, self.density, self.tc_max, self.c_tip, self.c_root, self.S_wing, self.b_wing)
        self.Wings.C_D0 = C_D0
        return C_D0
    
    def Get_CD0_VerticalStabilizer(self):
        C_D0 = CDo_vtail(self.Re(), self.Mach, self.L_c_4_v, self.tc_max_loc_v, self.tc_avg_v, self.S_wing, self.S_v_wet, 
                         self.Lift_Force, self.vinf, self.density, self.tc_max_v, self.c_tip_v, self.c_root_v, 
                         self.S_wing, #use S_wing now according to simulink, but I think it should be s_h 
                         self.b_v)
        self.VerticalStabilizer.C_D0 = C_D0
        return C_D0
        
    def Get_CD0_HorizontalStabilizer(self):
        C_D0 = CDo_htail(self.Re(), self.Mach, self.L_c_4_h, self.tc_max_loc_h,self.tc_avg_h, self.S_wing,self.S_h_wet, 
                         self.Lift_Force, self.vinf, self.c_tip_h, self.c_root_h, self.b_h, self.S_wing, #use S_wing now according to simulink, but I think it should be s_h
                         self.density, self.tc_max_h)    
        self.HorizontalStabilizer.C_D0 = C_D0
        return C_D0
    
    def Get_CD0_Fuselage(self):
        C_D0 = CDo_fus(self.Re(), self.Mach, self.l_fus, self.d_fus, self.S_fus_wet, self.S_wing, self.S_fus_maxfront)  
        self.Fuselage.C_D0 = C_D0
        return C_D0
    
    def Get_CDi_Wing(self):
        C_Di = CDi_wing_calc(self.Mach, self.AR, self.L_c_4_wing, self.taper, 
                             self.density, self.vinf, self.rle, self.visc, self.b_wing, 
                             self.c_tip, self.c_root, self.C_l_alpha, 
                             self.Lift_Force, self.S_wing)
        self.Wings.C_Di = C_Di
        return C_Di

    def Get_CDi_HorizontalStabilizer(self):
        C_Di = induced_drag_htail(self.AR_h, self.S_h, self.S_wing, self.Lift_Force, self.density, self.vinf, self.S_wing)
        self.Wings.C_Di = C_Di
        return C_Di

    def Get_CDi_Fuselage(self):
        C_Di = fuse_induced_drag(self.C_l_0, self.l_fus, self.d_fus, self.Mach, self.S_wing, self.S_fus_plan, self.S_fus_b,
                                 self.Lift_Force, self.density, self.vinf, self.S_wing, self.b_wing, self.c_tip,
                                 self.c_root, self.C_l_alpha, self.AR,self.L_c_4_wing)
        self.Wings.C_Di = C_Di
        return C_Di
    
    def Get_C_D(self):
        C_D0 = self.Get_CD0_Wing() + self.Get_CD0_VerticalStabilizer() + self.Get_CD0_HorizontalStabilizer() + self.Get_CD0_Fuselage()
        C_Di = self.Get_CDi_Wing() + self.Get_CDi_HorizontalStabilizer() + self.Get_CDi_Fuselage()
        CD_misc_cons = 0.05
        CDo_pyl = 0
        CDo_nac = 0
        CD_misc_val = CD_misc_calc(CDo_pyl, self.Get_CD0_Fuselage(), self.Get_CD0_Wing(),CDo_nac,
                                   self.Get_CD0_VerticalStabilizer(), self.Get_CD0_HorizontalStabilizer(),CD_misc_cons)
        C_D = C_D0 + C_Di*self.Ground_Effect + CD_misc_cons + CDo_pyl + CDo_nac + CD_misc_val
        print(C_D)
        return C_D


    def Freedom_Units(self):
        # Wing parameters converted to imperial units
        self.L_c_4_wing = self.Wings.L_c_4_wing
        self.tc_avg = self.Wings.tc_avg
        self.S_wing = self.Wings.S_wing / sp.constants.foot**2
        self.S_wet = self.Wings.S_wet / sp.constants.foot**2
        self.tc_max_loc = self.Wings.tc_max_loc
        self.tc_max = self.Wings.tc_max
        self.c_tip = self.Wings.c_tip / sp.constants.foot
        self.c_root = self.Wings.c_root / sp.constants.foot
        self.b_wing = self.Wings.b_wing / sp.constants.foot
        self.AR = self.Wings.AR  
        self.taper = self.Wings.taper 
        self.C_l_alpha = self.Wings.C_l_alpha 
        self.C_l_0 = self.Wings.C_l_0
        self.rle = self.Wings.rle

        # Vertical Stabilizer Parameters
        self.L_c_4_v = self.VerticalStabilizer.L_c_4_v 
        self.tc_max_loc_v = self.VerticalStabilizer.tc_max_loc_v
        self.tc_avg_v = self.VerticalStabilizer.tc_avg_v
        self.S_v_wet = self.VerticalStabilizer.S_v_wet / sp.constants.foot**2
        self.tc_max_v = self.VerticalStabilizer.tc_max_v
        self.c_tip_v = self.VerticalStabilizer.c_tip_v / sp.constants.foot
        self.c_root_v = self.VerticalStabilizer.c_root_v / sp.constants.foot
        self.b_v = self.VerticalStabilizer.b_v / sp.constants.foot

        
        # Horizontal Stabilizer Parameters
        self.L_c_4_h = self.HorizontalStabilizer.L_c_4_h
        self.tc_max_loc_h = self.HorizontalStabilizer.tc_max_loc_h
        self.tc_avg_h = self.HorizontalStabilizer.tc_avg_h
        self.S_h_wet = self.HorizontalStabilizer.S_h_wet / sp.constants.foot**2
        self.c_tip_h = self.HorizontalStabilizer.c_tip_h / sp.constants.foot
        self.c_root_h = self.HorizontalStabilizer.c_root_h / sp.constants.foot
        self.b_h = self.HorizontalStabilizer.b_h / sp.constants.foot
        self.tc_max_h = self.HorizontalStabilizer.tc_max_h
        self.AR_h = self.HorizontalStabilizer.AR_h
        self.S_h = self.HorizontalStabilizer.S_h / sp.constants.foot**2

        # Fuselage Parameters
        self.l_fus = self.Fuselage.l_fus / sp.constants.foot
        self.d_fus = self.Fuselage.d_fus / sp.constants.foot
        self.S_fus_wet = self.Fuselage.S_fus_wet / sp.constants.foot**2
        self.S_fus_maxfront = self.Fuselage.S_fus_maxfront / sp.constants.foot**2
        self.S_fus_plan = self.Fuselage.S_fus_plan / sp.constants.foot**2 
        self.S_fus_b = self.Fuselage.S_fus_b / sp.constants.foot**2


    def __setattr__(self, name, value) -> None:
            if name == "V_infty":
                if value < 2:
                    value = 2
                self.vinf = value / sp.constants.foot
                self.Mach = value / self.acousic_v
            object.__setattr__(self, name, value)
            
            if name == "Lift":
                self.Lift_Force = value / sp.constants.pound
            if name == "Altitude":
                if isinstance(value, (float, int)):
                    self.Atmosphere_attr()
                    self.Mach = self.V_infty / self.acousic_v
                    self.density = self.rho / sp.constants.slug*sp.constants.foot**3
                    self.visc = self.mu / sp.constants.slug*sp.constants.foot
                    if value < self.b_wing:
                        self.Ground_Effect = (16*value/self.b_wing)**2/(1 + (16*value/self.b_wing)**2) # McCormick Appoximation for Ground Effect
                else: 
                    raise TypeError("Cannot accept value of type {}".format(type(value)))