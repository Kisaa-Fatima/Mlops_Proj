from flask import Flask, jsonify, request
import joblib
import numpy as np

# Define the model class
class DummyWeatherModel:
    def predict(self, X):
        # Return a fixed temperature of 25.5°C
        return np.array([25.5])

app = Flask(__name__)

# Create a new model instance instead of loading from file
model = DummyWeatherModel()

@app.route("/")
def home():
    return """
    <h1>Weather Prediction API</h1>
    <p>Try these endpoints:</p>
    <ul>
        <li><a href="/health">/health</a> - Check if the model is loaded</li>
        <li>/predict - POST request with {"features": [2024, 5, 11, 12, 0, 0]}</li>
    </ul>
    """

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "model_loaded": True,
        "message": "Model is ready to make predictions!"
    })

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        if not data or 'features' not in data:
            return jsonify({"error": "Please provide features"}), 400

        # Make prediction
        features = np.array(data['features']).reshape(1, -1)
        prediction = model.predict(features)[0]

        return jsonify({
            "prediction": float(prediction),
            "unit": "celsius",
            "message": "Temperature prediction successful!"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
