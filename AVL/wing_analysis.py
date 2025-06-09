import os
cwd = os.getcwd()


avl_path = "avl.exe"

if cwd[-6:] == "\\APCSE":
    avl_dir = cwd + "\\AVL"
    os.chdir(avl_dir)

import numpy as np
import re
import subprocess
from scipy.interpolate import make_smoothing_spline
import matplotlib.pyplot as plt
import pandas as pd
import scipy as sp
from matplotlib.gridspec import GridSpec
import scienceplots

C_L_0, C_L_alpha, spaneff = 0.5303683475274001, 0.10037131779018216, 0.8749882376705862

import time
year, month, day, *excer = time.localtime()
if day < 10:
    day = "0" + str(day)
if month < 10:
    month = "0" + str(month)

plt.style.use(["science","grid"])
textsize = 18
plt.rcParams.update({'font.size': textsize})

date = "{}_{}_{}".format(month,day,year)




span = 35.5                # ft
c_tip = 3+6.2/12           # ft
c_root = 5.25              # ft
delta_c = 0.9596           # ft
l_1 = 3.7906/2             # ft
chordOnlyLength = 9.0447
l_3 = span/2 - chordOnlyLength  # ft
l_2 = l_1 + 2.4631   # ft


S_ref = 2*(l_1*(c_root+delta_c) + 1/2*(l_2-l_2)*(2*c_root+delta_c) + (l_3-l_2)*(c_root) + 1/2*(span/2-l_3)*(c_root+c_tip))

AR = span**2/S_ref

taper = c_tip/c_root
MAC = 2/3*c_root*(1+taper+taper**2)/(1+taper)
wingDihedral = 7/180*np.pi

Sweep = 0
Sweep_LE = np.arctan(np.tan(Sweep) + (1-taper)/(AR*(1+taper)))
x_locWing = 0.0


def show_avl_file(filepath):
    """
    Opens an .avl file, allows for editing, and saves the changes.

    Args:
        filepath (str): The path to the .avl file.
    """
    try:
        with open(filepath, 'r+') as file:  # Open for reading and writing ('r+')
            lines = file.readlines()

            # Display the current content (optional, but helpful for editing)
            print("Current content:")
            for i, line in enumerate(lines):
                print(f"{i + 1}: {line.strip()}") #Display line number and content
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def write_specific_line_avl(filepath, line_number, new_content):
    """
    Writes new content to a specific line in an .avl file.

    Args:
        filepath (str): The path to the .avl file.
        line_number (int): The line number (1-based index) to write to.
        new_content (str): The new content to write to the specified line.
    """
    try:
        with open(filepath, 'r+') as file:
            lines = file.readlines()

            if 1 <= line_number <= len(lines):
                lines[line_number - 1] = new_content + "\n"  # Replace the line, add newline
                file.seek(0)
                file.writelines(lines)
                file.truncate()
                # print(f"Line {line_number} updated successfully.")
            else:
                print(f"Error: Line number {line_number} is out of range.")
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")


def extract_aero_coeffs(avl_output: str):
    # Dictionary to hold extracted values
    coeffs = {}

    # Patterns to search for (can expand this list!)
    patterns = {
        'CLtot': r'CLtot\s*=\s*([-+]?\d*\.\d+|\d+)',
        'CDtot': r'CDtot\s*=\s*([-+]?\d*\.\d+|\d+)',
        'CDi': r'CDff\s*=\s*([-+]?\d*\.\d+|\d+)',
        'CYtot': r'CYtot\s*=\s*([-+]?\d*\.\d+|\d+)',
        'Cmtot': r'Cmtot\s*=\s*([-+]?\d*\.\d+|\d+)',
        'CXtot': r'CXtot\s*=\s*([-+]?\d*\.\d+|\d+)',
        'CZtot': r'CZtot\s*=\s*([-+]?\d*\.\d+|\d+)',
        'e':     r'e\s*=\s*([-+]?\d*\.\d+|\d+)'  # Oswald efficiency
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, avl_output)
        if match:
            coeffs[key] = float(match.group(1))
        else:
            coeffs[key] = None  # Optional: None if not found

    return coeffs
