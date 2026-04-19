# Exercise 1: Hello Kubernetes

## Overview
Write a simple HTTP server in Python, containerize it with Docker, and deploy it to a Kubernetes cluster.

---

## Step 1: Write the Python app

Create a file called `app.py`.

- Import the standard library modules needed to run an HTTP server (no third-party packages needed).
- Create an HTTP request handler that responds to GET requests with the plain text message:
  `Hello from Kubernetes!`
- The server should listen on port **8080**.
- Run the server when the script is executed.

<details>
<summary>Hint: which module?</summary>
Look into Python's built-in `http.server` module. You'll need `HTTPServer` and `BaseHTTPRequestHandler`.
</details>

<details>
<summary>Hint: responding to GET requests</summary>
Override the `do_GET` method in your handler class. Call `self.send_response(200)`, then `self.end_headers()`, then write your response body with `self.wfile.write(b"your message")`.
</details>

---

## Step 2: Write the Dockerfile

Create a file called `Dockerfile` in the same directory.

- Use `python:3.12-slim` as the base image.
- Set the working directory inside the container to `/app`.
- Copy `app.py` into the container.
- Set the default command to run `app.py` with Python.

<details>
<summary>Hint: Dockerfile instructions</summary>
The instructions you need are: `FROM`, `WORKDIR`, `COPY`, and `CMD`.
</details>

---

## Step 3: Build the Docker image

Build the image and tag it as `hello-k8s:v1`.

<details>
<summary>Hint: build command</summary>

```
docker build -t hello-k8s:v1 .
```
</details>

<details>
<summary>Hint: using a local cluster (kind/minikube)</summary>
Images built on your host are not automatically available inside the cluster.

- **kind**: `kind load docker-image hello-k8s:v1`
- **minikube**: run `eval $(minikube docker-env)` before building, then build normally.
</details>

---

## Step 4: Write the Kubernetes manifests

Create two files: `deployment.yaml` and `service.yaml`.

**deployment.yaml** should:
- Create a `Deployment` named `hello-k8s`.
- Run 1 replica of your container image `hello-k8s:v1`.
- Set `imagePullPolicy: Never` (so it uses the locally loaded image).
- Expose port 8080 on the container.

**service.yaml** should:
- Create a `Service` named `hello-k8s`.
- Route traffic to pods with the label `app: hello-k8s`.
- Map port 80 on the service to port 8080 on the container.
- Use type `ClusterIP`.

<details>
<summary>Hint: selector and labels must match</summary>
The `selector` in the Service and the `selector.matchLabels` in the Deployment must use the same label key/value as the `labels` on the pod template.
</details>

---

## Step 5: Deploy to the cluster

Apply both manifest files using `kubectl`.

<details>
<summary>Hint</summary>

```
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```
</details>

---

## Step 6: Verify it works

1. Check that your pod is in `Running` state.
2. Forward a local port to the service.
3. Send a GET request and confirm you receive `Hello from Kubernetes!`.

<details>
<summary>Hint: check pod status</summary>

```
kubectl get pods
```
</details>

<details>
<summary>Hint: port forwarding</summary>

```
kubectl port-forward service/hello-k8s 8080:80
```

Then in another terminal: `curl http://localhost:8080`
</details>

<details>
<summary>Hint: pod not running?</summary>
Run `kubectl describe pod <pod-name>` and look at the **Events** section at the bottom for error messages.
</details>

---

When curl returns `Hello from Kubernetes!` you're done. Check the solution file if you got stuck: `solution/`.
