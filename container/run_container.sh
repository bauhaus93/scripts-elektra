#!/bin/sh

SCRIPT_NAME="build_test.sh"
ENV_NAME="env_default.sh"

if [ ! -d libelektra ]
then
	echo "No libelektra folder found"
	exit 1
fi

SCRIPTS_DIR="../scripts"
SCRIPT_PATH="$SCRIPTS_DIR/container/build/$SCRIPT_NAME"
ENV_PATH="$SCRIPTS_DIR/container/env/$ENV_NAME"
ECHO_PATH="$SCRIPTS_DIR/container/env/env_echo.sh"

if [ ! -d $SCRIPTS_DIR ]
then
	echo "Scripts dir not found: $SCRIPTS_DIR"
	exit 1
fi

if [ ! -f $SCRIPT_PATH ]
then
	echo "Target script not found: $SCRIPT_PATH"
	exit 1
fi

if [ ! -f $ENV_PATH ]
then
	echo "Target environment not found: $ENV_PATH"
	exit 1
fi

if [ ! -f $ECHO_PATH ]
then
	echo "Echo file not found: $ECHO_PATH"
	exit 1
fi

if [ -z $ENV_DEFINED ]
then
	TMP_SCRIPT=$(mktemp --suffix=.sh -p /tmp starter_XXXXX) && \
	cat $ENV_PATH $ECHO_PATH $0 > $TMP_SCRIPT && \
	chmod +x $TMP_SCRIPT && \
	$TMP_SCRIPT
	exit $?
fi
LOCAL_BUILD_DIR="$PWD/$BUILD_DIR_NAME"

rm -rf $LOCAL_BUILD_DIR && \
mkdir -p $LOCAL_BUILD_DIR && \
cat $ENV_PATH $SCRIPT_PATH > $LOCAL_BUILD_DIR/run.sh && \
chmod +x $LOCAL_BUILD_DIR/run.sh && \
docker run -it --rm \
	-v "$PWD:/$JENKINS_WORKSPACE_DIR" \
        -w $JENKINS_WORKSPACE_DIR \
        $DOCKER_IMAGE \
        sh $JENKINS_BUILD_DIR/run.sh
rm $0
