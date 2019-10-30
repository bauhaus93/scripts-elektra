#!/bin/sh
echo "### Runing valgrind ###"
[ ${PWD##*/} == "build" ] && \
[ -f bin/testmod_toml ] && \
valgrind 	-s \
		--leak-check=full \
		--leak-resolution=low \
		--track-origins=yes \
		--trace-children=yes \
		bin/testmod_toml
