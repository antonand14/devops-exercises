# Exercise 4: ConfigMaps, Environment Variables, and JSON Responses

## Overview

You are given a Python app and Kubernetes manifests that contain intentional bugs.
The app reads a greeting message from an environment variable (injected via a ConfigMap) and returns a JSON response with the message and a running request log.

There are **two bugs** total — one in the Python code and one in the Kubernetes manifest.

---

## New concepts introduced

- **ConfigMap**: a Kubernetes object for storing non-secret configuration as key/value pairs.
- **env injection**: mounting a ConfigMap value as an environment variable inside a container.
- **JSON responses**: building and returning structured data from a Python HTTP server.
- **`os.environ`**: reading environment variables in Python.

---

## Step 1: Write the Python app

Create `app.py`. The app should:

- Import `os`, `json`, and `datetime`.
- Keep a module-level list `request_log = []` to track request timestamps.
- On each GET request:
  - Read the env var `APP_MESSAGE` using `os.environ`.
  - Append the current UTC time (as an ISO string) to `request_log`.
  - Respond with a JSON body containing:
    - `"message"`: the value of `APP_MESSAGE`
    - `"request_number"`: the total number of requests so far
    - `"last_requests"`: the last 3 timestamps from `request_log`
- Listen on port **8080**.

**Introduce this bug deliberately**: read `os.environ["MESSAGE"]` instead of `os.environ["APP_MESSAGE"]`.

---

## Step 2: Write the Dockerfile

Base image `python:3.12-slim`. Copy `app.py`. Run it with Python.

---

## Step 3: Write the Kubernetes manifests

Create `configmap.yaml`, `deployment.yaml`, and `service.yaml`.

**`configmap.yaml`**: define a ConfigMap named `greeter-config` with one key: `MESSAGE: "Hello from Kubernetes"`.

**`deployment.yaml`**: run 1 replica of `greeter:v1` with `imagePullPolicy: Never`. Inject the ConfigMap value into the container as an env var named `APP_MESSAGE`:

```yaml
env:
- name: APP_MESSAGE
  valueFrom:
    configMapKeyRef:
      name: greeter-config
      key: MESSAGE
```

**`service.yaml`**: ClusterIP service mapping port 80 to container port 8080.

---

## Step 4: Build and load the image

```
docker build -t greeter:v1 .
kind load docker-image greeter:v1
```

---

## Step 5: Deploy to the cluster

```
kubectl apply -f configmap.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

---

## Step 6: Observe the failure

Check the pod status:

```
kubectl get pods
```

The pod will be in `CrashLoopBackOff`. Time to debug.

---

## Step 7: Debug the crash

Work through these steps:

1. Check the pod logs — what error do you see?
2. A `KeyError` means the environment variable the code is looking for doesn't exist in the container. What variable is the code asking for?
3. Check what environment variables are actually injected. Describe the pod and look at the `Environment` section:
   ```
   kubectl describe pod <pod-name>
   ```
4. Do you see a mismatch between what the code reads and what the manifest injects?

<details>
<summary>Hint: check pod logs</summary>

```
kubectl logs <pod-name>
```

You should see a Python `KeyError` traceback.
</details>

<details>
<summary>Hint: what to look for in describe</summary>

Look at the `Environment:` section of the container. You'll see `APP_MESSAGE` is set — but the code is asking for `MESSAGE`.
</details>

---

## Step 8: Fix the bug

Fix `app.py` to read `os.environ["APP_MESSAGE"]` instead of `os.environ["MESSAGE"]`.

Rebuild and reload:

```
docker build -t greeter:v2 .
kind load docker-image greeter:v2
```

Update the image in `deployment.yaml` to `greeter:v2`, re-apply, and wait for the rollout:

```
kubectl apply -f deployment.yaml
kubectl rollout status deployment/greeter
```

---

## Step 9: Test the app

Port-forward and curl several times:

```
kubectl port-forward service/greeter 8080:80
curl http://localhost:8080
curl http://localhost:8080
curl http://localhost:8080
```

Each response should be valid JSON. Observe:
- `request_number` increments on each call.
- `last_requests` grows up to 3 entries and then slides (only the last 3 are shown).
- `message` always shows the value from the ConfigMap.

---

## Step 10: Update the ConfigMap (bonus)

Try changing the message in `configmap.yaml` and re-applying it:

```
kubectl apply -f configmap.yaml
```

Does the running pod pick up the change immediately? Why or why not?

<details>
<summary>Hint</summary>
Environment variables are set at container start time. To pick up a ConfigMap change injected via `env`, you need to restart the pod. Try:

```
kubectl rollout restart deployment/greeter
```
</details>

---

When `curl` returns correct JSON with an incrementing `request_number`, you're done. Solution is in `solution/`.
