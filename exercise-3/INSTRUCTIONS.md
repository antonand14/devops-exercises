# Exercise 3: Debug a Broken Deployment

## Overview
You are given a Python app and Kubernetes manifests that contain intentional bugs.
Your job is to deploy everything, observe the failures, and use `kubectl` to find and fix both bugs.

There are **two bugs** total — one in the Python code and one in the Kubernetes manifests.

---

## Step 1: Write the Python app

Create `app.py`. The app should:

- Keep a **request counter** as a module-level integer variable, starting at 0.
- On each GET request, **increment** the counter by 1.
- Respond with the text: `Request count: <n>` where `<n>` is the current count.
- Listen on port **8080**.

**Introduce this bug deliberately** when you write the increment line:

```python
count =+ 1
```

(You'll find out why this is wrong during debugging.)

<details>
<summary>Hint: global variables in Python</summary>
To modify a module-level variable inside a method, you need to declare it with the `global` keyword inside that method: `global count`.
</details>

---

## Step 2: Write the Dockerfile

Base image `python:3.12-slim`. Copy `app.py`. Run it with Python.

---

## Step 3: Build and load the image

Tag it `counter:v1` and load it into your cluster.

---

## Step 4: Write the Kubernetes manifests

Create `deployment.yaml` and `service.yaml`.

**Introduce this bug deliberately** in both files: use port **9090** instead of **8080** for `containerPort` and `targetPort`.

The deployment should run 1 replica of `counter:v1` with `imagePullPolicy: Never`.
The service should map port 80 to the (wrong) container port.

---

## Step 5: Deploy to the cluster

```
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

Check that the pod reaches `Running` state — it will, because a wrong port doesn't crash the container.

---

## Step 6: Test and observe the failure

Port-forward the service to local port 8080 and curl it.

```
kubectl port-forward service/counter 8080:80
curl http://localhost:8080
```

It will hang or return nothing. Time to debug.

---

## Step 7: Debug the manifest bug

Use `kubectl` commands to figure out why the service isn't working.

Work through these steps:

1. Check the pod logs — is the app running?
2. Describe the pod — what port is the container actually listening on?
3. Try port-forwarding **directly to the pod** (bypassing the service) on port 8080. Does that work?
4. If the direct pod forward works but the service doesn't, the issue is in the service/manifest ports.
5. Fix the port mismatch in both `deployment.yaml` and `service.yaml`, re-apply, and test again.

<details>
<summary>Hint: get the pod name</summary>

```
kubectl get pods
```
</details>

<details>
<summary>Hint: check pod logs</summary>

```
kubectl logs <pod-name>
```
</details>

<details>
<summary>Hint: port-forward directly to the pod</summary>

```
kubectl port-forward pod/<pod-name> 8080:8080
```
</details>

<details>
<summary>Hint: describe the service</summary>

```
kubectl describe service counter
```

Look at the `TargetPort` field — does it match what the app actually listens on?
</details>

---

## Step 8: Observe the Python bug

After fixing the port issue, curl the endpoint several times:

```
curl http://localhost:8080
curl http://localhost:8080
curl http://localhost:8080
```

The counter should increase with each request. Does it?

<details>
<summary>Hint: what to look for</summary>
If the count never goes above 1, the increment isn't working correctly. Look closely at the line `count =+ 1`. Is that the same as `count += 1`?
</details>

---

## Step 9: Fix the Python bug and redeploy

1. Fix `app.py`.
2. Rebuild the image as `counter:v2`.
3. Load `counter:v2` into the cluster.
4. Update the image reference in `deployment.yaml` to `counter:v2`.
5. Re-apply the deployment and wait for the rollout to complete.
6. Port-forward and curl several times to confirm the counter increments correctly.

<details>
<summary>Hint: check rollout status</summary>

```
kubectl rollout status deployment/counter
```
</details>

---

When the counter increments correctly on each request, you're done. Solution is in `solution/`.
