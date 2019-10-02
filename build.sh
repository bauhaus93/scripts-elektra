#/bin/sh

# This script is auto-generated and may be overwritten
# by the script_gen python script
# It is intended to be run within a docker container
# generated as mentioned in the elektra docker scripts

rm -rf /tmp/build_elektra_container && mkdir -p /tmp/build_elektra_container && cd /tmp/build_elektra_container && git clone https://github.com/ElektraInitiative/libelektra.git && cd libelektra && docker build -t buildelektra-stretch-full \
--build-arg JENKINS_USERID=`id -u` \
--build-arg JENKINS_GROUPID=`id -g` \
-f scripts/docker/debian/jessy/Dockerfile \
scripts/docker/debian/jessy