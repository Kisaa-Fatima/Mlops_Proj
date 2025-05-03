from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import csv
import os

# Define API URL for live weather data
url = (
    "https://api.open-meteo.com/v1/forecast?"
    "latitude=33.7215&longitude=73.0433&"
    "current_weather=true&"
    "timezone=auto"
)

def fetch_and_save():
    # Fetch data
    response = requests.get(url)
    data = response.json()
    
    # Extract live weather data
    weather = data.get("current_weather")
    if not weather:
        print("Error: 'current_weather' data not found.")
        print("Full response:", data)
        return

    # Prepare data
    weather_data = {
        "datetime": datetime.now().isoformat(),
        "temperature": weather.get("temperature"),
        "wind_speed": weather.get("windspeed"),
        "wind_direction": weather.get("winddirection"),
        "weather_condition": weather.get("weathercode")  # Optional: map the weather code
    }

    # Define absolute path for the data directory
    data_dir = os.path.expanduser('~/airflow/data')
    os.makedirs(data_dir, exist_ok=True)

    # Write to CSV
    filename = os.path.join(data_dir, "raw_live_data.csv")
    write_header = not os.path.exists(filename)
    with open(filename, "a", newline="") as csvfile:
        fieldnames = ["datetime", "temperature", "wind_speed", "wind_direction", "weather_condition"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        writer.writerow(weather_data)

    print("✅ Live weather data saved to:", filename)

# Set up the DAG
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'weather_data_pipeline',  
    default_args=default_args,
    description='Fetch live weather data and save it',
    schedule_interval=timedelta(minutes=2),  # Adjust schedule as needed
    start_date=datetime(2025, 4, 26),
    catchup=False,  
)

# Set up the task in Airflow
fetch_data_task = PythonOperator(
    task_id='fetch_and_save_weather_data',
    python_callable=fetch_and_save,
    dag=dag,
)

# Trigger preprocessing DAG after fetching data
trigger_preprocess_task = TriggerDagRunOperator(
    task_id='trigger_preprocess_dag',
    trigger_dag_id='weather_data_preprocessing',  # Name of the preprocessing DAG
    dag=dag,
)

# Set task dependencies: Fetch data -> Trigger Preprocessing
fetch_data_task >> trigger_preprocess_task