def run_avl(avl_path, avl_file, alpha=5):
    # Create the sequence of commands
    cmds = f"""
    LOAD {avl_file}
    OPER
    a
    a
    {alpha}
    x
    """
    # Launch AVL
    process = subprocess.Popen([avl_path],
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               universal_newlines=True)

    stdout, stderr = process.communicate(input=cmds)

    # Show output
    return stdout


# Example usage:
file_path = "PA_28_181.avl" # Replace with your .avl file path


Mach = 0.0

h = 0

z_wingInstalled = 2.1352

h_p_arr = np.linspace(0,100, 20) + z_wingInstalled
write_specific_line_avl(file_path, 10, "{}\t {}\t {}".format(S_ref, MAC, span)) # Reference Vals
write_specific_line_avl(file_path, 14, "{}\t {}\t {}".format(MAC/4, 0, 0)) # Reference Vals
write_specific_line_avl(file_path, 37, "NACA_65-415.dat")
write_specific_line_avl(file_path, 45, "NACA_65-415.dat")
write_specific_line_avl(file_path, 53, "NACA_65-415.dat")
write_specific_line_avl(file_path, 61, "NACA_65-415.dat")
write_specific_line_avl(file_path, 68, "NACA_65-415.dat")

# write_specific_line_avl(file_path, 0.0, str(Mach)) # Edits the Mach number
write_specific_line_avl(file_path, 7, "0\t1\t0.0")




text = run_avl(avl_path, file_path, 0)

# print(text)

# coeffs = {}

# # Patterns to search for (can expand this list!)
# patterns = {
#     'CLtot': r'CLtot\s*=\s*([-+]?\d*\.\d+|\d+)',
#     'CDtot': r'CDtot\s*=\s*([-+]?\d*\.\d+|\d+)',
#     'CDi': r'CDff\s*=\s*([-+]?\d*\.\d+|\d+)',
#     'CYtot': r'CYtot\s*=\s*([-+]?\d*\.\d+|\d+)',
#     'Cmtot': r'Cmtot\s*=\s*([-+]?\d*\.\d+|\d+)',
#     'CXtot': r'CXtot\s*=\s*([-+]?\d*\.\d+|\d+)',
#     'CZtot': r'CZtot\s*=\s*([-+]?\d*\.\d+|\d+)',
#     'e':     r'e\s*=\s*([-+]?\d*\.\d+|\d+)'  # Oswald efficiency
# }

# for key, pattern in patterns.items():
#     match = re.search(pattern, text)
#     if match:
#         coeffs[key] = float(match.group(1))
#     else:
#         coeffs[key] = None  # Optional: None if not found


# print(coeffs["CDi"])
# exit()


angleOfAttack_arr = np.arange(-12,12,1)
CL_tot_dict = {}
CD_tot_dict = {}

t_0 = time.time()

runGroundEffect = False
if runGroundEffect:
    for h in h_p_arr:
        CL_tot_list = [h]
        CD_tot_list = [h]
        if h == h_p_arr[-1]:
            write_specific_line_avl(file_path, 7, "0\t0\t0.0") # Gets limit of ground effect
        write_specific_line_avl(file_path, 34, "{}\t {}\t {}\t {}\t {}\t {}\t {}".format(float(x_locWing), 0., h, delta_c+c_root, 0, 20, 0))
        write_specific_line_avl(file_path, 42, "{}\t {}\t {}\t {}\t {}\t {}\t {}".format(float(x_locWing), l_1, l_1*np.sin(wingDihedral)+h, delta_c+c_root, 0, 20, 0))
        write_specific_line_avl(file_path, 50, "{}\t {}\t {}\t {}\t {}\t {}\t {}".format(float(x_locWing)+delta_c, l_2, l_2*np.sin(wingDihedral)+h, c_root, 0, 20, 0))
        write_specific_line_avl(file_path, 58, "{}\t {}\t {}\t {}\t {}\t {}\t {}".format(float(x_locWing)+delta_c, l_3, l_3*np.sin(wingDihedral)+h, c_root, 0, 20, 0))
        write_specific_line_avl(file_path, 65, "{}\t {}\t {}\t {}\t {}\t {}\t {}".format(float(x_locWing)+delta_c + chordOnlyLength*np.tan(Sweep_LE), span/2, span/2*np.sin(wingDihedral)+h, c_tip, 0, 20, 0))
        for AOA in angleOfAttack_arr:
            text = run_avl(avl_path, file_path, AOA)
            results = extract_aero_coeffs(text)
            # if AOA == 0:
            #     C_L_0_avl = results["CLtot"]
            CL_tot_list.append(results["CLtot"])
            CD_tot_list.append(results["CDi"])
        CL_tot_arr = np.array(CL_tot_list)
        CD_tot_arr = np.array(CD_tot_list)
        CL_tot_dict["h_p: {} ft".format(round(h,3))] = CL_tot_arr

        CD_tot_dict["h_p: {} ft".format(round(h,3))] = CD_tot_arr

    t_1 = time.time()
    print(t_1-t_0)

    df = pd.DataFrame(CL_tot_dict)
    df.to_csv("C_L_AVL.csv")

    df = pd.DataFrame(CD_tot_dict)
    df.to_csv("C_D_AVL.csv")


