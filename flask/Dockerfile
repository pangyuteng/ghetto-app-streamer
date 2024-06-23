FROM ubuntu:22.04
RUN apt update && apt install python3 python3-pip curl -yq
RUN curl -fsSL https://get.docker.com | sh

RUN mkdir /opt/c3d
COPY c3d-nightly-Linux-x86_64.tar.gz /tmp
RUN tar -xf /tmp/c3d-nightly-Linux-x86_64.tar.gz -C /opt/c3d --strip-components=1

COPY requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt

COPY . /opt/flask
ENV PATH="/opt/c3d/bin:$PATH"
WORKDIR /opt/flask