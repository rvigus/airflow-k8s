# airflow-k8s
local airflow running on kubernetes


1) run ./init.sh to create the cluster and configure persistent logging
2) run ./deploy.sh to build airflow image, load these into nodes on the cluster.
3) run ./expose.sh to expose webserver container at localhost:8080




Setting up pycharm
1) `mkvirtualenv airflow-k8s -p $path_to_python39`
2) `pip install requirements-dev.txt`
3) 