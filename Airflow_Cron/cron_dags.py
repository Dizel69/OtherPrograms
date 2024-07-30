from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

# Определяем функцию, которая будет выполняться
def my_task():
    print("Выполняем задачу")

# Определяем DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'my_cron_dag',
    default_args=default_args,
    description='Пример DAG, имитирующий cron job',
    schedule_interval='0 12 * * *',  # Это cron-выражение для запуска каждый день в 12:00
)

# Определяем задачу
task = PythonOperator(
    task_id='my_task',
    python_callable=my_task,
    dag=dag,
)
