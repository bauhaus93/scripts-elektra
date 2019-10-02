import os
import tempfile

from glob import BUILD_CONTAINER_PREFIX, ELEKTRA_PREFIX
from git import generate_git_clone

def generate_container(build_type):
    return generate_container_build("ElektraInitiative", "libelektra", build_type, "buildelektra-stretch-full")

def generate_container_build(git_name, git_repository, script_path, image_name):
    build_path = os.path.join(tempfile.gettempdir(), "build_elektra_container")
    full_script_path = os.path.join("scripts", "docker", script_path)

    setup_cmd = f"rm -rf {build_path} && mkdir -p {build_path} && cd {build_path}"
    git_clone_cmd = generate_git_clone(git_name, git_repository)
    docker_cmd = generate_build_cmd(image_name, full_script_path)

    cmd = f"{setup_cmd} && {git_clone_cmd} && cd {ELEKTRA_PREFIX} && {docker_cmd}"

    return cmd

def generate_build_cmd(image_name, script_path):
    dockerfile_path = os.path.join(script_path, "Dockerfile")
    cmd = f"docker build -t {image_name} \\\n"
    cmd += "--build-arg JENKINS_USERID=`id -u` \\\n"
    cmd += "--build-arg JENKINS_GROUPID=`id -g` \\\n"
    cmd += f"-f {dockerfile_path} \\\n"
    cmd += f"{script_path}"
    return cmd
