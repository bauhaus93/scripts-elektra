#!/bin/python3

import os
import sys
import subprocess
import argparse

ELEKTRA_PREFIX = "libelektra"
BUILD_PREFIX = "build"
INSTALL_PREFIX = "system"
BUILD_CONTAINER_PREFIX = "build_container"
IMAGE_NAME = "buildelektra-stretch-full"
LOCAL_ROOT = os.path.abspath(".")
CONTAINER_ROOT = os.path.join("/", "home", "jenkins", "workspace")

def build_cmake_cmd(elektra_path, install_path, kdb_config_path, build_doc, plugins, tools, bindings):
    kdb_system_path = os.path.join(kdb_config_path, "system")
    kdb_spec_path = os.path.join(kdb_config_path, "spec")
    kdb_home_path = os.path.join(kdb_config_path, "home")

    cmd = f'cmake {elektra_path} \\\n\t-DCMAKE_INSTALL_PREFIX="{install_path}"'
    cmd += f' \\\n\t-DKDB_DB_SYSTEM="{kdb_system_path}"'
    cmd += f' \\\n\t-DKDB_DB_SPEC="{kdb_spec_path}"'
    cmd += f' \\\n\t-DKDB_DB_HOME="{kdb_home_path}"'
    cmd += " \\\n\t-DBUILD_STATIC=ON -DBUILD_COVERAGE=ON"

    if build_doc:
        cmd += f" \\\n\t-DBUILD_DOCUMENTATION=ON"
    else:
        cmd += f" \\\n\t-DBUILD_DOCUMENTATION=OFF"

    if plugins:
        cmd += f" \\\n\t-DPLUGINS=\"{plugins}\""
    if tools:
        cmd += f" \\\n\t-DTOOLS=\"{tools}\""
    if bindings:
        cmd += f" \\\n\t-DBINDINGS=\"{bindings}\""
    return cmd

def build_make_cmd(jobs = 8):
    cmd = f"make -j{jobs} install"
    return cmd

def build_test_cmd(jobs = 8):
    cmd = f"ctest -j {jobs} --force-new-ctest-process --output-on-failure --no-compress-output"
    cmd += "\\\n\t-T Test -E \"testmod_(crypto_(botan|openssl)|dbus(recv)?|fcrypt|gpgme|zeromqsend)\""
    return cmd

def build_command(root_dir, run_tests, clean_build, build_doc, plugins, tools, bindings, jobs):
    elektra_path = os.path.join(root_dir, ELEKTRA_PREFIX)
    build_path = os.path.join(root_dir, BUILD_PREFIX)
    install_path = os.path.join(root_dir, INSTALL_PREFIX)
    kdb_config_path = os.path.join(root_dir, "config", "kdb")

    clean_cmd = f"rm -rf {install_path}"
    if clean_build:
        clean_cmd += f" {build_path}"

    setup_cmd = f"{clean_cmd} && \\\nmkdir -p {build_path} {install_path} && \\\ncd {build_path}"
    cmake_cmd = build_cmake_cmd(elektra_path, install_path, kdb_config_path, build_doc, plugins, tools, bindings)
    make_cmd = build_make_cmd(8)

    cmd = f"{setup_cmd} && \\\n{cmake_cmd} && \\\n{make_cmd}"

    if run_tests:
        test_cmd = build_test_cmd(16)
        cmd += f" && \\\n{test_cmd}"

    return cmd

def build_command_default(root_dir, run_tests = False, clean_build = False):
    return build_command(root_dir, run_tests, clean_build, False, None, None, None, 8)

def build_command_all(root_dir, run_tests = False, clean_build = False):
    return build_command(root_dir, run_tests, clean_build, True, "ALL", "ALL", "ALL", 8)

def create_script_command(cmd, script_name):
    with open(script_name, "w") as f:
        f.write("#/bin/sh\n")
        f.write("# This script is auto-generated anc may be overwritten\n\n")
        f.write(cmd)

def container_build_git_clone_cmd(user_name, repository):
    cmd = f"git clone https://github.com/{user_name}/{repository}.git"
    return cmd

def container_build_docker_cmd(image_name):
    cmd = f"docker build -t {image_name} \\\n"
    cmd += "--build-arg JENKINS_USERID=`id -u` \\\n"
    cmd += "--build-arg JENKINS_GROUPID=`id -g` \\\n"
    cmd += "-f scripts/docker/debian/stretch/Dockerfile \\\n"
    cmd += "scripts/docker/debian/stretch/"
    return cmd

def container_build_command(root_dir, git_name, git_repository, image_name):
    build_path = os.path.abspath(os.path.join(root_dir, BUILD_CONTAINER_PREFIX))
    elektra_path = os.path.abspath(os.path.join(root_dir, git_repository))

    setup_cmd = f"rm -rf {build_path} && mkdir -p {build_path} && cd {build_path}"
    git_clone_cmd = container_build_git_clone_cmd(git_name, git_repository)
    docker_cmd = container_build_docker_cmd(image_name)

    cmd = f"{setup_cmd} && {git_clone_cmd} && {docker_cmd}"

    return cmd

def container_build_command_default(root_dir):
    return container_build_command(root_dir, "ElektraInitiative", "libelektra", "buildelektra-stretch-full")

def execute_command(cmd):
    popen = subprocess.Popen(cmd, stdout = subprocess.PIPE, universal_newlines = True)
    for line in iter(popen.stdout.readline, ""):
        print(line, end = "")
    popen.stdout.close()
    ret_code = popen.wait()
    return ret_code

parser = argparse.ArgumentParser(description='Build/Test libelektra configurations')

parser.add_argument("--build-type", metavar="type_str", type=str, default = "default", choices = ["all", "default", "lcdproc"], help="Type of build")
parser.add_argument("--run-tests", action = "store_true", help = "Check if want to run tests after build")

parser.add_argument("--build-base-image", action = "store_true", help = "Check if want to rebuild base docker image")
parser.add_argument("--clean-build", action = "store_true", help = "Check if want to clean build directory before build")

args = parser.parse_args()

if __name__ == "__main__":

    if args.build_base_image:
        cmd = container_build_command_default(CURR_DIR)
        script_path = os.path.join(LOCAL_ROOT, "rebuild_container.sh")
    else:
        elektra_dir = os.path.join(os.path.abspath("."), "libelektra")
        if not (os.path.isdir(elektra_dir) and os.path.exists(elektra_dir)):
            print(f"Script must be executed in directory which contains libelektra dir, but '{elektra_dir}' not existing")
            exit(1)
        script_path = os.path.join(LOCAL_ROOT, "build.sh")
        if args.build_type == "all":
            cmd = build_command_all(CONTAINER_ROOT, args.run_tests, args.clean_build)
        elif args.build_type == "lcdproc":
            cmd = build_command_default(CONTAINER_ROOT, args.run_tests, args.clean_build)
        else:
            cmd = build_command_default(CONTAINER_ROOT, args.run_tests, args.clean_build)
    create_script_command(cmd, script_path)
