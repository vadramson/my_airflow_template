# syntax=docker/dockerfile:1

FROM python:3.6-buster

USER root
RUN apt-get update -y \
    && apt-get install -y python3-dev python3-pip build-essential \
    && apt-get install gcc -y \
    && apt-get install sudo -y \ 
    && apt-get clean

RUN apt-get update && \
      apt-get -y install sudo
#RUN adduser --disabled-password --gecos '' airflow

#RUN useradd --disabled-password --gecos '' airflow


RUN useradd -ms /bin/bash airflow

RUN groupadd docker
RUN usermod -a -G docker airflow
RUN usermod -aG docker airflow

#RUN chmod 777 /var/run/docker.sock
USER airflow
#RUN su ${USER}

#USER airflow


CMD ["echo", "Vadrama Says Hi. Lunched from Airflow Docker"]