import os

from glob import BUILD_CONTAINER_PREFIX
from git import generate_git_clone

def generate_container_build_default(root_dir):
    return generate_command(root_dir, "ElektraInitiative", "libelektra", "buildelektra-stretch-full")

def generate_container_build(root_dir, git_name, git_repository, image_name):
    build_path = os.path.abspath(os.path.join(root_dir, BUILD_CONTAINER_PREFIX))
    elektra_path = os.path.abspath(os.path.join(root_dir, git_repository))

    setup_cmd = f"rm -rf {build_path} && mkdir -p {build_path} && cd {build_path}"
    git_clone_cmd = generate_git_clone(git_name, git_repository)
    docker_cmd = generate_build_cmd(image_name)

    cmd = f"{setup_cmd} && {git_clone_cmd} && {docker_cmd}"

    return cmd


def generate_build_cmd(image_name):
    cmd = f"docker build -t {image_name} \\\n"
    cmd += "--build-arg JENKINS_USERID=`id -u` \\\n"
    cmd += "--build-arg JENKINS_GROUPID=`id -g` \\\n"
    cmd += "-f scripts/docker/debian/stretch/Dockerfile \\\n"
    cmd += "scripts/docker/debian/stretch/"
    return cmd
