#!/bin/sh

IMAGE_NAME="buildelektra-stretch-full"

../scripts/script_gen/script_gen.py $@

[[ -f $PWD/build.sh ]] && \
    chmod +x $PWD/build.sh && \
    docker run -it --rm \
        -v "$PWD:/home/jenkins/workspace" \
        -w /home/jenkins/workspace \
        $IMAGE_NAME \
        sh /home/jenkins/workspace/build.sh

