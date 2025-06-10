from ImportAPCSE import *
from PiperArcherIII_Blueprint import *
import pickle



####################################################
# Testing the Reserves Mission - why the f*ck is it burning so much energy - 30 minutes of a reserve is TOO MUCH for EV's

# print(ElectricArcherAircraft.Altitude)

# ElectricArcherAircraft.Altitude = 700
# ElectricArcherAircraft.V_infty = 76*ElectricArcherAircraft.knots_to_mps
# controlArcher.Reserves.Reserves(70)
# print(controlArcher.Reserves.Percent)
# exit()
####################################################
tol = 0.1


percent = 100

useReserve = True
electric = True

if useReserve:
    reserveText = "reserves"
else:
    reserveText = "no-reserves"


filepath = "DataFiles\\range_trade_dump\\piston\\".format(energyDensity, reserveText)
filepath = "DataFiles\\range_trade_dump\\electric\\energy-density-{}Wh_kg\\{}\\".format(energyDensity, reserveText)

if not os.path.exists(filepath):
    os.makedirs(filepath)


char = filepath[27]

#################################################################################
vInfty_arr = np.array([70, 80, 90, 100, 110, 120, 130, 140]).astype(float)
# vInfty_arr = [140]
h_p_arr = np.arange(500, 10500, 1000).astype(float)
# h_p_arr = [9500]
if char == "e":
    controlArcher = Control(ElectricArcherAircraft)
elif char == "p":
    controlArcher = Control(ArcherAircraft)
else:
    raise Exception("There's an error here buddy!")
#################################################################################


for vInfty in vInfty_arr:
    # Iterate over a range of velocities
    for h_p in h_p_arr:
        # Iterate over a range of altitudes
        if char == "e":
            Range = 20
        elif char == "p":
            Range = 300
        else:
            raise Exception("There's an error here buddy!")
        
        percent = 100
        # h_p = 10500; vInfty = 140
        while np.abs(percent) > tol or percent < 0:
            # Needs to ensure that most of the fuel is being used
            # while constraining the percent to be greater than 0 %
            if Range < 0:
                Range = 0
            print("\nTesting for Range: {} nmi at h_p: {} ft and vInfty: {} knots".format(Range, h_p, vInfty))
            data, bool = controlArcher.Range_Mission(Range, h_p, vInfty)
            ArcherAircraft.reset("Else")
            percent = data["percent"]
            if Range == 0 and percent < 0:
                break
            if np.abs(percent) < tol and percent < 0:
                Range -= tol*0.9
            else:
                if char == "e":
                    Range += percent
                elif char == "p":
                    Range += percent * 3.0
                else:
                    raise Exception("There's an error here buddy!")

        filename = "vInfty-{}_h_p-{}.pickle".format(vInfty,h_p,data["range [nmi]"])
        with open(filepath+filename, "wb") as file:
            pickle.dump(data, file)