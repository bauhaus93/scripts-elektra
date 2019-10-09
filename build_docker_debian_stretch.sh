#!/bin/sh
docker build -t buildelektra-stretch-full \                                                                                             
    --build-arg JENKINS_USERID=`id -u` \
    --build-arg JENKINS_GROUPID=`id -g` \
    -f scripts/docker/debian/stretch/Dockerfile \
    scripts/docker/debian/stretch/
