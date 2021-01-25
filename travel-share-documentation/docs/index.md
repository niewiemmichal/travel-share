# Welcome to TravelShare

For projects' source codes please visit:<br/>
[server source](https://github.com/niewiemmichal/travel-share) <br/>
[website source](https://github.com/niewiemmichal/travel-share-ui)


## Deployment services

This section is related to deploying travel-share services to Kubernetes cluster running on Google Cloud Platform.

## Requirements

To deploy travel-share services the latest version of below packages is required.

* [terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli)
* [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
* [helm](https://helm.sh/docs/intro/install/)
* [gcloud](https://cloud.google.com/sdk/gcloud)
* [istioctl](https://istio.io/latest/docs/ops/diagnostic-tools/istioctl/)

## Creating required infrastructure

Go to the `infrastructure` directory and run below commands. Fill all required variables.

```bash
terraform init
terraform apply
```

## Authorizing to Kubernetes cluster

To get access to created Kubernetes cluster run below commands.

```bash
gcloud init
gcloud auth application-default login
gcloud container clusters get-credentials <GCP_PROJECT_ID> --zone us-central1-a
```

## Deploying cert-manager and Istio

Go to the `kubernetes` directory and run below commands.

```bash
kubectl apply -f namespace.yaml
helm install --namespace cert-manager cert-manager jetstack/cert-manager
kubectl apply -f cert-manager/namespace.yaml
kubectl apply -f istio/certificate.yaml
istioctl install -n istio-system -f istio-operator.yaml --revision 1-8
kubectl apply -f istio/gateway.yaml
```

## Deploying travelshare services

Go to the `kubernetes` directory fill `values-*.yaml` files properly and create `values-backend.secret.yaml` file with below content.

```yaml
sql:
  password: <DB_PASSWORD>
django:
  secretKey: <DJANGO_SECRET_KEY>
```

Then run below commands.

```bash
helm upgrade --install --namespace travel-share -f values-backend.yaml -f values-backend.secret.yaml travel-share ./travel-share
helm upgrade --install --namespace travel-share -f values-frontend.yaml travel-share-ui ./travel-share-ui
```
