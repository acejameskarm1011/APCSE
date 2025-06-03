from ImportAPCSE import *
# from PiperArcherIII_Blueprint import *
import pickle

# Unpickling (Deserialization)
filepath = r"C:\APCSE\DataFiles\range_trade_dump\electric\energy-density-265Wh_kg\reserves"

import os
# Get the list of all files and directories
path = filepath
dir_list = os.listdir(path)
print("Files and directories in '", path, "' :")
# prints all files
print(dir_list)



# h_p = 500
# vInfty = 80
# Range = 0
Range_List = []
vInfty_List = []
h_p_List = []
for filename in dir_list:
    with open(filepath+"\\"+filename, 'rb') as file:
        loaded_data = pickle.load(file)
    Range_List.append(loaded_data["range [nmi]"])
    h_p_List.append(loaded_data["h_p [ft]"])
    vInfty_List.append(loaded_data["vInfty [knots]"])
    # print(loaded_data["range [nmi]"])
Range_List = np.array(Range_List)
vInfty_List = np.array(vInfty_List)
h_p_List = np.array(h_p_List)

RangeMax = Range_List.max()
vInfty_maxRange = vInfty_List[Range_List==RangeMax][0]
hp_maxRange = h_p_List[Range_List==RangeMax][0]

print("Max range found: {} nmi at h_p: {} ft and vInfty: {} knots".format(RangeMax, hp_maxRange, vInfty_maxRange))