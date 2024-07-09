from Aviation import Aviation
from Aerodynamic_Classes.Aerodynamics import Aerodynamics
from Sizing_And_Geometry.ImportComponents import Wings, HorizontalStabilizer, VerticalStabilizer, Fuselage, LandingGear

import sys
sys.path.append("./Drag_Model/AE-298")


class Coefficients(Aviation):
    def __init__(self, External_Components) -> None:
        """
        Class used to evaluate the aircraft coefficients based on the airplane's current state.

        Parameters
        ---------
        External_Components : list
            All of the currently known external components for the aircraft
        """
        self.Altitude = 0
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



    def Re(self):
        V_infty = self.V_infty
        L = self.Wings.c_bar
        Reynolds_Number = self.rho*L*V_infty/self.mu

    def C_f(self):
        """
        WARNINGS!!! 
        Reynolds number and Mach number are currently not coded into this class as of yet
        """
        from CDo_fus import calcCf
        C_f = calcCf(self.Re(), self.Mach)
        for Component in self.External_Components:
            Component.C_f = C_f

    