FROM debian:wheezy
MAINTAINER Paddy Carey <paddy@wackwack.co.uk>

# empty file that when touched will force a full rebuild of the container
ADD assets/force_rebuild /force_rebuild

# no tty
ENV DEBIAN_FRONTEND noninteractive

# get up to date
RUN apt-get update --fix-missing && apt-get upgrade -y

# install packages from apt
RUN apt-get install -y ca-certificates make wget unzip python-pip python-imaging python-numpy

# install packages from PyPI
ADD assets/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# Download and install the Appengine Python SDK
RUN wget -nv https://storage.googleapis.com/appengine-sdks/featured/google_appengine_1.9.10.zip
RUN unzip -q google_appengine_1.9.10.zip && rm google_appengine_1.9.10.zip
ENV PATH /google_appengine:$PATH

VOLUME ["/.appengine_storage"]

# default run command
CMD bash

# expose ports (application server & admin server)
EXPOSE 8080
EXPOSE 8000
