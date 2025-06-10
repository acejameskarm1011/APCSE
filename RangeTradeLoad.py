from ImportAPCSE import *
# from PiperArcherIII_Blueprint import *
import pickle
import os

filepaths = [r"C:\APCSE\DataFiles\range_trade_dump\electric\energy-density-265Wh_kg\reserves", r"C:\APCSE\DataFiles\range_trade_dump\piston"]
# Unpickling (Deserialization)
# filepath = r"C:\APCSE\DataFiles\range_trade_dump\electric\energy-density-265Wh_kg\reserves"

missionTypes = ["electric_reserves", "piston"]
for missionType, filepath in zip(missionTypes, filepaths):
    # Get the list of all files and directories
    path = filepath
    dir_list = os.listdir(path)
    print("Files and directories in '", path, "' :")

    # h_p = 500
    # vInfty = 80
    # Range = 0
    Range_List = []
    vInfty_List = []
    h_p_List = []
    full = []
    for filename in dir_list:
        with open(filepath+"\\"+filename, 'rb') as file:
            loaded_data = pickle.load(file)
        Range_List.append(loaded_data["range [nmi]"])
        h_p_List.append(loaded_data["h_p [ft]"])
        vInfty_List.append(loaded_data["vInfty [knots]"])
        full.append([loaded_data["h_p [ft]"], loaded_data["vInfty [knots]"], loaded_data["range [nmi]"]])
        # print(loaded_data["range [nmi]"])
    Range_List = np.array(Range_List)
    vInfty_List = np.array(vInfty_List)
    h_p_List = np.array(h_p_List)
    full = np.array(full)

    vArr = []
    hpArr = []
    for v in vInfty_List:
        if v not in vArr:
            vArr.append(v)
    for h in h_p_List:
        if h not in hpArr:
            hpArr.append(h)

    vArr.sort()
    hpArr.sort()

    vhUnsorted = full[:,:2]
    RangeSorted = []
    X, Y = np.meshgrid(vArr, hpArr)
    R = np.zeros(X.shape)

    for i, h in enumerate(hpArr):
        for j, v in enumerate(vArr):
            sub_array = np.array([h,  v])
            index = None
            for k in range(vhUnsorted.shape[0]):
                if np.array_equal(sub_array, vhUnsorted[k]):
                    index = k
            if index == None:
                raise Exception("Cry")
            R[i,j] = Range_List[index]



    RangeMax = Range_List.max()
    vInfty_maxRange = vInfty_List[Range_List==RangeMax][0]
    hp_maxRange = h_p_List[Range_List==RangeMax][0]
    figsize = (5,6)
    plt.figure(figsize=figsize, constrained_layout = True)
    contour = plt.contourf(X, Y, R, levels = 50, cmap="inferno", vmin = 0)
    bar = plt.colorbar(contour)
    bar.set_label("Range [nmi]")
    plt.xlabel(r"Cruise Speed - ($V_\infty$) [knots]")
    plt.ylabel(r"Cruise Altitude - ($h$) [ft]")
    plt.gca().yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
    hp_maxRange_str = str(int(hp_maxRange))
    if len(hp_maxRange_str) == 4:
        hp_maxRange_str = hp_maxRange_str[0] + "," + hp_maxRange_str[1:]
    plt.plot(vInfty_maxRange, hp_maxRange, "ro", label = "Maximum Range: {} nmi \nat {} knots and {} ft".format(round(RangeMax), int(vInfty_maxRange), hp_maxRange_str))
    plt.legend()

    plt.savefig("Images_From_Code\\Range_Trade\\{}.png".format(missionType))
    # plt.show()
    print("Max range found: {} nmi at h_p: {} ft and vInfty: {} knots".format(RangeMax, hp_maxRange, vInfty_maxRange))