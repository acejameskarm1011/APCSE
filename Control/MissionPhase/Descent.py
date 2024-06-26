import scipy as sp
import numpy as np
from Control.MissionPhase.Climb import Climb
from math import copysign

class Descent(Climb):

    def NoFlaps_Descent_Kinematics(self):
        self.V_infty = 70 * self.knots_to_mps
        gamma = -3/180*np.pi
        Velocity = self.V_infty*np.array([np.cos(gamma),0,np.sin(gamma)])
        self.Aircraft.Velocity = Velocity
        self.Aircraft.Pitch = gamma
        self.Aircraft.Set_Forces()
        self.Get_Aircraft_Attr()

    def NoFlaps_Descent(self):
        self.V_des = 70 * self.knots_to_mps
        self.RPM = 2200
        self.MaxRPM = self.Aircraft.Engine.MaxRPM


        """
        Future plans for tomorrow hope to see how and when the engine setting should change. Should I update it within the Pitch_EOM function?
        Certainly not, as that will cause complications when the engine is at a different setting than what was expected. Should I add the engine
        RPM to the equations of motion? Maybe...

        It isn't a state variable, so I don't see why it would fit, but I do think that it could be valuable to investigate and see if that is a valid
        choice to make here. It would help with the saving of that information. Now the only thing left is to see where I could fit the whole solution.
        More abstraction, less abstration, and where and why? All of these questions, I will tackle in the morning, or maybe right after taking a shower
        """

    def Pitch_EOM(self, Dot, mass):
        x, y, z, V_infty, Pitch = Dot

        return super().Pitch_EOM(Dot, mass)
    
    def delta_RPM(self, V_infty):
        """
        This method will automatically update what the change in RPM of the engine should be
        """
        V_des = self.V_des
        if abs(V_des-V_infty) <= 1.5:
            self.RPM += (V_des-V_infty)/V_des*self.MaxRPM
        else:
            self.RPM += copysign(1/27, V_des-V_infty)

    def __setattr__(self, name: str, value: np.Any) -> None:
        object.__setattr__(self, name, value)
        if name == "RPM":
            self.Aircraft.Set_RPM(self.RPM)