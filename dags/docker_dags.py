
from datetime import datetime, timedelta

from setuptools import Command
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.docker_operator import DockerOperator
from airflow.operators.python_operator import BranchPythonOperator
from airflow.operators.dummy_operator import DummyOperator

default_args = {
'owner'                 : 'airflow',
'description'           : 'Use of the DockerOperator',
'depend_on_past'        : False,
'start_date'            : datetime(2022, 5, 1),
'email_on_failure'      : True,
'email_on_retry'        : False,
'retries'               : 1,
'retry_delay'           : timedelta(minutes=5)
}

with DAG('docker_operator_demo', default_args=default_args, schedule_interval="5 * * * *", catchup=False) as dag:
    start_dag = DummyOperator(
        task_id='start_dag'
        )

    end_dag = DummyOperator(
        task_id='end_dag'
        )        

    t1 = BashOperator(
        task_id='print_current_date',
        bash_command='date'
        )

    tdoc = BashOperator(
        task_id='run_docker_from_BashOperator',
        bash_command = "docker run -ti python_rquest_app "
        )    
        
    t2 = DockerOperator(
        privileged=True,
        task_id='docker_command_hello',
        image='python_rquest_app',
        container_name='task___command_hello',
        api_version='auto',
        auto_remove=True,
        #command="python /opt/airflow/dags/Interchange/interchange_app.py",
        command = "docker run -ti python_rquest_app ",
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        mount_tmp_dir=True, 
        tmp_dir='/tmp/airflow'
        )

    t3 = DockerOperator(
        privileged=True,
        task_id='docker_command_world',
        image='docker_image_task',
        container_name='task___command_world',
        api_version='auto',
        auto_remove=True,
        #command="echo I am Running HELLO, I was launched from an Airflow Container",
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        mount_tmp_dir=True, 
        tmp_dir='/tmp/airflow'
        )

    t3doc = DockerOperator(
        privileged=True,
        task_id='comman_to_run_request_launch',
        image='python_rquest_app',
        container_name='task___request_launch',
        api_version='auto',
        auto_remove=True,
        #command="python request_launch.py",
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge"
        #mount_tmp_dir=True, 
        #tmp_dir='/tmp/airflow'
        )

    t4 = BashOperator(
        task_id='print_hello',
        bash_command='echo "hello world"'
        )
    
    t_who = BashOperator(
        task_id = "who_am_I",
        bash_command = "echo Nice to meet you $USER"
    )

    start_dag >> t1 >> t_who
    
    t_who >> t2 >> t4
    t_who >> t3 >> t4

    t4 >> end_dag
