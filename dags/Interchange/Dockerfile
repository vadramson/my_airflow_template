# syntax=docker/dockerfile:1

#FROM python:3.6-buster

FROM python:3.10.4-slim-buster

WORKDIR /Users/vadramandisang/Documents/Vadrama/data/Product/Docker-Airflow/Airflow/my_airflow_template/dags/Interchange

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

# --  Start add python dependencies

#COPY requirements.txt requirements.txt
COPY Dockerfile Dockerfile
COPY dags/Interchange/interchange_app.py dags/Interchange/interchange_app.py

#RUN pip install -r requirements.txt
RUN pip3 install pandas
RUN pip3 install -r https://raw.githubusercontent.com/snowflakedb/snowflake-connector-python/v2.7.6/tested_requirements/requirements_310.reqs
RUN pip3 install snowflake-connector-python
RUN pip3 install "snowflake-connector-python[secure-local-storage,pandas]"

# --  End add python dependencies

#RUN chmod 777 /var/run/docker.sock
USER airflow
#RUN su ${USER}

#USER airflow


# CMD ["echo", "Vadrama Says Hi. Lunched from Airflow Docker"]
CMD [ "python", "dags/Interchange/interchange_app.py"]