FROM debian:wheezy
MAINTAINER Paddy Carey <paddy@wackwack.co.uk>

# empty file that when touched will force a full rebuild of the container
ADD assets/force_rebuild /force_rebuild

# no tty
ENV DEBIAN_FRONTEND noninteractive

# get up to date
RUN apt-get update --fix-missing
RUN apt-get upgrade -y

# install packages from apt
RUN apt-get install -y ca-certificates make wget unzip
RUN apt-get install -y python-pip python-imaging python-numpy

# install local packages
ADD assets/python-coverage_3.7.1_amd64.deb /packages/python-coverage_3.7.1_amd64.deb
RUN dpkg -i /packages/python-coverage_3.7.1_amd64.deb

ADD assets/python-nose_1.3.4_all.deb /packages/python-nose_1.3.4_all.deb
RUN dpkg -i /packages/python-nose_1.3.4_all.deb

ADD assets/python-yanc_0.2.4_all.deb /packages/python-yanc_0.2.4_all.deb
RUN dpkg -i /packages/python-yanc_0.2.4_all.deb

# Download and install the Appengine Python SDK
RUN wget -nv https://storage.googleapis.com/appengine-sdks/featured/google_appengine_1.9.10.zip
RUN unzip google_appengine_1.9.10.zip
RUN rm google_appengine_1.9.10.zip
ENV PATH /google_appengine:$PATH

VOLUME ["/.appengine_storage"]

# default run command
CMD bash

# expose ports (application server & admin server)
EXPOSE 8080
EXPOSE 8000
