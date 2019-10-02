#!/bin/python3

import argparse
import os

from glob import LOCAL_ROOT, CONTAINER_ROOT
from docker import generate_container_build_default
from build import generate_build_command_default, generate_build_command_all
from command import create_script

parser = argparse.ArgumentParser(description='Build/Test libelektra configurations')

parser.add_argument("--build-type", metavar="type_str", type=str, default = "default", choices = ["all", "default", "lcdproc"], help="Type of build")
parser.add_argument("--run-tests", action = "store_true", help = "Check if want to run tests after build")

parser.add_argument("--build-base-image", action = "store_true", help = "Check if want to rebuild base docker image")
parser.add_argument("--clean-build", action = "store_true", help = "Check if want to clean build directory before build")

args = parser.parse_args()

if __name__ == "__main__":

    if args.build_base_image:
        cmd = generate_container_build_default(LOCAL_ROOT)
        script_path = os.path.join(LOCAL_ROOT, "rebuild_container.sh")
    else:
        elektra_dir = os.path.join(os.path.abspath("."), "libelektra")
        if not (os.path.isdir(elektra_dir) and os.path.exists(elektra_dir)):
            print(f"Script must be executed in directory which contains libelektra dir, but '{elektra_dir}' not existing")
            exit(1)
        script_path = os.path.join(LOCAL_ROOT, "build.sh")
        if args.build_type == "all":
            cmd = generate_build_command_all(CONTAINER_ROOT, args.run_tests, args.clean_build)
        elif args.build_type == "lcdproc":
            print("Not Implemented!")
            exit(1)
        else:
            cmd = generate_build_command_default(CONTAINER_ROOT, args.run_tests, args.clean_build)
    create_script(cmd, script_path)
