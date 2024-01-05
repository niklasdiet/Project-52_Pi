FROM ubuntu:16.04

RUN apt-get update && \
	apt-get install python-pip libatlas3-base -y && \
	pip install -U pip

RUN pip install -U reqiuments.txt