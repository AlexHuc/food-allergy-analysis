# Use lightweight base image
FROM python:3.12-slim

# Install Pipenv
RUN pip install pipenv

# Set working directory
WORKDIR /app

# Copy Pipenv files first for dependency caching
COPY ["deployment/flask/Pipfile", "deployment/flask/Pipfile.lock", "./"]

# Install project dependencies system-wide (no virtualenv inside container)
RUN pipenv install --deploy --system

# Copy model files and app code
RUN mkdir -p ./model
COPY ["deployment/flask/predict.py", "./"]
COPY ["models/model_xgb_class_eda=0.05_max_depth=6_min_child_weight=30.bin", "./models/"]
COPY ["models/model_xgb_reg_eda=0.05_max_depth=6_min_child_weight=30.bin", "./models/"]

# Expose port
EXPOSE 9696

# Run the Flask app with Gunicorn
ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:9696", "predict:app"]
