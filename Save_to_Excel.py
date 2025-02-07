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



def Save_to_Excel(MissionType, *Phases):
    """
    This function takes multiple phases of flight, sorts the data, and then exports the aircraft and flight data into an excel spreadsheet.
    """

    filepath = current_directory + "\\ExcelFiles\\" + "{}_{}_{}\\".format(day,month,year)
    if not os.path.exists(filepath):
        os.makedirs(filepath)

    PhaseString = ""
    AllPhases = {}
    for Phase in Phases:
        PhaseName = str(Phase)
        Phase = Phase.__dict__()
        AllPhases[PhaseName] = Phase
        PhaseString = PhaseString + PhaseName + "_"
    totalstring = filepath + MissionType + ".xlsx"

    writer = pd.ExcelWriter(totalstring)
    for key0 in AllPhases:
        cols = []
        Phase = AllPhases[key0]

        for key1 in Phase:
            if isinstance(Phase[key1], (np.ndarray, list, tuple)):
                i = len(Phase[key1])
            cols.append(key1)

        rows = (np.arange(i) + 1).astype(str)
        datatot = pd.DataFrame(Phase, index = rows, columns=cols)
        datatot.to_excel(writer, sheet_name=key0)

    writer.close()
    return None