#!/bin/sh

docker run -it --rm \
    -v "$PWD:/home/jenkins/workspace" \
    -w /home/jenkins/workspace \
    elektra-reformat \
    ./scripts/dev/reformat-source
