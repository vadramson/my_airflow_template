
from datetime import datetime, timedelta

from setuptools import Command
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.docker_operator import DockerOperator
from airflow.operators.python_operator import BranchPythonOperator
from airflow.operators.dummy_operator import DummyOperator

default_var_args = {
'owner'                 : 'airflow',
'description'           : 'Use of the DockerOperator',
'depend_on_past'        : False,
'start_date'            : datetime(2022, 9, 11),
'email_on_failure'      : True,
'email_on_retry'        : False,
'retries'               : 1,
'retry_delay'           : timedelta(minutes=5)
}

with DAG('enrich_merchant_dag', default_args=default_var_args, schedule_interval="@weekly", catchup=False) as dag:
    start_dag = DummyOperator(
        task_id='starting_up'
        )

    run_enrich_station = DockerOperator(
        privileged=True,
        task_id='command_to_run_enrich_merchant_docker_image',
        image='enrich-station-service-python-docker-container',
        container_name='run_enrich-station-python-docker', 
        api_version='auto',
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge"
        #mount_tmp_dir=True, 
        #tmp_dir='/tmp/airflow'
    )

    start_dag >> run_enrich_station