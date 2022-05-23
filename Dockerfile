# syntax=docker/dockerfile:1

FROM python:3.10.4-slim-buster

WORKDIR /Users/vadramandisang/Documents/Vadrama/data/Product/Miscellaneous/Interchange/Interchange_app

#COPY requirements.txt requirements.txt
COPY Dockerfile Dockerfile
COPY interchange_app.py interchange_app.py

#RUN pip install -r requirements.txt
RUN pip3 install pandas
RUN pip3 install -r https://raw.githubusercontent.com/snowflakedb/snowflake-connector-python/v2.7.6/tested_requirements/requirements_310.reqs
RUN pip3 install snowflake-connector-python
RUN pip3 install "snowflake-connector-python[secure-local-storage,pandas]"


CMD [ "python", "interchange_app.py"]