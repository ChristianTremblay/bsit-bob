FROM ubuntu:22.04

RUN echo 'APT::Install-Suggests "0";' >> /etc/apt/apt.conf.d/00-docker
RUN echo 'APT::Install-Recommends "0";' >> /etc/apt/apt.conf.d/00-docker

RUN apt-get update -qy
RUN apt-get install -y python3-dev python3-pip zip unzip git default-jre

WORKDIR /app
RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY shacl-1.4.2/ shacl-1.4.2/
COPY validate.py .

COPY 223standard.ttl .

