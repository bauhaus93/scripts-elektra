#!/bin/sh

docker build -t buildelektra-with-sudo \
    -f docker/sudo/Dockerfile \
    docker/sudo
