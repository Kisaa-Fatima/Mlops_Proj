import numpy as np
import joblib

# Create a simple dummy model that just returns a fixed temperature
class DummyWeatherModel:
    def predict(self, X):
        # Return a fixed temperature of 25.5°C
        return np.array([25.5])

# Create and save the model
model = DummyWeatherModel()
joblib.dump(model, 'weather_model.pkl')
print("Dummy model saved as weather_model.pkl") 