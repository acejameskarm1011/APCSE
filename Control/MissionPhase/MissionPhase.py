from Control.Control import Control
from Propulsion.Engine import ElectricEngineTest
class MissionPhase(Control):
    weather = "Good"
    def __init__(self, AircraftInstance) -> None:
        self.aircraft = AircraftInstance

    def Get_Aircraft_Attr(self):
        """
        Get all needed aircraft attributes for a desired mission phase.
        """
        self.aircraft.Aircraft_Forces()
        self.Lift = self.aircraft.Lift
        self.Drag = self.aircraft.Drag
        self.Weight = self.aircraft.Weight
        self.Thrust = self.aircraft.Thrust
        
        if isinstance(self.aircraft.Engine, ElectricEngineTest):
            self.Percent = 100*self.aircraft.BatteryRatio
        else:
            self.Percent = 100*self.aircraft.FuelRatio
            

    @classmethod
    def changeweather(cls, text):
        cls.weather = text
    def Save_Data(self):
        if not hasattr(self, "Lift_List"):
            self.Lift_List = [self.Lift]
        else:
            self.Lift_List.append(self.Lift)

        if not hasattr(self, "Thrust_List"):
            self.Thrust_List = [self.Thrust]
        else:
            self.Thrust_List.append(self.Thrust)

        if not hasattr(self, "Drag_List"):
            self.Drag_List = [self.Drag]
        else:
            self.Drag_List.append(self.Drag)

        if not hasattr(self, "Weight_List"):
            self.Weight_List = [self.Weight]
        else:     
            self.Weight_List.append(self.Weight)
        
        if not hasattr(self, "Percent_List"):
            self.Percent_List = [self.Percent]
        else:
            self.Percent_List.append(self.Percent)


class subphase(MissionPhase):
    pass