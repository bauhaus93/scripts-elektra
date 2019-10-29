#!/bin/sh

# Expected to be run from the scripts directory

docker build -t buildelektra-toml \
    -f docker/toml/Dockerfile \
    docker/toml
