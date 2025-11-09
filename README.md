# Food Allergy Progression Prediction System

## Description of the Problem

### Background
Food allergies affect millions of people worldwide and can develop at any age, with some individuals experiencing multiple allergies throughout their lifetime. Understanding patterns of allergy development, particularly in pediatric populations, is crucial for early intervention and preventive care. The concept of "atopic march" describes the progression from one allergic condition to another, often following predictable patterns.

### Problem Statement
Healthcare providers need predictive tools to identify patients at risk of developing new food allergies and estimate when these allergies might manifest. This is a critical healthcare challenge because:

- **Early Detection Saves Lives**: Food allergies can be life-threatening, and early identification allows for preventive measures
- **Healthcare Cost Reduction**: Proactive monitoring is more cost-effective than emergency interventions
- **Quality of Life**: Families can prepare and adapt lifestyles before severe allergic reactions occur
- **Clinical Decision Support**: Helps allergists prioritize patients for testing and follow-up care

### Solution Approach

1. **Risk Assessment**: Predict which patients are likely to develop specific food allergies
2. **Timeline Prediction**: Estimate the age when allergies might manifest
3. **Clinical Integration**: Deploy as a web service for healthcare provider use

The solution uses Random Forest classification for allergy prediction and Linear Regression for age estimation, trained on longitudinal patient data including demographics, existing allergies, and atopic conditions.

### Business Impact
- **For Healthcare Providers**: Evidence-based risk stratification and monitoring schedules
- **For Patients/Families**: Early awareness and preparation for potential allergic conditions
- **For Healthcare Systems**: Optimized resource allocation and preventive care protocols

## Instructions on How to Run the Project

### Prerequisites

#### System Requirements
- Python 3.8 or higher
- Docker (for containerization)
- 4GB RAM minimum
- 2GB free disk space

### Quick Start with Docker (Recommended)

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/allergy-prediction.git
cd allergy-prediction
```

2. **Build and run with Docker:**
```bash
# Build the Docker image
docker build -t allergy-prediction .

# Run the container
docker run -p 9696:9696 allergy-prediction
```

3. **Test the service:**
```bash
# Test prediction endpoint
curl -X POST http://localhost:9696/predict \
  -H "Content-Type: application/json" \
  -d '{
    "gender": "Female",
    "race": "White", 
    "has_milk_allergy": 1,
    "has_egg_allergy": 0,
    "age_start": 2.5,
    "atopic_march_cohort": true
  }'
```

### Local Development Setup

#### 1. Environment Setup
```bash
# Create and activate virtual environment
python -m venv allergy_env
source allergy_env/bin/activate  # On Windows: allergy_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### 2. Data Setup
The dataset is included in the `data/` folder. If you need to download it separately:
```bash
# Download dataset (example - replace with actual source)
wget https://example.com/allergy_data.csv -O data/allergy_data.csv
```

#### 3. Run the Complete Pipeline

**Step 1: Explore the data and train models**
```bash
# Open Jupyter notebook for exploration
jupyter notebook notebook.ipynb
```

**Step 2: Train the final model**
```bash
# Train and save the model
python train.py
```

**Step 3: Start the prediction service**
```bash
# Start Flask web service
python predict.py
```

The service will be available at `http://localhost:9696`

### Project Structure
```
allergy-prediction/
├── README.md                          # This file
├── notebook.ipynb                     # Data exploration and model development
├── train.py                          # Training script
├── predict.py                        # Web service for predictions
├── requirements.txt                   # Python dependencies
├── Pipfile                           # Pipenv dependencies
├── Pipfile.lock                      # Pipenv lock file
├── Dockerfile                        # Container configuration
├── data/
│   └── allergy_data.csv              # Dataset
├── models/
│   ├── random_forest_model.pkl       # Trained classification model
│   └── scaler.pkl                    # Feature scaler
├── src/
│   ├── __init__.py
│   ├── data_preprocessing.py
│   └── feature_engineering.py
└── deployment/
    ├── kubernetes/
    │   ├── deployment.yaml
    │   └── service.yaml
    └── cloud_deploy.py
```

