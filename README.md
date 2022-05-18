# my_airflow_template
This repository contains a starter template for airflow projects

**Start by downloading the current Airflow .yml file ("https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml")[here]**

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
![Screenshot 2022 05 18 At 17.48.09](/var/folders/vp/c_kgx06n7dq2rtfy8_mhq1dw0000gp/T/TemporaryItems/NSIRD_screencaptureui_aiCGTv/Screenshot%202022-05-18%20at%2017.48.09.png)


Enter the username and password as specified in the docker-compose file and login. The following screen should be displayed
![Screenshot 2022 05 18 At 17.48.09](/var/folders/vp/c_kgx06n7dq2rtfy8_mhq1dw0000gp/T/TemporaryItems/NSIRD_screencaptureui_aiCGTv/Screenshot%202022-05-18%20at%2017.48.09.png)


#### Restart a running airflow container use the following command

	docker-compose down && docker-compose up  

#### Accessing an Airflow container's CLI

Using the command
 	
	docker ps 

get the desired container ID. For example the webserver container ID as shown in the image below
![Screenshot 2022 05 18 At 17.48.09](/var/folders/vp/c_kgx06n7dq2rtfy8_mhq1dw0000gp/T/TemporaryItems/NSIRD_screencaptureui_aiCGTv/Screenshot%202022-05-18%20at%2017.48.09.png)

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

