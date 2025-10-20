from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

with DAG(
    'retrain_model',
    schedule_interval='0 2 * * *',  # каждый день в 2:00
    start_date=datetime(2025, 10, 21),
    catchup=False
) as dag:

    retrain = BashOperator(
        task_id='train_model',
        bash_command='python /services/ml_service/train.py'
    )

    deploy = BashOperator(
        task_id='deploy_model',
        bash_command='cp /models/als_model_v1.npz /services/models/als_model_v1.npz'
    )


    retrain >> deploy