from datetime import timedelta, datetime
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from scripts.jobs_extraction_etl import run_remotive_etl

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2026, 2, 5),
    'email': ['ephraimkonje01@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1, 
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
    'remotive_jobs_etl',
    default_args = default_args,
    description = 'A DAG to run the Remotive jobs ETL process',
    schedule=timedelta(days=1),
)

run_etl = PythonOperator(
    task_id = 'run_remotive_etl',
    python_callable = run_remotive_etl,
    dag = dag,
)

run_etl
