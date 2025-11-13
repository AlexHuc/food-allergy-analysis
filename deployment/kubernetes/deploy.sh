#!/bin/bash
# Deployment script for Asthma Prediction Service

echo "🚀 Deploying Asthma Prediction Service"

# Check if running from project root
if [ ! -d "deployment" ]; then
    echo "❌ Run this from the project root directory"
    exit 1
fi

# Start minikube
echo "📦 Starting minikube..."
minikube start

# Build image
echo "🐳 Building Docker image..."
eval $(minikube docker-env)
docker build -t asthma-predictor:latest -f deployment/flask/Dockerfile .

# Deploy to Kubernetes
echo "☸️ Deploying to Kubernetes..."
kubectl apply -f deployment/kubernetes/deployment.yaml

# Wait for deployment
echo "⏳ Waiting for pod to be ready..."
kubectl wait --for=condition=ready pod -l app=asthma-prediction -n asthma-prediction --timeout=60s

# Show status
echo ""
echo "📊 Status:"
kubectl get pods -n asthma-prediction
kubectl get service -n asthma-prediction

# Set up port forwarding to consistent port
echo ""
echo "🌐 Setting up port forwarding to localhost:9696..."

# Kill any existing port forward on 9696
pkill -f "kubectl port-forward.*9696" 2>/dev/null || true

# Start port forwarding in background
kubectl port-forward service/asthma-prediction-service 9696:80 -n asthma-prediction &
PORT_FORWARD_PID=$!

# Give it a moment to establish
sleep 2

echo "✅ Service available at: http://localhost:9696"

echo ""
echo "✅ Deployment complete!"
echo ""
echo "🔗 Service URL: http://localhost:9696"
echo ""
echo "📊 To open dashboard:"
echo "   minikube dashboard"
echo "   (Select 'asthma-prediction' namespace)"
echo ""
echo "🧪 To test the API:"
echo "   curl -X GET http://localhost:9696/health"
echo "   curl -X POST http://localhost:9696/predict -H 'Content-Type: application/json' -d '{...}'"
echo ""
echo "📝 Note: Port forwarding is running in background (PID: $PORT_FORWARD_PID)"
echo "   To stop: kill $PORT_FORWARD_PID"
echo "   Keep this terminal open while using the service"