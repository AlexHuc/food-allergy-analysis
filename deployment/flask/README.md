pip install pipenv
pipenv install xgboost flask gunicorn


docker build -t asthma-predictor -f deployment/flask/Dockerfile .
docker run -it --rm -p 9696:9696 asthma-predictor