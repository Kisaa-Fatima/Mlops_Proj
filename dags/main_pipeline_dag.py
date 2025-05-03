from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import subprocess

# Define functions for each step in the pipeline
def trigger_collect_weather(*args, **kwargs):
    # Here you can call your weather collection script or function
    subprocess.run(["python", "/home/ayera/weather-pipeline/collect_weather.py"])

def trigger_preprocess_data(*args, **kwargs):
    # Here you can call your data preprocessing script or function
    subprocess.run(["python", "/home/ayera/weather-pipeline/preprocess.py"])

def trigger_train_model(*args, **kwargs):
    # Here you can call your model training script or function
    subprocess.run(["python", "/home/ayera/weather-pipeline/train_model.py"])

# Set default args for the DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 5, 1),
    'retries': 1,
}

# Create the DAG
with DAG('weather_pipeline', default_args=default_args, schedule_interval='@daily') as dag:
    start = DummyOperator(task_id='start')

    collect_data = PythonOperator(
        task_id='collect_weather_data',
        python_callable=trigger_collect_weather
    )

    preprocess_data = PythonOperator(
        task_id='preprocess_weather_data',
        python_callable=trigger_preprocess_data
    )

    train_model = PythonOperator(
        task_id='train_model',
        python_callable=trigger_train_model
    )

    # Define the order of the tasks
    start >> collect_data >> preprocess_data >> train_model
