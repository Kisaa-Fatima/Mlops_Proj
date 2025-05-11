# Weather Prediction MLOps Pipeline

This project implements an end-to-end MLOps pipeline for weather prediction, including data collection, processing, model training, and deployment.

## Project Structure

```
weather-pipeline/
├── .github/
│   └── workflows/
│       └── ci.yml
├── data/
│   ├── raw/
│   └── processed/
├── src/
│   ├── data/
│   └── models/
├── tests/
├── airflow/
├── Dockerfile
├── Jenkinsfile
├── dvc.yaml
├── requirements.txt
└── README.md
```

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/Kisaa-Fatima/MLOPS_PROJECT.git
cd MLOPS_PROJECT
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize DVC:
```bash
dvc init
```

5. Start MLflow server:
```bash
mlflow server --host 0.0.0.0 --port 5000
```

## Running the Pipeline

1. Data Collection and Processing:
```bash
dvc repro
```

2. Model Training:
```bash
python src/models/train.py
```

3. Docker Build:
```bash
docker build -t kisaafatimadocker/weather-app:latest .
```

4. Kubernetes Deployment:
```bash
kubectl apply -f deployment.yaml
```

## API Endpoints

- `POST /predict`: Get weather predictions
  - Input: JSON with features
  - Output: Predicted temperature

## CI/CD Pipeline

The project uses:
- GitHub Actions for CI
- Jenkins for CD
- Docker for containerization
- Kubernetes for orchestration

## Contributing

1. Create a feature branch
2. Make your changes
3. Submit a pull request

## License

MIT License 