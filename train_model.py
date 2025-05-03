import pandas as pd
from sklearn.linear_model import LinearRegression

# Load preprocessed data
data = pd.read_csv("data/processed_data.csv")

# Convert 'datetime' to datetime object and extract features (you can choose either option)
data['datetime'] = pd.to_datetime(data['datetime'])
data['year'] = data['datetime'].dt.year
data['month'] = data['datetime'].dt.month
data['day'] = data['datetime'].dt.day
data['hour'] = data['datetime'].dt.hour
data['minute'] = data['datetime'].dt.minute
data['second'] = data['datetime'].dt.second
data.drop('datetime', axis=1, inplace=True)  # Drop the original datetime column

# Define X and y
X = data.drop("temperature", axis=1)  # Features
y = data["temperature"]  # Target variable (temperature)

# Initialize and train the model
model = LinearRegression()
model.fit(X, y)

# Save the trained model (optional)
import joblib
joblib.dump(model, 'weather_model.pkl')

