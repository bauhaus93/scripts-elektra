#!/bin/sh

function print_or_exit {
	if [ -z $2 ]
	then
		echo "Unset variable: $1"
		exit 1
	else
		echo "$1: $2"
	fi
}

function print_or_silent {
	if [ ! -z $2 ]
	then
		echo "$1: $2"
	fi
}

echo "### Current build environment ###"

print_or_exit "DOCKER_IMAGE" $DOCKER_IMAGE
print_or_exit "JENKINS_BUILD_DIR" $JENKINS_BUILD_DIR
print_or_exit "JENKINS_ELEKTRA_DIR" $JENKINS_ELEKTRA_DIR
print_or_exit "PLUGINS" $PLUGINS
print_or_exit "TOOLS" $TOOLS
print_or_exit "BINDINGS" $BINDINGS
print_or_silent "INCLUDE_TESTS" $INCLUDE_TESTS
print_or_silent "EXCLUDE_TESTS" $EXCLUDE_TESTS
