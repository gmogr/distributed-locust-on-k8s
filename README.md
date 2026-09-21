# Distributed Locust on GKE

This repository contains configuration files to run a distributed load test in Kubernetes (GKE) without needing a custom Docker image.

## Key Features
- **Official Image**: Uses the official [locustio/locust](https://hub.docker.com/r/locustio/locust/) image.
- **Dynamic Dependencies**: Automatically installs Python packages from `requirements.txt` at runtime via shell logic in the deployment.
- **Flexible Scripts**: Locustfiles are managed via ConfigMaps, allowing for quick updates without rebuilding images.
- **GKE Optimized**: Tailored for Google Kubernetes Engine with easy cluster creation and connection steps.

## Components
- **[locust.yaml](./locust.yaml)**: A single manifest containing the Master Deployment, Worker Deployment, and the Service for internal communication.
- **[locustfile/](./locustfile/)**: Directory containing the Python load test logic (`locustfile.py`) and its dependencies (`requirements.txt`).

---

## 1. Prerequisites & Environment Setup

Set your environment variables:
```bash
export PROJECT_ID=<GCP_PROJECT_ID>
export REGION=<GCP_REGION>
```

Create a GKE cluster (if you don't have one):
```bash
gcloud container clusters create locust-test \
--enable-private-nodes \
--enable-ip-alias \
--shielded-secure-boot \
--enable-shielded-nodes \
--shielded-integrity-monitoring \
--no-enable-master-authorized-networks \
--machine-type=n2-standard-4 \
--enable-dns-access \
--region=${REGION} \
--project=${PROJECT_ID}
```

Connect to the cluster:
```bash
gcloud container clusters get-credentials locust-test --region ${REGION} --project ${PROJECT_ID} --dns-endpoint
```

---

## 2. Configuration & Deployment

### Step A: Create the Locustfile ConfigMap
Generate the ConfigMap from your local script directory. You can modify the `locustfile.py` and `requirements.txt` files to fit your specific test case before running the command below. This keeps your Python code and dependencies separate from the Kubernetes YAML.

```bash
# Create the ConfigMap from your local files:
kubectl create configmap locustfile \
  --from-file=locustfile.py=./locustfile/locustfile.py \
  --from-file=requirements.txt=./locustfile/requirements.txt \
  --dry-run=client -o yaml > locustfile.yaml

kubectl apply -f locustfile.yaml
```

### Step B: Deploy Locust Components
Deploy the Master, Service, and Workers:
```bash
kubectl apply -f locust.yaml
```

---

## 3. Usage & Scaling

### Access the Web UI
Port-forward to the master node:
```bash
kubectl port-forward service/locust-master 8080:8089
```
Then open `http://localhost:8089` in your browser. If using [Google Cloud Shell](https://docs.cloud.google.com/shell/docs/using-cloud-shell), use the [Web Preview](https://docs.cloud.google.com/shell/docs/using-web-preview) button.

### Injecting Environment Variables
If your test requires additional parameters, you can inject environment variables into the workers:

```bash
kubectl set env deployment/locust-worker <ENV_VAR_NAME>=<ENV_VAR_VALUE>
```

### Scaling Workers
Increase the number of workers to generate more load:
```bash
kubectl scale deployment locust-worker --replicas=10
```

---

## 4. Maintenance & Cleanup

### Updating Scripts
After modifying `locustfile.py`, recreate the ConfigMap and restart the workers to pick up changes:
```bash
kubectl apply -f locustfile.yaml
kubectl rollout restart deployment/locust-worker
```

### Checking Logs
Monitor the worker logs to verify dependency installation and test execution:
```bash
kubectl logs -l app=locust-worker
```

### Cleanup
To remove the Locust deployment and the GKE cluster:
```bash
# Remove Kubernetes resources
kubectl delete -f locust.yaml
kubectl delete configmap locustfile

# Delete GKE cluster (Warning: this deletes the infrastructure)
gcloud container clusters delete locust-test --region ${REGION}
```
