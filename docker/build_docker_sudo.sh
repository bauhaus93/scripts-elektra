#!/bin/sh

# Expected to be run in the scripts directory

docker build -t buildelektra-with-sudo \
    -f docker/sudo/Dockerfile \
    docker/sudo
