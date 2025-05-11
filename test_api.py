import requests
import json

# API endpoint
url = "http://localhost:8080/predict"

# Test data
data = {
    "features": [2024, 5, 11, 12, 0, 0]
}

# Test prediction
print("Testing prediction endpoint...")
response = requests.post(url, json=data)
print("Status Code:", response.status_code)
print("Response:", response.json())

# Test health endpoint
print("\nTesting health endpoint...")
response = requests.get("http://localhost:8080/health")
print("Status Code:", response.status_code)
print("Response:", response.json()) 