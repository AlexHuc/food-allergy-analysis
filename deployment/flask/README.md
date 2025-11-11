# Flask Deployment for Asthma Prediction Service

This folder contains the Dockerized Flask service for serving the asthma prediction machine learning models.  
It includes the `Pipfile`, `Pipfile.lock`, and `Dockerfile` used to build and run the service.

---

## 📦 Python Environment

We used **Pipenv** to manage dependencies.  

### Steps to create `Pipfile` and install packages:

1. Install Pipenv (if not installed):
```bash
pip install pipenv
```

2. Initialize the Pipfile and install required packages:
```bash
pipenv install xgboost flask gunicorn scikit-learn pandas numpy
```

This generates `Pipfile` and `Pipfile.lock` automatically.
- `Pipfile` specifies the Python version and project dependencies.
- `Pipfile.lock` locks the exact versions for reproducible builds.

## 🐳 Docker Setup

The `Dockerfile` builds a container image for the Flask service.

Key points:
- Uses lightweight `python:3.12-slim` base image.
- Installs Pipenv to handle Python dependencies.
- Copies the model files (`.bin`) and the Flask app (`predict.py`) into the container.
- Runs the service with Gunicorn on port `9696`.

**Build the Docker image**
From the root of the project, run:
```bash
docker build -t asthma-predictor -f deployment/flask/Dockerfile .
```

**Run the Docker container**
```bash
docker run -it --rm -p 9696:9696 asthma-predictor
```
- The Flask service will be available at `http://localhost:9696/predict`.

## ⚡ Notes
- Make sure all model `.bin` files are present in the `models/` folder before building the Docker image.
- Any Python package used in `predict.py` (like `scikit-learn`, `xgboost`, `pandas`, `numpy`) must be listed in the Pipfile.
- This setup ensures the service runs consistently across machines and environments.