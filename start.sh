CONFIG_PATH=$PWD/dev/config
REGISTRY_NAME='local-registry'

# Create cluster
kind create cluster --name airflow-cluster --config $CONFIG_PATH/kind-cluster.yaml

# create airflow namespace
kubectl create namespace airflow

# PV is storage that has been provisioned for use within the cluster.
# PVC is a request for storage made by an application running in a pod.
# Using this we provide resources to persist logs
kubectl apply -f $CONFIG_PATH/pv-volume.yaml
kubectl apply -f $CONFIG_PATH/pv-claim.yaml

# run helm install
helm repo add apache-airflow https://airflow.apache.org
helm repo update
# 1.7.0 helm chart == airflow 2.4.1
helm install airflow apache-airflow/airflow --version 1.7.0 --namespace airflow --debug

# create local image registry
if ! docker container ls -f "status=running" | grep -q $REGISTRY_NAME; then
  docker run -d --restart=always -p 5000:5000 --name "$REGISTRY_NAME" --network kind registry:2
fi


# spin up localstack
LOCALSTACK_NAME='my_localstack'
if ! docker container ls -f "status=running" | grep -q $LOCALSTACK_NAME; then
  docker run --rm -it -d -p 4566:4566 -p 4510-4559:4510-4559 --network kind --name localstack/localstack
  sleep 10

  # set keys
  aws configure set aws_access_key_id test --profile localstack
  aws configure set aws_secret_access_key test --profile localstack
  aws configure set aws_default_region us-east-1 --profile localstack

  # Create a bucket called data
  aws --endpoint-url=http://localhost:4566 --profile localstack s3 mb s3://data

fi


# run deploy script
./deploy.sh
