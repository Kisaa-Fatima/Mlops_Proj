from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from sklearn.preprocessing import MinMaxScaler
import os
import joblib

# Preprocessing function
def preprocess_data():
    raw_data_path = os.path.expanduser('~/airflow/data/raw_live_data.csv')

    if not os.path.exists(raw_data_path):
        print(f"Error: Raw data file not found at {raw_data_path}")
        return

    df = pd.read_csv(raw_data_path)

    # Handle missing values
    df.fillna(0, inplace=True)

    # Optional: Convert datetime column
    if 'datetime' in df.columns:
        df['datetime'] = pd.to_datetime(df['datetime'])
        df['hour'] = df['datetime'].dt.hour
        df['day'] = df['datetime'].dt.day
        df['month'] = df['datetime'].dt.month
        df.drop(columns=['datetime'], inplace=True)

    # Normalize selected columns
    scaler = MinMaxScaler()
    df[['temperature', 'wind_speed']] = scaler.fit_transform(df[['temperature', 'wind_speed']])

    # Save preprocessed data
    processed_data_path = os.path.expanduser('~/airflow/data/processed_data.csv')
    df.to_csv(processed_data_path, index=False)
    print(f"✅ Preprocessed data saved to: {processed_data_path}")

 # Save scaler
    scaler_path = os.path.expanduser('~/airflow/models/minmax_scaler.pkl')
    joblib.dump(scaler, scaler_path)
    print(f"✅ Scaler saved to: {scaler_path}")

# Default args
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# DAG
dag = DAG(
    'weather_data_preprocessing',
    default_args=default_args,
    description='Preprocess weather data',
    schedule_interval=None,
    start_date=datetime(2025, 4, 26),
    catchup=False,
)

# Task
preprocess_data_task = PythonOperator(
    task_id='preprocess_weather_data',
    python_callable=preprocess_data,
    dag=dag,
)

# Trigger next DAG
trigger_training_dag = TriggerDagRunOperator(
    task_id='trigger_model_training_dag',
    trigger_dag_id='weather_model_training',
    dag=dag,
)

preprocess_data_task >> trigger_training_dag
