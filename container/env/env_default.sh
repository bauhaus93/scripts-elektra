#!/bin/sh

DOCKER_IMAGE="buildelektra-with-sudo"
BUILD_DIR_NAME="build-jenkins"
JENKINS_WORKSPACE_DIR="/home/jenkins/workspace"
JENKINS_ELEKTRA_DIR="$JENKINS_WORKSPACE_DIR/libelektra"
JENKINS_BUILD_DIR="$JENKINS_WORKSPACE_DIR/$BUILD_DIR_NAME"
DB_SYSTEM_DIR="$JENKINS_BUILD_DIR/config/kdb/system"
DB_SPEC_DIR="$JENKINS_BUILD_DIR/config/kdb/spec"
DB_HOME_DIR="$JENKINS_BUILD_DIR/config/kdb/home"

PLUGINS="MAINTAINED"
TOOLS="ALL"
BINDINGS="ALL"

BUILD_JOBS=8
TEST_JOBS=16

INCLUDE_TESTS=""
EXCLUDE_TESTS="testmod_(crypto_(botan|openssl)|dbus(recv)?|fcrypt|gpgme|zeromqsend)"

ENV_DEFINED=1
