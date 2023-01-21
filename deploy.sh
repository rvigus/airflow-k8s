# build airflow image and load onto cluster
CONFIG_PATH=./dev/config

docker build --no-cache -t local-airflow:latest .
kind load docker-image local-airflow:latest --name airflow-cluster

# kill running port-forward commands
pgrep kubectl | xargs kill -9

# re-install on cluster
helm upgrade --install airflow apache-airflow/airflow -n airflow -f $CONFIG_PATH/values.yaml --debug
