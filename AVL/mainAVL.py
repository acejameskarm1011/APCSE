import os
import subprocess
import matplotlib.pyplot as plt
import re

def write_avl_file(filename, aircraft_name, mach, ref_area, ref_chord, ref_span, x_ref, y_ref, z_ref, surfaces):
    with open(filename, "w") as f:
        f.write(f"{aircraft_name}\n")
        f.write(f"#Mach\n{mach:.3f}\n")
        f.write("#IYsym   IZsym   Zsym\n")
        f.write("0       0       0.0\n")
        f.write("#Sref    Cref    Bref\n")
        f.write(f"{ref_area:.2f}   {ref_chord:.2f}   {ref_span:.2f}\n")
        f.write("#Xref    Yref    Zref\n")
        f.write(f"{x_ref:.2f}     {y_ref:.2f}     {z_ref:.2f}\n")
        f.write("#\n#\n#====================================================================\n")
        
        for surf in surfaces:
            f.write("SURFACE\n")
            f.write(f"{surf['name']}\n")
            f.write("#Nchordwise  Cspace   Nspanwise   Sspace\n")
            f.write(f"{surf.get('Nchord',10)}    {surf.get('Cspace',1.0)}    {surf.get('Nspan',20)}    {surf.get('Sspace',1.0)}\n")
            f.write("#\nYDUPLICATE\n0.0\n")
            f.write("#\nANGLE\n0.0\n\n")
            
            for sec in surf['sections']:
                f.write("#-------------------------------------------------------------\n")
                f.write("SECTION\n")
                f.write(f"# Xle Yle Zle Chord Ainc Nspan Sspace\n")
                f.write(f"{sec['x']} {sec['y']} {sec['z']} {sec['chord']} {sec.get('a_inc', 0)} 0 0\n")
                f.write("AFILE\n")
                f.write(f"{sec['airfoil']}\n")

def plot_plane_2d(surfaces):
    fig, ax = plt.subplots()

    for surf in surfaces:
        sections = surf['sections']
        leading_edges_x = [sec['x'] for sec in sections]
        leading_edges_y = [sec['y'] for sec in sections]

        trailing_edges_x = [sec['x'] + sec['chord'] for sec in sections]
        trailing_edges_y = [sec['y'] for sec in sections]

        # Draw outline of wing: leading edge -> trailing edge (reversed) -> close
        x_outline = leading_edges_x + trailing_edges_x[::-1] + [leading_edges_x[0]]
        y_outline = leading_edges_y + trailing_edges_y[::-1] + [leading_edges_y[0]]

        ax.fill(x_outline, y_outline, color='lightblue', edgecolor='black', alpha=0.7)
        ax.plot(x_outline, y_outline, 'k-')  # outline

    ax.set_aspect('equal')
    plt.xlabel("X (ft)")
    plt.ylabel("Y (ft)")
    plt.title("2D Top View of Wing")
    plt.grid()
    plt.show()



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

def extract_aero_coeffs(avl_output: str):
    # Dictionary to hold extracted values
    coeffs = {}

    # Patterns to search for (can expand this list!)
    patterns = {
        'CLtot': r'CLtot\s*=\s*([-+]?\d*\.\d+|\d+)',
        'CDtot': r'CDtot\s*=\s*([-+]?\d*\.\d+|\d+)',
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