### Environment Management Options

#### Option 1: Using pip and virtualenv
```bash
pip install -r requirements.txt
```

#### Option 2: Using Pipenv (Recommended)
```bash
# Install Pipenv if not already installed
pip install pipenv

# Install dependencies and create virtual environment
pipenv install

# Activate virtual environment
pipenv shell

# Run the project
pipenv run python train.py
```

#### Option 3: Using conda
```bash
# Create environment from environment.yml
conda env create -f environment.yml

# Activate environment
conda activate allergy-prediction
```

### Usage Examples

#### Training a New Model
```bash
# Train with default parameters
python train.py

# Train with custom parameters
python train.py --max_depth 10 --n_estimators 200 --test_size 0.3
```

#### Making Predictions via API
```bash
# Start the service
python predict.py

# Make a prediction
curl -X POST http://localhost:9696/predict \
  -H "Content-Type: application/json" \
  -d '{
    "gender": "Male",
    "race": "Asian",
    "ethnicity": "Non-Hispanic",
    "has_milk_allergy": 1,
    "has_egg_allergy": 1,
    "age_start": 3.0,
    "atopic_march_cohort": true
  }'
```

### Containerization

#### Building the Docker Image
```bash
# Build the image
docker build -t allergy-prediction:latest .

# Run the container
docker run -p 9696:9696 allergy-prediction:latest

# Run with environment variables
docker run -p 9696:9696 -e MODEL_PATH=/app/models allergy-prediction:latest
```

#### Docker Compose (Optional)
```bash
# Run with docker-compose
docker-compose up

# Run in background
docker-compose up -d
```

### Cloud Deployment

#### AWS ECS Deployment
```bash
# Configure AWS CLI
aws configure

# Deploy to ECS
python deployment/deploy_aws.py

# Get service URL
aws ecs describe-services --cluster allergy-prediction --services allergy-service
```

#### Kubernetes Deployment
```bash
# Apply Kubernetes manifests
kubectl apply -f deployment/kubernetes/

# Check deployment status
kubectl get pods

# Get service URL
kubectl get service allergy-prediction-service
```

#### Testing Deployed Service
```bash
# Replace with your deployed URL
export SERVICE_URL="https://your-deployed-service.com"

curl -X POST $SERVICE_URL/predict \
  -H "Content-Type: application/json" \
  -d '{
    "gender": "Female",
    "race": "White",
    "has_milk_allergy": 1,
    "age_start": 2.0
  }'
```

### Troubleshooting

#### Common Issues

1. **Port already in use:**
```bash
# Kill process using port 9696
lsof -ti:9696 | xargs kill
```

2. **Docker build fails:**
```bash
# Clean Docker cache
docker system prune -a
```

3. **Missing dependencies:**
```bash
# Reinstall requirements
pip install --force-reinstall -r requirements.txt
```

4. **Model file not found:**
```bash
# Retrain the model
python train.py
```

### Performance Metrics

- **Classification Accuracy**: >80% for primary food allergies
- **Regression RMSE**: <2.5 years for age prediction
- **API Response Time**: <200ms average
- **Service Uptime**: >99% availability target

### API Documentation

#### Endpoints

**POST /predict**
- **Description**: Predict future allergies for a patient
- **Input**: JSON with patient features
- **Output**: JSON with allergy predictions and confidence scores

**GET /health**
- **Description**: Health check endpoint
- **Output**: Service status

**GET /model/info**
- **Description**: Get model metadata
- **Output**: Model version, training date, performance metrics

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes and add tests
4. Submit a pull request

### License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Service URL**: https://allergy-prediction-service.herokuapp.com/predict

**Demo Video**: See `demo/service_demo.mp4` for interaction examples
