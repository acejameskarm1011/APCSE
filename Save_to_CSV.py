import numpy as np
import pandas as pd
import time
import os

current_directory = os.getcwd()
year, month, day, *excer = time.localtime()
if day < 10:
    day = "0" + str(day)
if month < 10:
    month = "0" + str(month)

filepath = current_directory + "\\DataFiles\\" + "{}_{}_{}\\".format(month,day,year)
if not os.path.exists(filepath):
    os.makedirs(filepath)

def Save_to_CSV(*Phases, missionType = "Conventional"):
    """
    This function takes multiple phases of flight, sorts the data, and then exports the aircraft and flight data into a csv.
    """
    for Phase in Phases:
        PhaseName = str(Phase)
        Phase = Phase.__dict__()
        df = pd.DataFrame(Phase)

        PhaseString = filepath + PhaseName + missionType + ".csv"

        df.to_csv(PhaseString)
    return None





