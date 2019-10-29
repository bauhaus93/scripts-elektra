#!/bin/sh

rm -f leak.log

[ -f bin/testmod_toml ] && \
make -j8 && \
valgrind 	-s \
		--leak-check=full \
		--leak-resolution=low \
		--track-origins=yes \
		--trace-children=yes \
		--log-file=leak.log \
		bin/testmod_toml && \
vim leak.log
