#!/bin/python3

import argparse
import os

from glob import CONTAINER_ROOT, ELEKTRA_PREFIX, OUTPUT_PREFIX
from build import generate_build_command
from command import create_script

parser = argparse.ArgumentParser(description='Build/Test libelektra configurations')

parser.add_argument
parser.add_argument("--target", metavar="target_str", type = str, help = "Set build target", choices = ["all", "default", "lcdproc", "toml"], default = "default")
parser.add_argument("--build-type", metavar="type_str", type = str, default = "Debug", choices = ["Release", "Debug", "RelWithDebInfo"], help="Type of build")
parser.add_argument("--run-tests", action = "store_true", help = "Check if want to run tests after build")
parser.add_argument("--run-shell", action = "store_true", help = "Check if want to run a shell after build")
parser.add_argument("--clean-build", action = "store_true", help = "Check if want to clean build directory before build")

args = parser.parse_args()

if __name__ == "__main__":
    NATIVE_ROOT = os.path.abspath(".")
    SCRIPT_PATH = os.path.join(NATIVE_ROOT, OUTPUT_PREFIX, "build.sh")
    ELEKTRA_DIR = os.path.join(NATIVE_ROOT, ELEKTRA_PREFIX)

    if not (os.path.isdir(ELEKTRA_DIR) and os.path.exists(ELEKTRA_DIR)):
        print(f"Script must be executed in directory which contains libelektra dir, but '{ELEKTRA_DIR}' not existing")
        exit(1)
    cmd = generate_build_command(CONTAINER_ROOT, args.target, args.build_type, args.run_tests,  args.run_shell, args.clean_build)
    create_script(cmd, SCRIPT_PATH)
