#!/bin/sh

docker build -t buildelektra-toml \
    -f docker/toml/Dockerfile \
    docker/toml
