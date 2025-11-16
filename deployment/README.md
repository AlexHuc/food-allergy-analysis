# Deployment

This directory contains all resources needed to deploy the Food Allergy & Asthma prediction models using either **Flask + Docker** or **Kubernetes**.

## Structure

### `flask/`
This folder provides a lightweight web service exposing the prediction model through a REST API.

- **Dockerfile** – Builds a Docker image for the Flask service  
- **Pipfile / Pipfile.lock** – Dependency management using Pipenv  
- **predict.py** – Flask app serving prediction endpoints  
- **predict_test.ipynb** – Notebook for testing the API  
- **README.md** – Instructions for running the Flask service locally or via Docker

### `kubernetes/`
This folder contains the configuration required to run the model in a Kubernetes cluster.

- **deployment.yaml** – Kubernetes manifests for the API  
- **deploy.sh** – Shell script to apply the manifests and manage the deployment  
- **README.md** – Guide for deploying using Minikube or a cloud Kubernetes cluster

---

Both deployment options package the same trained model, allowing you to run inference in local, containerized, or distributed environments.
