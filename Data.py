from dataclasses import dataclass

@dataclass
class Data:
    """
    Type : What data is being stored
    
    MissionType : Mission analysis being done

    Units : The units of measurement for the amount

    MGTOW_Percent : Percent of Mass over max possible
    
    Amount : The number amount of the data
    """
    Type : str
    MissionType : str
    Units : str
    MGTOW_Percent : float
    Amount : float

class Aggregate:
    def __init__(self, MissionType, MGTOW_Percent):
        self.MissionType = MissionType
        self.MGTOW_Percent = MGTOW_Percent
        self.Types = ["CO2", "CH4", "N2O", "Pb", "Take_Off_Ground_Roll", "Final_Percent"]
        self.CO2 = []
        self.CH4 = []
        self.N2O = []
        self.Pb = []
        self.Take_Off_Ground_Roll = []
        self.Final_Percent = []
        

    def Add_Data(self, Type, value):
        if Type not in self.Types:
            raise NameError("This is not a data type that is being stored at this time.")
        if Type == "Take_Off_Ground_Roll":
            Units = "ft"
        elif Type == "Final_Percent":
            Units = "None"
        else:
            Units = "g"
        Element = Data(Type, self.MissionType, Units, self.MGTOW_Percent, value)
        getattr(self, Type).append([self.MGTOW_Percent, Element])

        
MissionData = Aggregate("Pattern", 0.80)
MissionData.Add_Data("Take_Off_Ground_Roll", 700)