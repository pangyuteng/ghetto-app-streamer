FROM ubuntu:22.04
RUN apt update && apt install python3 python3-pip curl -yq
RUN curl -fsSL https://get.docker.com | sh

RUN pip3 install flask

COPY . /opt/flask
ENV FLASK_APP=/opt/flask/app.py
WORKDIR /opt/flask