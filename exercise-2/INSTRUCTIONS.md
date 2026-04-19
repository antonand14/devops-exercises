# Exercise 2: Environment-Configured Greeter with ConfigMap

## Overview
Write a Python HTTP server whose response message is controlled by an environment variable.
Configure that variable in Kubernetes using a **ConfigMap** — without rebuilding the image.

---

## Step 1: Write the Python app

Create a file called `app.py`.

- Read an environment variable called `GREETING`. If it is not set, fall back to the default value `"Hello, World!"`.
- On a GET request to any path, respond with the value of `GREETING` as plain text.
- Listen on port **8080**.

<details>
<summary>Hint: reading environment variables</summary>
Use `os.environ.get("GREETING", "Hello, World!")` — remember to `import os`.
</details>

<details>
<summary>Hint: HTTP server structure</summary>
Same pattern as Exercise 1: `HTTPServer` + `BaseHTTPRequestHandler`. Store the env var in a module-level variable so it's read once at startup.
</details>

---

## Step 2: Write the Dockerfile

Same structure as Exercise 1 — base image `python:3.12-slim`, copy `app.py`, run it with Python on startup.

---

## Step 3: Build and load the image

Tag the image `greeter:v1` and load it into your local cluster.

<details>
<summary>Hint</summary>

```
docker build -t greeter:v1 .
kind load docker-image greeter:v1
```
</details>

---

## Step 4: Write the Kubernetes manifests

Create three files: `configmap.yaml`, `deployment.yaml`, and `service.yaml`.

**configmap.yaml** should:
- Create a `ConfigMap` named `greeter-config`.
- Define a key `GREETING` with the value `"Greetings from a ConfigMap!"`.

**deployment.yaml** should:
- Create a `Deployment` named `greeter` running `greeter:v1`.
- Inject **all keys** from the ConfigMap as environment variables using `envFrom`.
- Expose port 8080.

**service.yaml** should:
- Expose the deployment on port 80, routing to container port 8080.

<details>
<summary>Hint: envFrom syntax</summary>

```yaml
envFrom:
- configMapRef:
    name: greeter-config
```

This goes under the container spec, at the same level as `image` and `ports`.
</details>

---

## Step 5: Deploy to the cluster

Apply all three manifests. Check that the pod reaches `Running` state.

---

## Step 6: Test it

Port-forward the service and curl it. You should see `Greetings from a ConfigMap!`.

---

## Step 7: Update the greeting without rebuilding

1. Edit `configmap.yaml` — change the `GREETING` value to something new.
2. Apply the updated ConfigMap.
3. The pod won't pick up the change automatically — trigger a rolling restart.
4. Port-forward again and confirm the new message appears.

<details>
<summary>Hint: why doesn't it update automatically?</summary>
Environment variables are set at pod startup. Updating a ConfigMap doesn't restart existing pods. You need to trigger a new rollout.
</details>

<details>
<summary>Hint: rolling restart command</summary>

```
kubectl rollout restart deployment/greeter
```
</details>

---

When curl returns your updated greeting, you're done. Solution is in `solution/`.
