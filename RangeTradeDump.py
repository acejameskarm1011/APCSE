from ImportAPCSE import *
from PiperArcherIII_Blueprint import *
import pickle

MGTOWCase = Mass(PiperArcherIII_Dict, 340, 0, 0, 0)
Motor = [21, 90/12*0.3048]
Inverter = [10, 90/12*0.3048]
BP = [[262., 91/12*0.3048]]
ECU = [86.5, 90/12*0.3048]
BMS = [39.89467616, 90/12*0.3048]
energyDensity = 265
energyDensity_ESS = energyDensity * 0.6238738739 # Wh/kg
MGTOWCase.electrify(*Motor, *Inverter, *ECU, *BMS, energyDensity_ESS, BP)


ElectricArcherAircraft = Aircraft(AircraftName, PiperArcherIII_Dict, 
                          Wings = ArcherWings, 
                          HorizontalStabilizer = ArcherHorizontalStabilizer, 
                          Fuselage = ArcherFuselage, 
                          VerticalStabilizer = ArcherVerticalStabilizer, 
                          Engine = ElectricArcherEngine,
                          Mass = MGTOWCase)







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
h_pMax = 1000
dist = 0

percent = 100

h_p = 500
vInfty = 80

useReserve = True
electric = True

if useReserve:
    reserveText = "reserves"
else:
    reserveText = "no-reserves"


filepath = "DataFiles\\range_trade_dump\\electric\\energy-density-{}Wh_kg\\{}\\".format(energyDensity, reserveText)

if not os.path.exists(filepath):
    os.makedirs(filepath)


#################################################################################
# These are tailored for the electric aircraft mission profile
vInfty_arr = np.array([70, 80, 90, 100, 110, 120, 130, 140]).astype(float)
h_p_arr = np.arange(500, 2500, 1000).astype(float)
controlArcher = Control(ElectricArcherAircraft)
#################################################################################

for vInfty in vInfty_arr:
    # Iterate over a range of velocities
    for h_p in h_p_arr:
        # Iterate over a range of altitudes
        Range = 0
        percent = 100
        # h_p = 1500; vInfty = 70
        while np.abs(percent) > tol or percent < 0:
            # Needs to ensure that most of the fuel is being used
            # while constraining the percent to be greater than 0 %
            if Range < 0:
                Range = 0
            print("\nTesting for Range: {} nmi at h_p: {} ft and vInfty: {} knots".format(Range, h_p, vInfty))
            data, bool = controlArcher.Range_Mission(Range, h_p, vInfty)
            ElectricArcherAircraft.reset("Else")
            percent = data["percent"]
            if Range == 0 and percent < 0:
                break
            if np.abs(percent) < tol and percent < 0:
                Range -= tol*0.9
            else:
                Range += percent

        filename = "vInfty-{}_h_p-{}.pickle".format(vInfty,h_p,data["range [nmi]"])
        with open(filepath+filename, "wb") as file:
            pickle.dump(data, file)