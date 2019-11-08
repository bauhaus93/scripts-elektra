#!/bin/sh

IMAGE_NAME="buildelektra-with-sudo"
LOCAL_WORKSPACE_DIR="$PWD"
LOCAL_ELEKTRA_BUILD_DIR="$LOCAL_WORKSPACE_DIR/build-jenkins"
LOCAL_LCDPROC_DIR="$PWD/lcdproc"
JENKINS_WORKSPACE_DIR="/home/jenkins/workspace"
JENKINS_ELEKTRA_DIR="$JENKINS_WORKSPACE_DIR/libelektra"
JENKINS_LCDPROC_DIR="$JENKINS_WORKSPACE_DIR/lcdproc"
JENKINS_ELEKTRA_BUILD_DIR="$JENKINS_WORKSPACE_DIR/build-jenkins"
PLUGINS="c;cache;dump;gopts;hexnumber;ini;list;mmapstorage;network;ni;noresolver;path;quickdump;range;reference;resolver;resolver_fm_hpu_b;spec;specload;type;validation;sync"

mkdir -p $LOCAL_ELEKTRA_BUILD_DIR
pushd $LOCAL_LCDPROC_DIR && make clean
popd

docker run -it --rm \
	-v "$LOCAL_WORKSPACE_DIR:$JENKINS_WORKSPACE_DIR" \
	$IMAGE_NAME \
	sh -c "cd $JENKINS_ELEKTRA_BUILD_DIR && \
		  cmake $JENKINS_ELEKTRA_DIR \
		  -DPLUGINS=\"$PLUGINS\" \
		  -DENABLE_DEBUG=ON \
		  -DCMAKE_BUILD_TYPE=Debug \
		  -DBUILD_TESTING=OFF \
		  -DENABLE_TESTING=OFF \
		  -DINSTALL_TESTING=OFF && \
		  make -j8 && \
		  sudo make install && \
		  sudo ldconfig && \
		  cd $JENKINS_LCDPROC_DIR && \
		  sh ./autogen.sh && \
		  ./configure && \
		  make && \
		  sudo make install && \
		  sudo ./post-install.sh && \
		  kdb set '/sw/lcdproc/lcdd/#0/current/server/drivers/#0' '@/curses/#0' && \
		  tmux"
