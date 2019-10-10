#!/bin/sh

IMAGE_NAME="buildelektra-with-sudo"

mkdir -p $PWD/output
rm -f $PWD/output/build.sh

../scripts/script_gen/script_gen.py $@

[[ -f $PWD/output/build.sh ]] && \
    chmod +x $PWD/output/build.sh && \
    docker run -it --rm \
        -v "$PWD:/home/jenkins/workspace" \
        -w /home/jenkins/workspace \
        $IMAGE_NAME \
        sh /home/jenkins/workspace/output/build.sh

