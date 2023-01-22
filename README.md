# Airflow running on K8's

## Table of contents
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Usage](#usage)
* [Whats next](#whats-next)

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development. 

### Prerequisites
- [Docker](https://www.docker.com/products/docker-desktop/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl-macos/#install-with-homebrew-on-macos)
- [kind](https://kind.sigs.k8s.io/docs/user/quick-start/#installation)
- [helm](https://helm.sh/docs/intro/install/#from-homebrew-macos)
- Your preferred method for creating/managing virtual environments

###  Usage
Running ``./start.sh`` will create your K8's cluster and install Airflow via helm. We also spin up  
local docker registry, this is where we push our images to be run via KubernetesPodOperator.

`./expose.sh` can be used to expose the airflow webserver so we can connect to the UI via `localhost:8080` 

`.deploy.sh` can be used to rebuild and deploy the airflow image (so code changes are reflected to the cluster).

To clean up the kubernetes cluster run `./stop.sh`.

### Local IDE
You'll want to be able to run/test code locally via an IDE (albeit in a limited way). To do so, create a virtualenv for the project and once activated run
`pip install -r requirements-dev.txt`. This will install the same packages used in the Airflow image. 

## Whats next?
Rather than re-running `./deploy.sh` everytime we want to test changes, wouldn't it be nice if this was handled automatically for us? 
One option is  [skaffold](https://skaffold.dev/) 
which is a tool that facilitates continuous development for container based and K8's applications.
