WORKDIR=$HOME/repos-personal/airflow-k8s
CONFIG_PATH=$WORKDIR/dev/config
REGISTRY_NAME='local-registry'

# Create cluster
kind create cluster --name airflow-cluster --config $CONFIG_PATH/kind-cluster.yaml

# create airflow namespace
kubectl create namespace airflow

# setup persistant logging
echo $CONFIG_PATH/pv.yaml
echo $CONFIG_PATH/pvc.yaml

kubectl apply -f $CONFIG_PATH/pv.yaml
kubectl get pv -n airflow
kubectl apply -f $CONFIG_PATH/pvc.yaml
kubectl get pvc -n airflow

# run helm install
helm repo add apache-airflow https://airflow.apache.org
helm repo update
helm install airflow apache-airflow/airflow --namespace airflow --debug

# create local image registry
running="$(docker inspect -f '{{.State.Running}}' "${REGISTRY_NAME}" 2>/dev/null || true)"
if [ "${running}" != 'true' ]; then
  docker run -d --restart=always -p "5000:5000" --name "${REGISTRY_NAME}" --network kind registry:2
fi

# run deploy script
./deploy.sh
