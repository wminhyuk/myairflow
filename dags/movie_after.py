from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import (
        BranchPythonOperator, 
        PythonVirtualenvOperator,
)

from airflow.sensors.filesystem import FileSensor

with DAG(
    'movie_after',
    default_args={
        'depends_on_past': True,
        'retries': 1,
        'retry_delay': timedelta(seconds=3),
    },
    max_active_runs=1,
    max_active_tasks=5,
    description='movie',
    schedule="10 10 * * *",
    start_date=datetime(2024, 1, 1),
    end_date=datetime(2024, 1, 5),
    catchup=True,
    tags=['api', 'movie'],
) as dag:
    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")
    

    
    check_file = FileSensor(task_id="check.done",
                            filepath="/home/seominhyuk/data/movies/done/dailyboxoffice/{{ds_nodash}}/_DONE",
                            fs_conn_id="fs_after_movie")
    
    start >> check_file >> end