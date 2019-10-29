#!/bin/sh

DOCKER_IMAGE="buildelektra-stretch-full"
BUILD_DIR_NAME="build_jenkins"
JENKINS_WORKSPACE_DIR="/home/jenkins/workspace"
JENKINS_ELEKTRA_DIR="$JENKINS_WORKSPACE_DIR/libelektra"
JENKINS_BUILD_DIR="$JENKINS_WORKSPACE_DIR/$BUILD_DIR_NAME"
DB_SYSTEM_DIR="$JENKINS_BUILD_DIR/config/kdb/system"
DB_SPEC_DIR="$JENKINS_BUILD_DIR/config/kdb/spec"
DB_HOME_DIR="$JENKINS_BUILD_DIR/config/kdb/home"

PLUGINS="MAINTAINED"
TOOLS="MAINTAINED"
BINDINGS="MAINTAINED"

BUILD_JOBS=8
TEST_JOBS=16

INCLUDE_TESTS=""
EXCLUDE_TESTS="testmod_(crypto_(botan|openssl)|dbus(recv)?|fcrypt|gpgme|zeromqsend)"

export DOCKER_IMAGE
export BUILD_DIR_NAME
export JENKINS_WORKSPACE_DIR
export JENKINS_ELEKTRA_DIR
export JENKINS_BUILD_DIR
export DB_SYSTEM_DIR
export DB_SPEC_DIR
export DB_HOME_DIR
export PLUGINS
export TOOLS
export BINDINGS
export BUILD_JOBS
export TEST_JOBS
if [ ! -z $INCLUDE_TESTS ]
then
	export INCLUDE_TESTS
else
	export EXCLUDE_TESTS
fi
