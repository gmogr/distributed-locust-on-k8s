# Baseline Locust Test

This directory contains a generic, baseline load test configuration. It is intended to be used for initial cluster verification and simple performance benchmarking.

## Files
- **`locustfile.py`**: The Python script defining the user behavior.
- **`requirements.txt`**: List of Python dependencies for this test (currently empty).

## Test Behavior
- **Wait Time**: Simulated users wait between 1 and 3 seconds between tasks.
- **Tasks**:
  - `index_page`: Hits the root path `/` (Weight: 1).

## Usage
To use this test case, generate the `locustfile` ConfigMap pointing to this directory:

```bash
kubectl create configmap locustfile \
  --from-file=locustfile.py=./locustfile/locustfile.py \
  --from-file=requirements.txt=./locustfile/requirements.txt \
  --dry-run=client -o yaml > locustfile.yaml

kubectl apply -f locustfile.yaml
```
