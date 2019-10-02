import subprocess

def create_script(cmd, script_name):
    with open(script_name, "w") as f:
        f.write("#/bin/sh\n\n")
        f.write("# This script is auto-generated and may be overwritten\n")
        f.write("# by the script_gen python script\n")
        f.write("# It is intended to be run within a docker container\n")
        f.write("# generated as mentioned in the elektra docker scripts\n\n")
        f.write(cmd)

def execute(cmd):
    popen = subprocess.Popen(cmd, stdout = subprocess.PIPE, universal_newlines = True)
    for line in iter(popen.stdout.readline, ""):
        print(line, end = "")
    popen.stdout.close()
    ret_code = popen.wait()
    return ret_code
