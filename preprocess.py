import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import os

def preprocess_data():
    # Load the raw data
    raw_data_path = os.path.join("data", "raw_live_data.csv")
    if not os.path.exists(raw_data_path):
        print(f"Error: Raw data file not found at {raw_data_path}")
        return

    df = pd.read_csv(raw_data_path)

    # Step 1: Handle Missing Values
    df.fillna(0, inplace=True)

    # Step 2: Normalize numerical columns
    scaler = MinMaxScaler()
    df[['temperature', 'wind_speed']] = scaler.fit_transform(df[['temperature', 'wind_speed']])

    # Step 3: Save preprocessed data
    processed_data_path = os.path.join("data", "processed_data.csv")
    df.to_csv(processed_data_path, index=False)
    print(f"Preprocessed data saved to: {processed_data_path}")

    return df
