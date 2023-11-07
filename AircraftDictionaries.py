#AircraftDictionaries
import os
import numpy as np
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
                    elif UnitType == 'deg':
                        SubDictionary[subkey] = SubDictionary[subkey][0]/180*np.pi
                    elif UnitType == 'invdeg':
                        SubDictionary[subkey] = SubDictionary[subkey][0]*180/np.pi
                    elif UnitType == 'lbf':
                        SubDictionary[subkey] = SubDictionary[subkey][0] * 0.45359237
                    elif UnitType == "m" or UnitType == "m2" or UnitType == "N" or UnitType == "rad" or UnitType == "kg":
                        SubDictionary[subkey] = SubDictionary[subkey][0]
                    else:
                        print("You missed ONE!!!!")
                        return None
                        break
                        print("You missed ONE!!!!")
    return ACDict

main_dir = os.getcwd()
dict_dir = main_dir + '.\Aircraft_Dictionaries'



os.chdir(dict_dir)
from Embraer175 import Embraer175_Dict
from PA28 import PA28_Dict
os.chdir(main_dir)



PiperArcherIII_Dict = Dict2SI(PA28_Dict)
Embraer175_Dict = Dict2SI(Embraer175_Dict)