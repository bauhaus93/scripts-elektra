#!/bin/python3

import argparse
import os

from glob import CONTAINER_ROOT, ELEKTRA_PREFIX, OUTPUT_PREFIX
from docker import generate_container
from build import generate_build_command_default, generate_build_command_all
from command import create_script

parser = argparse.ArgumentParser(description='Build/Test libelektra configurations')

parser.add_argument("--build-type", metavar="type_str", type=str, default = "default", choices = ["all", "default", "lcdproc"], help="Type of build")
parser.add_argument("--run-tests", action = "store_true", help = "Check if want to run tests after build")

parser.add_argument("--build-image", metavar="type_str", type = str, help = "Check if want to rebuild base docker image", choices = ["debian/stretch", "debian/sid", "debian/jessy"])
parser.add_argument("--clean-build", action = "store_true", help = "Check if want to clean build directory before build")

args = parser.parse_args()

if __name__ == "__main__":
    NATIVE_ROOT = os.path.abspath(".")
    SCRIPT_PATH = os.path.join(NATIVE_ROOT, OUTPUT_PREFIX, "build.sh")
    ELEKTRA_DIR = os.path.join(NATIVE_ROOT, ELEKTRA_PREFIX)

    if not args.build_image is None:
        cmd = generate_container(args.build_image)
    else:
        if not (os.path.isdir(ELEKTRA_DIR) and os.path.exists(ELEKTRA_DIR)):
            print(f"Script must be executed in directory which contains libelektra dir, but '{ELEKTRA_DIR}' not existing")
            exit(1)
        if args.build_type == "all":
            cmd = generate_build_command_all(CONTAINER_ROOT, args.run_tests, args.clean_build)
        elif args.build_type == "lcdproc":
            print("Not Implemented!")
            exit(1)
        else:
            cmd = generate_build_command_default(CONTAINER_ROOT, args.run_tests, args.clean_build)
    create_script(cmd, SCRIPT_PATH)
