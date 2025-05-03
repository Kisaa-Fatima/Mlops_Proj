import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import os

def preprocess_data():
    # Load the raw data
    raw_data_path = os.path.join("data", "raw_data.csv")
    if not os.path.exists(raw_data_path):
        print(f"Error: Raw data file not found at {raw_data_path}")
        return

    print(f"Loading data from {raw_data_path}...")
    df = pd.read_csv(raw_data_path)
    print(f"Data loaded. Columns: {df.columns}")
    print(f"First few rows of data:\n{df.head()}")

    # Step 1: Handle Missing Values
    print("Handling missing values...")
    df.fillna(0, inplace=True)

    # Step 2: Normalize numerical columns
    print("Normalizing numerical columns...")
    scaler = MinMaxScaler()
    #df[['temperature', 'wind_speed']] = scaler.fit_transform(df[['temperature', 'wind_speed']])
    df[['temperature_2m', 'wind_speed_10m']] = scaler.fit_transform(df[['temperature_2m', 'wind_speed_10m']])
    # Step 3: Save preprocessed data
    processed_data_path = os.path.join("data", "processed_data.csv")
    print(f"Saving preprocessed data to: {processed_data_path}")
    df.to_csv(processed_data_path, index=False)

    print(f"Preprocessed data saved to: {processed_data_path}")
    return df

if __name__ == "__main__":
    preprocess_data()

