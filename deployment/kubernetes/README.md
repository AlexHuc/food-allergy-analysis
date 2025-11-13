# Kubernetes Local Deployment

![Minikube and Kubernetes](../../imgs/minikube_and_kubernetes.png)

This project includes a complete Kubernetes deployment setup for the Asthma Prediction Service using minikube for local development and testing.

## 📋 Prerequisites

- [Docker](https://www.docker.com/) installed and running
- [minikube](https://minikube.sigs.k8s.io/docs/start/) installed
- [kubectl](https://kubernetes.io/docs/tasks/tools/) installed

## 🚀 Deployment

### 1. Deploy to Local Kubernetes Cluster

```bash
# From the project root directory
./deployment/kubernetes/deploy.sh
```

The deployment script will:
- Start minikube
- Build the Docker image in minikube's environment
- Deploy the service to Kubernetes
- Wait for the pod to be ready
- Display service information

### 2. Access the Service

```bash
# Get the service URL
minikube service asthma-prediction-service -n asthma-prediction --url

# Or open in browser directly
minikube service asthma-prediction-service -n asthma-prediction
```

### 3. View in Kubernetes Dashboard

```bash
# Open Kubernetes dashboard
minikube dashboard
```

**Important:** In the dashboard, select **"asthma-prediction"** from the namespace dropdown to view your deployment.

## 🧪 Testing the Service

### Health Check

```bash
SERVICE_URL=$(minikube service asthma-prediction-service -n asthma-prediction --url)
curl -X GET $SERVICE_URL/health
```

**Response:**
```json
{
  "service": "asthma-prediction",
  "status": "healthy",
  "timestamp": "2025-11-13 20:42:53.123456"
}
```

### Prediction Test

```bash
curl -X POST $SERVICE_URL/predict \
  -H "Content-Type: application/json" \
  -d '{
    "BIRTH_YEAR": 2015,
    "GENDER_FACTOR": "Female",
    "RACE_FACTOR": "White",
    "ETHNICITY_FACTOR": "Non-Hispanic",
    "PAYER_FACTOR": "Private",
    "ATOPIC_MARCH_COHORT": 1,
    "AGE_START_YEARS": 2.5,
    "NUM_ALLERGIES": 2
  }'
```

**Response:**
```json
{
  "asthma": false,
  "asthma_probability": 0.23
}
```

For patients with high asthma risk, the response includes predicted onset age:
```json
{
  "asthma": true,
  "asthma_probability": 0.85,
  "asthma_start_age_predicted": 4.2
}
```

## 📁 Deployment Structure

```
deployment/kubernetes/
├── deploy.sh              # Simple deployment script
└── deployment.yaml        # Kubernetes manifests (namespace, configmap, deployment, service)
```

## 🛠️ Useful Commands

```bash
# Check deployment status
kubectl get all -n asthma-prediction

# View pod logs
kubectl logs -l app=asthma-prediction -n asthma-prediction

# Delete deployment
kubectl delete -f deployment/kubernetes/deployment.yaml

# Stop minikube
minikube stop
```

## 🔧 Service Configuration

- **Image:** `asthma-predictor:latest` (built locally)
- **Port:** Service runs on port 80, forwards to container port 9696
- **NodePort:** 30080 for external access
- **Namespace:** `asthma-prediction`
- **Health Checks:** Readiness and liveness probes on `/health`
- **Resources:** 250m-500m CPU, 512Mi-1Gi Memory

## 📊 Architecture

The deployment creates:
1. **Namespace:** `asthma-prediction` for resource isolation
2. **ConfigMap:** Environment configuration
3. **Deployment:** Single replica of the Flask application
4. **Service:** NodePort service for external access

The Flask application serves two endpoints:
- `GET /health` - Health check endpoint
- `POST /predict` - ML prediction endpoint

This provides a complete local Kubernetes environment for developing and testing the asthma prediction service.