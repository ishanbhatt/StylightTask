FROM ubuntu:18.04

MAINTAINER Ishan Bhatt <ishan_bhatt@hotmail.com>

RUN mkdir Stylight-Task
COPY requirements.txt Stylight-Task/requirements.txt

RUN apt-get update && apt-get install -y \
    python3-pip \
	build-essential \
	libssl-dev \
	libsasl2-dev \
	libldap2-dev \
	libffi-dev \
	python3-dev \
	libcurl4-openssl-dev \
	libssl-dev \
	cmake \
	pkg-config

RUN pip3 install -r Stylight-Task/requirements.txt
COPY . Stylight-Task

WORKDIR Stylight-Task

ENTRYPOINT ["/bin/bash", "gunicorn.sh"]