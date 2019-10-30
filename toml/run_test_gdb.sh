#!/bin/sh

[ ${PWD##*/} == "build" ] && \
gdb --args \
ctest	-R toml \
	--output-on-failure
	
