import numpy as np



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
wingDihedral = 3/180*np.pi

Sweep = 0
Sweep_LE = np.arctan(np.tan(Sweep) + (1-taper)/(AR*(1+taper)))
x_locWing = 0.0

# S_Canard = 82
# x_loc_Canard = 11.1 #ft
# AR_Canard = 3
# b_Canard = np.sqrt(S_Canard*AR_Canard)
# taper_Canard = 0.25
# Sweep = 45/180*np.pi
# Sweep_LE = np.arctan(np.tan(Sweep) + (1-taper_Canard)/(AR_Canard*(1+taper_Canard)))
# C_r_Canard = 2*S_Canard/b_Canard/(1+taper_Canard)
# C_t_Canard = C_r_Canard*taper
# dihedral_Canard = 5/180*np.pi
# MAC_Canard = 2/3*C_r_Canard*(1+taper_Canard+taper_Canard**2)/(1+taper_Canard)
# YBar_Canard = b_Canard/6*((1+2*taper_Canard)/(1+taper_Canard))


# S_VT = 65
# x_loc_VT = 32.98 #ft
# AR_VT = 1.3
# b_VT = np.sqrt(S_VT*AR_VT)
# taper_VT = 0.35
# Sweep = 25/180*np.pi
# Sweep_LE = np.arctan(np.tan(Sweep) + (1-taper_VT)/(AR_VT*(1+taper_VT)))
# C_r_VT = 2*S_VT/b_VT/(1+taper_VT)
# C_t_VT = C_r_VT*taper
# dihedral_VT = 60/180*np.pi
# MAC_VT = 2/3*C_r_VT*(1+taper_VT+taper_VT**2)/(1+taper_VT)
# YBar_VT = b_VT/6*((1+2*taper_VT)/(1+taper_VT))



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


# Example usage:
file_path = "PA_28_181.avl" # Replace with your .avl file path



Mach = 0.0
GroundEffect = False

h = 0

# write_specific_line_avl(file_path, 0.0, str(Mach)) # Edits the Mach number
if GroundEffect:
    write_specific_line_avl(file_path, 7, "0\t1\t0.0")
else:
    write_specific_line_avl(file_path, 7, "0\t0\t0.0")
write_specific_line_avl(file_path, 10, "{}\t {}\t {}".format(S_ref, MAC, span)) # Reference Vals
write_specific_line_avl(file_path, 14, "{}\t {}\t {}".format(MAC/4, 0, 0)) # Reference Vals
write_specific_line_avl(file_path, 34, "{}\t {}\t {}\t {}\t {}\t {}\t {}".format(float(x_locWing), 0., 0.+h, delta_c+c_root, 0, 20, 0))
write_specific_line_avl(file_path, 37, "NACA_65-415.dat")
write_specific_line_avl(file_path, 42, "{}\t {}\t {}\t {}\t {}\t {}\t {}".format(float(x_locWing), l_1, l_1*np.sin(wingDihedral)+h, delta_c+c_root, 0, 20, 0))
write_specific_line_avl(file_path, 45, "NACA_65-415.dat")
write_specific_line_avl(file_path, 50, "{}\t {}\t {}\t {}\t {}\t {}\t {}".format(float(x_locWing)+delta_c, l_2, l_2*np.sin(wingDihedral)+h, c_root, 0, 20, 0))
write_specific_line_avl(file_path, 53, "NACA_65-415.dat")
write_specific_line_avl(file_path, 58, "{}\t {}\t {}\t {}\t {}\t {}\t {}".format(float(x_locWing)+delta_c, l_3, l_3*np.sin(wingDihedral)+h, c_root, 0, 20, 0))
write_specific_line_avl(file_path, 61, "NACA_65-415.dat")
write_specific_line_avl(file_path, 65, "{}\t {}\t {}\t {}\t {}\t {}\t {}".format(float(x_locWing)+delta_c + chordOnlyLength*np.tan(Sweep_LE), span/2, span/2*np.sin(wingDihedral)+h, c_tip, 0, 20, 0))
write_specific_line_avl(file_path, 68, "NACA_65-415.dat")
 


# show_avl_file(file_path)