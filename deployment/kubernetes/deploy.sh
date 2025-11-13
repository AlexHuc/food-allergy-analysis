#!/bin/bash
# Complete deployment script
# Run this script from the PROJECT ROOT directory

echo "🚀 Starting Asthma Prediction Service Deployment"

# Check if running from project root
if [ ! -d "deployment" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    echo "Usage: ./deployment/kubernetes/deploy.sh"
    exit 1
fi

# Step 1: Start minikube
echo "📦 Starting minikube..."
minikube start

# Step 2: Build Docker image in minikube's Docker environment
echo "🐳 Building Docker image..."
eval $(minikube docker-env)
docker build -t asthma-predictor:latest -f deployment/flask/Dockerfile .

# Check if build was successful
if [ $? -ne 0 ]; then
    echo "❌ Docker build failed!"
    exit 1
fi

# Step 3: Deploy to Kubernetes
echo "☸️ Deploying to Kubernetes..."
kubectl apply -f deployment/kubernetes/deployment.yaml

# Step 4: Wait for deployment
echo "⏳ Waiting for deployment to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/asthma-prediction-deployment -n asthma-prediction

# Step 5: Get service URL (non-blocking)
echo "🌐 Getting service URL..."
NODE_PORT=$(kubectl get service asthma-prediction-service -n asthma-prediction -o jsonpath='{.spec.ports[0].nodePort}')
MINIKUBE_IP=$(minikube ip)
SERVICE_URL="http://${MINIKUBE_IP}:${NODE_PORT}"

echo "Service available at: $SERVICE_URL"

# Step 6: Test health endpoint
echo "🏥 Testing health endpoint..."
sleep 5
curl -X GET "$SERVICE_URL/health"
echo ""

# Step 7: Show pod status
echo ""
echo "📊 Pod Status:"
kubectl get pods -n asthma-prediction

# Step 8: Example test command
echo ""
echo "✅ Deployment complete!"
echo "🔗 Service URL: $SERVICE_URL"
echo ""
echo "🧪 Test with:"
echo "curl -X POST $SERVICE_URL/predict -H 'Content-Type: application/json' -d '{\"BIRTH_YEAR\": 2015, \"GENDER_FACTOR\": \"M\", \"RACE_FACTOR\": \"White\", \"ETHNICITY_FACTOR\": \"Non-Hispanic\", \"PAYER_FACTOR\": \"Non-Medicaid\", \"ATOPIC_MARCH_COHORT\": true, \"AGE_START_YEARS\": 2.5, \"NUM_ALLERGIES\": 2}'"
echo ""
echo "📊 To open Kubernetes dashboard, run: minikube dashboard"
echo "📝 To view logs, run: kubectl logs -n asthma-prediction -l app=asthma-prediction"
