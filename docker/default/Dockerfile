FROM buildelektra-debian-stretch

RUN apt-get install flex sudo
RUN echo "jenkins:jenkins" | chpasswd && adduser jenkins sudo
RUN visudo
# RUN echo "jenkins" | passwd jenkins 


