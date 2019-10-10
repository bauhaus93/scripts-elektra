FROM buildelektra-stretch-full

USER root
RUN apt-get update && apt-get -y install vim sudo 
RUN adduser jenkins sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
USER jenkins


