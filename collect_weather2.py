import requests
import csv
import os
from datetime import datetime

# Define API URL for live weather data (current weather)
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
        "weather_condition": weather.get("weathercode")  # You may map the weather code
    }

    # Ensure data folder exists
    os.makedirs("data", exist_ok=True)

    # Write to CSV
    filename = "data/raw_live_data.csv"
    write_header = not os.path.exists(filename)
    with open(filename, "a", newline="") as csvfile:
        fieldnames = ["datetime", "temperature", "wind_speed", "wind_direction", "weather_condition"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        writer.writerow(weather_data)

    print("Live weather data saved to:", filename)

if __name__ == "__main__":
    fetch_and_save()
