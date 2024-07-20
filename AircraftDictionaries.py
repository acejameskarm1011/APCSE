#AircraftDictionaries
import os
import numpy as np
import scipy as sp
def Dict2SI(ACDict):
    for key in ACDict:
        if key == "Name":
            pass
        else:
            for subkey in ACDict[key]:
                SubDictionary = ACDict[key]
                DictEntry = SubDictionary[subkey]
                if isinstance(DictEntry, type([])):
                    UnitType = DictEntry[-1]
                    if UnitType[0:2] == 'ft':
                        SubDictionary[subkey] = SubDictionary[subkey][0] * 0.3048
                        if UnitType[-1] == '2':
                            SubDictionary[subkey] *= 0.3048
                    elif UnitType == 'invdeg':
                        SubDictionary[subkey] = SubDictionary[subkey][0]*180/np.pi
                    elif UnitType == 'in':
                        SubDictionary[subkey] = SubDictionary[subkey][0]*sp.constants.inch
                    elif UnitType == 'lbf':
                        SubDictionary[subkey] = SubDictionary[subkey][0] * 0.45359237
                    elif UnitType == "deg" or UnitType == "m" or UnitType == "m2" or UnitType == "N" or UnitType == "rad" or UnitType == "kg" or UnitType == "W" or UnitType=="None":
                        SubDictionary[subkey] = SubDictionary[subkey][0]
                    elif UnitType == "kts" or UnitType == "knots":
                        SubDictionary[subkey] = SubDictionary[subkey][0]*0.514444
                    elif UnitType == "hp":
                        SubDictionary[subkey] = SubDictionary[subkey][0]*745.7
                    else:
                        print("You missed ONE!!!!")
                        return None
    return ACDict

main_dir = os.getcwd()
dict_dir = main_dir + r'\Aircraft_Dictionaries'




from Aircraft_Dictionaries.PA_28_181 import PA_28_181_Dict
from Aircraft_Dictionaries.Embraer175 import Embraer175_Dict




PiperArcherIII_Dict = Dict2SI(PA_28_181_Dict)
Embraer175_Dict = Dict2SI(Embraer175_Dict)