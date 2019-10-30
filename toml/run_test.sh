#!/bin/sh

echo "### Running ctest ###"
[ ${PWD##*/} == "build" ] && \
ctest	-R toml \
	--output-on-failure
	
