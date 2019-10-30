#!/bin/sh
[ -d "libelektra" ] && \
rm -rf build && \
mkdir build && \
cd build && \
cmake ../libelektra \
	-DPLUGINS="MAINTAINED;toml" \
	-DCMAKE_BUILD_TYPE=Debug \
	-DBUILD_TESTING=ON \
	-DENABLE_TESTING=ON \
	-DENABLE_DEBUG=ON && \
make -j8
