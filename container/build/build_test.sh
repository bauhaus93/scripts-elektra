#!/bin/sh

cd $JENKINS_BUILD_DIR && \
cmake $JENKINS_ELEKTRA_DIR \
	-DCMAKE_BUILD_TYPE=Debug \
	-DENABLE_DEBUG=ON \
	-DENABLE_TESTING=ON \
	-DBUILD_TESTING=ON \
	-DBUILD_DOCUMENTATION=OFF \
	-DPLUGINS="\"$PLUGINS\"" \
	-DTOOLS="\"$TOOLS\"" \
	-DBINDINGS="\"$BINDINGS\"" \
	-DKDB_DB_SYSTEM=$DB_SYSTEM_DIR \
	-DKDB_DB_SPEC=$DB_SPEC_DIR \
	-DKDB_DB_HOME=$DB_HOME_DIR && \
make -j $BUILD_JOBS && \
ctest	-j $TEST_JOBS \
	--force-new-ctest-process \
	--output-on-failure \
	--no-compress-output \
	-T Test \
	$([ ! -z INCLUDE_TESTS ] \
		&& echo "-R $INCLUDE_TESTS" \
		|| echo "-E $EXCLUDE_TESTS") \
