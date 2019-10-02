#!/bin/sh

rm -rf build_image_tmp
mkdir build_image_tmp
cd build_image_tmp && \
    git clone https://github.com/ElektraInitiative/libelektra.git && \
    cd libelektra && \
        docker build -t buildelektra-stretch-full \
        --build-arg JENKINS_USERID=`id -u` \
        --build-arg JENKINS_GROUPID=`id -g` \
        -f scripts/docker/debian/stretch/Dockerfile \
        scripts/docker/debian/stretch/
