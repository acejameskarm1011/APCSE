import os
import sys
current_dir = os.getcwd()
main_dir = current_dir[:-8]
# excel_dir = main_dir + "\\ExcelFiles"
sys.path.insert(0, current_dir)

from Save_to_Excel import Save_to_Excel
import numpy as np



TakeOff = {
    "Velocity [knots]" : np.arange(0, 67),
    "Altitude [ft]" : np.zeros(len(np.arange(0, 67)))
}

Climb = {
    "Velocity [knots]" : np.ones(20)*76,
    "Altitude [ft]" : np.linspace(0,700,20)
}

Phases = {
    "Take-Off" : TakeOff,
    "Climb" : Climb
}


print(current_dir)
# os.chdir(main_dir)

Save_to_Excel(Phases)
# os.chdir(current_dir)