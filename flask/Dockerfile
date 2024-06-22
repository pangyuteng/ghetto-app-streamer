FROM ubuntu:22.04
RUN apt update && apt install python3 python3-pip curl -yq
RUN curl -fsSL https://get.docker.com | sh

COPY requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt

COPY . /opt/flask
WORKDIR /opt/flask