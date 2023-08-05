# CKAN Cloud Operator

CKAN Cloud operator manages, provisions and configures Ckan Cloud components inside a [Ckan Cloud cluster](https://github.com/ViderumGlobal/ckan-cloud-cluster).

## Install

See [environment.yaml](environment.yaml) for the required system dependencies

Insatll ckan-cloud-operator Python package

```
python3 -m pip install -e .
```

Make sure you are connected to the right Kubernetes cluster from your shell

```
kubectl get nodes
```

Install ckan-cloud-operator custom resource definitions

```
ckan-cloud-operator install-crds
```

View available commands

```
ckan-cloud-operator
```
