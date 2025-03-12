from datetime import datetime, timedelta
from airflow.models.dag import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonVirtualenvOperator, PythonOperator
import pendulum

# Directed Acyclic Graph
with DAG(
    "virtual",
    schedule="@hourly",
    start_date=pendulum.datetime(2025, 3, 12, tz="Asia/Seoul"),
        default_args = {
        "depends_on_past": False,
    },
    max_active_runs=1,
) as dag:
    
    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end") 
    
    def f_python(**kwargs):
        from myairflow.send_notify import send_noti
        ti = kwargs['data_interval_start'].in_tz('Asia/Seoul').format('YYYYMMDDHH')
        send_noti(f"time {ti} : wminhyuk : python")
        
    
    def f_vpython(dis):
        from myairflow.send_notify import send_noti
        send_noti(f"time : wminhyuk : vpython")
    
    t_vpython = PythonVirtualenvOperator(
        task_id="t_vpython", python_callable=f_vpython, 
        requirements=["git+https://github.com/wminhyuk/myairflow.git@main"],
        op_args=["{{data_interval_start.in_tz('Asia/Seoul').format('YYYYMMDDHH')}}"]
        )
        
    t_python = PythonOperator(
        task_id="t_python", python_callable=f_python
        )
    
    start >> t_vpython >> t_python >> end 
    
if __name__ == "__main__":
    dag.test()
