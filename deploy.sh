# build airflow image and load onto cluster
docker build --no-cache -t rory-airflow:latest .
kind load docker-image rory-airflow:latest --name airflow-cluster

# kill running port-forward commands
pgrep kubectl | xargs kill -9

# re-install on cluster
helm upgrade --install airflow apache-airflow/airflow -n airflow -f values.yaml --debug