# exit()






# If AVL is in your path, this runs it and loads the file

CL_tot_list = []
CD_tot_list = []
write_specific_line_avl(file_path, 7, "0\t0\t0.0") # Gets limit of ground effect
write_specific_line_avl(file_path, 34, "{}\t {}\t {}\t {}\t {}\t {}\t {}".format(float(x_locWing), 0., h, delta_c+c_root, 0, 20, 0))
write_specific_line_avl(file_path, 42, "{}\t {}\t {}\t {}\t {}\t {}\t {}".format(float(x_locWing), l_1, l_1*np.sin(wingDihedral)+h, delta_c+c_root, 0, 20, 0))
write_specific_line_avl(file_path, 50, "{}\t {}\t {}\t {}\t {}\t {}\t {}".format(float(x_locWing)+delta_c, l_2, l_2*np.sin(wingDihedral)+h, c_root, 0, 20, 0))
write_specific_line_avl(file_path, 58, "{}\t {}\t {}\t {}\t {}\t {}\t {}".format(float(x_locWing)+delta_c, l_3, l_3*np.sin(wingDihedral)+h, c_root, 0, 20, 0))
write_specific_line_avl(file_path, 65, "{}\t {}\t {}\t {}\t {}\t {}\t {}".format(float(x_locWing)+delta_c + chordOnlyLength*np.tan(Sweep_LE), span/2, span/2*np.sin(wingDihedral)+h, c_tip, 0, 20, 0))
for AOA in angleOfAttack_arr:
    text = run_avl(avl_path, file_path, AOA)
    results = extract_aero_coeffs(text)
    if AOA == 0:
        C_L_0_avl = results["CLtot"]
    CL_tot_list.append(results["CLtot"])
    CD_tot_list.append(results["CDi"])
CL_tot_arr = np.array(CL_tot_list)
CD_tot_arr = np.array(CD_tot_list)

plotting = False
if plotting:
    fig, ax = plt.subplots(1,2,figsize=(12,7), constrained_layout = True)
    ax[0].plot(angleOfAttack_arr, CL_tot_arr, "r.", label = "AVL")
    ax[0].set_xlabel("AOA")
    ax[0].set_ylabel("$C_L$")
    ax[0].plot(angleOfAttack_arr, C_L_0 + angleOfAttack_arr*C_L_alpha, "b.", label = "LLT")
    ax[0].set_xlabel("AOA")
    ax[0].set_ylabel("$C_L$")
    ax[0].legend()

    ax[1].plot(CD_tot_arr, CL_tot_arr, "r.", label = "AVL")
    ax[1].set_ylabel("$C_L$")
    ax[1].set_xlabel("$C_D$")
    ax[1].plot((C_L_0 + angleOfAttack_arr*C_L_alpha)**2/(np.pi*AR*spaneff), C_L_0 + angleOfAttack_arr*C_L_alpha, "b.", label = "LLT")
    ax[1].set_ylabel("$C_L$")
    ax[1].set_xlabel("$C_D$")
    ax[1].legend()
    plt.savefig("AVL_vs_LLT_comparison.png")
    plt.show()
    C_L_0 = C_L_0_avl
    C_L_alpha = np.mean(CL_tot_arr[1:] - CL_tot_arr[:-1])
os.chdir(cwd)