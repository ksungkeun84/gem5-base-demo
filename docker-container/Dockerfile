FROM ubuntu:20.04
MAINTAINER Sungkeun Kim <ksungkeun84@tamu.edu>

######################################
# Utility tools
######################################
RUN apt-get update
RUN apt-get install -y bash
RUN apt-get install -y vim


######################################
# gem5
######################################
RUN apt-get install -y build-essential 
RUN apt-get install -y git-core 
RUN apt-get install -y m4
RUN apt-get install -y zlib1g 
RUN apt-get install -y zlib1g-dev 
RUN apt-get install -y libprotobuf-dev 
RUN apt-get install -y protobuf-compiler 
RUN apt-get install -y libprotoc-dev 
RUN apt-get install -y libgoogle-perftools-dev 
RUN apt-get install -y swig python-dev 
RUN apt-get install -y python 
RUN apt-get install -y python3.8 python3-dev
RUN apt-get install -y pip
RUN apt-get install -y libprotobuf-dev 
RUN apt-get install -y protobuf-compiler 
RUN apt-get install -y libgoogle-perftools-dev

# make python3.8 default
#RUN rm /usr/bin/python
#RUN ln -s /usr/bin/python3.8 /usr/bin/python

######################################
# Celery
######################################
RUN apt-get install -y rabbitmq-server
RUN pip install gem5art-artifact gem5art-run gem5art-tasks
RUN pip install dnspython
RUN pip install celery
RUN pip install flower

######################################
# gem5 ver 19 requires to use python 2
######################################
WORKDIR /
RUN apt-get install -y curl
RUN curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output get-pip.py
RUN python2 get-pip.py
RUN pip2 install six
RUN pip2 install scons


# remove broker uri (local) - it causes issue in docker
WORKDIR /usr/local/lib/python3.8/dist-packages/gem5art/tasks
RUN sed -i "s/broker.*,//g" celery.py

ENV C_FORCE_ROOT="true"

######################################
# Set working directory
######################################
RUN mkdir /autoperf
VOLUME /autoperf
WORKDIR /autoperf

RUN apt-get clean

CMD bash

