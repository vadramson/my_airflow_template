## What can you do with Airflow?

In Layman’s term, Airflow is an orchestration tool, which means it will trigger tasks on schedule, or when certain events happen (such as an API call or when a sensor operator senses an action). Here are some possible use cases of Airflow:

- **Replace cron jobs:** monitoring cron jobs is hard and tedious. Instead of manually ssh to servers to find out if/why your jobs fail, you can visually see whether your code run or not through the UI and have Airflow notifies you when a job fails.

- Extract data: Airflow, with its many integrations, are used a lot for data engineering tasks. You can write tasks to extract data from your production databases, check data quality, and write the results to your on-cloud data warehouse.

- **Transform data:** you can interface with external services to process your data. For example, you can have a pipeline that submits a job to EMR to process data in S3 with Spark and writes the results to your Redshift data warehouse.

- **Train machine learning models:** you can extract data from a data warehouse, do feature engineering, train a model, and write the results to a NoSQL database to be consumed by other applications.

- **Crawl data from the Internet:** you can write tasks to periodically crawl data from the Internet and write to your database. For instance, you can get daily competitor’s prices or get all comments from your company’s Facebook page.

__The possibilities are endless.__



**DAGs**

-  DAG is an acronym for a directed acyclic graph, which is a fancy way of describing a graph that is direct and does not form a cycle (a later node never point to an earlier one). Think of DAG in Airflow as a pipeline with nodes (tasks in a DAG, such as “start”, “section-1-task-1”, …) and edges (arrows).


**Operator, sensor, task**

- An operator defines what gets done within a task. Some example operators are PythonOperator (execute a python script), BashOperator(run a bash script)…

- A sensor is an operator that waits for a specific event to happen. For instance, a file is written to an S3 bucket, a database row is inserted, or an API call happens.

- A task is simply an instantiated operator. In your dag definition, you can define task dependency with Python code. That is which execute B, C after task A, and D after task B, C.

# my_airflow_template
This repository contains a starter template for airflow projects

Start by downloading the current Airflow .yml file **[Here](https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml)**

#### Create the needed folders with
	mkdir dags logs plugins

#### Export current system permision by creating an env file with
	echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env


#### initialize the Airflow instance with the airflow service using the command 
	docker-compose up airflow-init
This pulls all the images and create all the services listed in the docker-compose file 

#### After initializing the Airflow instance, you can now run all the services listed in the docker-compose file using the command 
	docker-compose up
This starts all the servives

#### To check which services are running, enter the command 
	docker ps

#### To verify the running airflow instance, enter the following link in a web browse
	http://localhost:8080/home

The following page should be display 

![Login Screen](https://github.com/vadramson/my_airflow_template/blob/main/img/airflow_login.png)


Enter the username and password as specified in the docker-compose file and login.
The following screen should be displayed

![Connected Screen](https://github.com/vadramson/my_airflow_template/blob/main/img/airflow_after_login.png)


#### Restart a running airflow container use the following command

	docker-compose down && docker-compose up  

#### Accessing an Airflow container's CLI

Using the command
 	
	docker ps 

get the desired container ID. For example the webserver container ID as shown in the image below
![Highlighted Container ID](https://github.com/vadramson/my_airflow_template/blob/main/img/airflow_running_container.png)

The enter the command 

docker exec <container_ID> airflow <desired-command>

	docker exec e23404e1d901 airflow version

The current Airflow version should be displayed in the terminal


#### Accessing an Airflow API
Make sure your docker-compose file has the following command

	AIRFLOW__API__AUTH_BACKENDS: 'airflow.api.auth.backend.basic_auth'

Then using the following command to get all the available dags 

	curl -X GET --user "airflow-username:airflow-password" "http://localhost:8080/api/v1/dags"

	curl -X GET --user "airflow:airflow" "http://localhost:8080/api/v1/dags"

