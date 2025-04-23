"""import subprocess as subprocess

avl = subprocess.Popen(
    "avl",  # Replace with the actual path to your AVL executable
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,  # Optionally capture the output
    stderr=subprocess.PIPE,  # Optionally capture errors
    universal_newlines=True
)
commands = """"""
LOAD NT3.avl
OPER
A A 0
X
FS
QUIT"""
"""
output, errors = avl.communicate(commands)

print(output)
if errors:
    print(errors)
"""
import subprocess
import os

def extract_cl_from_avl(avl_filepath, alpha):
    """
    Runs AVL, extracts C_L for a given alpha, and returns it.
    """
    try:
        avl_executable = avl_filepath #<-- Replace with your actual path.
        avl = subprocess.Popen(
            [avl_executable],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )

        avl_commands = [
            "load {}".format("NT3.avl"),
            "oper",
            f"a a {alpha}",
            "x",
            "ft",
            "",
            "quit",
        ]
        input_str = "\n".join(avl_commands) + "\n"

        print("Sending to AVL:\n", input_str) #debug.
        avl.stdin.write(input_str) #Explicit write.
        avl.stdin.flush() #Explicit flush.
        stdout, stderr = avl.communicate()

        print("AVL stdout:\n", stdout) #debug.
        print("AVL stderr:\n", stderr) #debug.

        if avl.returncode != 0:
            print(f"AVL run failed. stderr: {stderr}")
            return None

        ft_filename = os.path.subprocesslitext(avl_filepath)[0] + ".ft"
        if os.path.exists(ft_filename):
            with open(ft_filename, "r") as ft_file:
                for line in ft_file:
                    if "CL =" in line:
                        cl = float(line.subprocesslit("=")[1].strip())
                        os.remove(ft_filename)
                        return cl
            os.remove(ft_filename)
            return None
        else:
            print(f"ft file {ft_filename} was not created.")
            return None

    except FileNotFoundError:
        print("Error: AVL executable or file not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

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
avl_file = "NT3.avl" # Replace with your AVL file.
avl_path = "avl.exe"
AOA = 0

# out = run_avl(avl_path, avl_file, 0) #alpha of 5 degrees.
# print(out)