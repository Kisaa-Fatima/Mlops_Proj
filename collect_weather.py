import requests
import csv

# Your API URL
URL = "https://api.open-meteo.com/v1/forecast?latitude=33.7215&longitude=73.0433&hourly=temperature_2m,wind_speed_10m,relative_humidity_2m,wind_direction_180m,rain,precipitation,showers&timezone=auto&start_date=2025-04-26&end_date=2025-05-01"

# Fetch and write data
def fetch_and_save():
    response = requests.get(URL)
    data = response.json()
    
    hours = data['hourly']['time']
    temperature = data['hourly']['temperature_2m']
    wind_speed = data['hourly']['wind_speed_10m']
    humidity = data['hourly']['relative_humidity_2m']
    wind_dir = data['hourly']['wind_direction_180m']
    rain = data['hourly']['rain']
    precipitation = data['hourly']['precipitation']
    showers = data['hourly']['showers']
    
    with open("data/raw_data.csv", "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["datetime", "temperature_2m", "wind_speed_10m", "relative_humidity_2m", "wind_direction_180m", "rain", "precipitation", "showers"])
        
        for i in range(len(hours)):
            writer.writerow([
                hours[i],
                temperature[i],
                wind_speed[i],
                humidity[i],
                wind_dir[i],
                rain[i],
                precipitation[i],
                showers[i]
            ])

if __name__ == "__main__":
    import os
    os.makedirs("data", exist_ok=True)
    fetch_and_save()
