import scipy as sp
import numpy as np
from Control.MissionPhase.MissionPhase import MissionPhase


class Descent(MissionPhase):

    def NoFlaps_Descent(self):
        self.V_infty = 70 * self.knots_to_mps
        gamma = -3/180*np.pi
        Velocity = self.V_infty*np.array([np.cos(gamma),0,np.sin(gamma)])
        self.Aircraft.Velocity = Velocity
        self.Aircraft.Pitch = gamma
        self.Aircraft.Set_Forces()
        self.Get_Aircraft_Attr()





    def Get_Aircraft_Attr(self):
        super().Get_Aircraft_Attr()
        self.Altitude = self.Aircraft.Altitude


    def Save_Data(self):
        super().Save_Data()
        if not hasattr(self, "Altitude_List"):
            self.Altitude_List = [self.Altitude]
        else:
            self.Altitude_List.append(self.Altitude)
        if not hasattr(self, "Pitch_List"):
            self.Pitch_List = [self.Pitch]
        else:
            self.Pitch_List.append(self.Pitch)