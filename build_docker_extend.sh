#!/bin/sh

docker build -t buildelektra-extended \
    -f docker/default/Dockerfile \
    docker/default
