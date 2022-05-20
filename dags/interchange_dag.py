import os
from airflow import DAG  # Indicates the file is a DAG file
from airflow.operators.python import PythonOperator, BranchPythonOperator # Imports the needed operator
from airflow.operators.bash import BashOperator

from datetime import datetime

# Creating a DAG Object using the context manager with
with DAG("interchange_dag",  # Dag id
start_date=datetime(2022, 1, 1,0,0,0), # start date, the 1st of January 2022 --> This DAG will starts triggered on 02/01/2022
schedule_interval="@daily",  # Cron expression, here it is a preset of Airflow, @daily means once every day at midnight.
catchup=False # Catchup avoids triggering none-trggered DAGs between the start date and the current date
) as dag:
    run_interchage_container = BashOperator(
        task_id = "run_interchage_container",
        bash_command = "docker run -ti interchange-python-docker"
    )



runn_command = "./home/talend/talend_share/python_scripts/Interchange_app/run_interchange.sh "
if os.path.exists(runn_command):
   t1 = BashOperator(
        task_id= 'create_file',
        bash_command=runn_command,
        dag=dag
   )
else:
    raise Exception("Cannot locate {}".format(runn_command))
