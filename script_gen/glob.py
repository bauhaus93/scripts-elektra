import os

ELEKTRA_PREFIX = "libelektra"
BUILD_PREFIX = "build"
INSTALL_PREFIX = "system"
BUILD_CONTAINER_PREFIX = "build_container"
IMAGE_NAME = "buildelektra-stretch-full"
LOCAL_ROOT = os.path.abspath(".")
CONTAINER_ROOT = os.path.join("/", "home", "jenkins", "workspace")
