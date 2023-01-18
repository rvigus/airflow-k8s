# create cluster
kind create cluster --name airflow-cluster --config kind-cluster.yaml

docker network connect "kind" "registry"

# create airflow namespace
kubectl create namespace airflow

# setup persistant logging
kubectl apply -f pv.yaml
kubectl get pv -n airflow
kubectl apply -f pvc.yaml
kubectl get pvc -n airflow

# run helm install
helm repo add apache-airflow https://airflow.apache.org
helm repo update
helm install airflow apache-airflow/airflow --namespace airflow --debug
