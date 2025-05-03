from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
import os
import logging

# Training function
def train_model():
    processed_data_path = '/home/ayera/airflow/data/processed_data.csv'
    model_path = '/home/ayera/airflow/models/linear_model.pkl'

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    if not os.path.exists(processed_data_path):
        logger.error(f"Processed data not found at {processed_data_path}")
        return

    df = pd.read_csv(processed_data_path)

    if 'temperature' not in df.columns:
        logger.error("Target column 'temperature' not found in data.")
        return

    X = df.drop(columns=['temperature'])
    y = df['temperature']

    model = LinearRegression()
    model.fit(X, y)

    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(model, model_path)
    logger.info(f"Model trained and saved to: {model_path}")

# DAG default arguments
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# ✅ Use the same variable name as the DAG ID
weather_model_training = DAG(
    'weather_model_training',
    default_args=default_args,
    description='Train ML model on preprocessed weather data',
    schedule_interval=None,
    start_date=datetime(2025, 4, 26),
    catchup=False,
)

# Task
train_model_task = PythonOperator(
    task_id='train_weather_model',
    python_callable=train_model,
    dag=weather_model_training,
)

# Expose the DAG explicitly
globals()['weather_model_training'] = weather_model_training  # This exposes the DAG

