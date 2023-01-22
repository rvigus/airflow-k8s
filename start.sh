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
helm install airflow apache-airflow/airflow --namespace airflow --debug

# create local image registry
if ! docker container ls -f "status=running" | grep -q $REGISTRY_NAME; then
  docker run -d --restart=always -p 5000:5000 --name "$REGISTRY_NAME" --network kind registry:2
fi

# run deploy script
./deploy.sh
