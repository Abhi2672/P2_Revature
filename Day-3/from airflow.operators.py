from airflow.operators.bash import BashOperator
from airflow import DAG
from datetime import datetime

with DAG('get_ip', start_date=datetime(2023, 1, 1), schedule_interval=None, catchup=False) as dag:
    t1 = BashOperator(
        task_id='print_ip',
        bash_command='curl https://ifconfig.me'
    )