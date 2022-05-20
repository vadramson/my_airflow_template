from airflow import DAG  # Indicates the file is a DAG file
from airflow.operators.python import PythonOperator, BranchPythonOperator # Imports the needed operator
from airflow.operators.bash import BashOperator

from random import randint
from datetime import datetime


def choose_best_ml_model(ti): # Returns the ID of the next task to be executed
    accuracies = ti.xcom_pull(task_ids = [
        'tarining_dummy_model_A',
        'tarining_dummy_model_B',
        'tarining_dummy_model_C'
    ]) # Use xcom to share data amongst different tasks

    best_accuracy =  max(accuracies)
    
    if (best_accuracy > 8):
        return 'accurate'
    return 'inaccurate'



def train_dummy_model():
    return randint(1, 10) # Automatically saves the results in the airflow database



# Creating a DAG Object using the context manager with
with DAG("dag_may_20_2022",  # Dag id
start_date=datetime(2022, 1, 1,0,0,0), # start date, the 1st of January 2022 --> This DAG will starts triggered on 02/01/2022
schedule_interval="@daily",  # Cron expression, here it is a preset of Airflow, @daily means once every day at midnight.
catchup=False # Catchup avoids triggering none-trggered DAGs between the start date and the current date
) as dag: 
    
    #tasks

    tarining_dummy_model_A = PythonOperator(    # Task 1 
        task_id = "training_model_A", # task_id must be unique for esach DAG
        python_callable = train_dummy_model # A python callable function
    )

    tarining_dummy_model_B = PythonOperator(    # Task 2 
        task_id = "training_model_B", # task_id must be unique for esach DAG
        python_callable = train_dummy_model # A python callable function
    )

    tarining_dummy_model_C = PythonOperator(    # Task 3
        task_id = "training_model_C", # task_id must be unique for esach DAG
        python_callable = train_dummy_model # A python callable function
    )


    choose_best_model_to_run = BranchPythonOperator(
        task_id = "choose_best_model",
        python_callable = choose_best_ml_model
    )

    accurate = BashOperator(
        task_id = "accurate",
        bash_command = "echo 'accurate' "
    )


    inaccurate = BashOperator(
        task_id = "inaccurate",
        bash_command = "echo 'inaccurate' "
    )

    # Start tasks to the left then >> those to the right >> then those to the further right
    [tarining_dummy_model_A, tarining_dummy_model_B, tarining_dummy_model_C] >> choose_best_model_to_run >> [accurate, inaccurate]


