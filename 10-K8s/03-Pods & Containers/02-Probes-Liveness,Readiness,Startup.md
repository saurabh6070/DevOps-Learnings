# 🩺 Liveness, Readiness & Startup Probes

## 💓 Liveness Probe
Checks whether a container is **still running properly**.

- If it fails, the kubelet **restarts** the container.
- Use it to recover from deadlocks or stuck processes.

- Example 1 : - A basic HTTP probe for simple apps.
```
apiVersion: v1
kind: Pod
metadata:
  name: basic-liveness-pod
spec:
  containers:
  - name: myapp
    image: nginx:latest
    ports:
    - containerPort: 80
    livenessProbe:
      httpGet:
        path: /
        port: 80
      initialDelaySeconds: 5
      periodSeconds: 10
```

httpGet: Sends an HTTP GET request to / on port 80.
initialDelaySeconds: Waits 5 seconds before starting checks.
periodSeconds: Runs the probe every 10 seconds.

- Example 2 : - A complex exec probe with custom thresholds for fine-grained control.
```
apiVersion: v1
kind: Pod
metadata:
  name: advanced-liveness-pod
spec:
  containers:
  - name: myapp
    image: busybox:latest
    args:
    - /bin/sh
    - -c
    - "while true; do sleep 30; done"
    livenessProbe:
      exec:
        command:
        - sh
        - -c
        - |
          if [ -f /tmp/healthy ]; then
            exit 0
          else
            exit 1
          fi
      initialDelaySeconds: 10
      periodSeconds: 5
      timeoutSeconds: 2
      failureThreshold: 3
      successThreshold: 1
```

exec: Runs a shell command inside the container.
The probe checks if /tmp/healthy exists. If not, it fails.
timeoutSeconds: Probe must finish within 2 seconds.
failureThreshold: After 3 consecutive failures, Kubernetes restarts the container.
successThreshold: One success is enough to mark it healthy again.


## ✅ Readiness Probe
Checks whether a container is **ready to receive traffic**.

- If it fails, the Pod is **removed from Service endpoints** (no restart).
- Use it during startup, warm-up, or temporary dependency issues.
- Example 1 : - Check if the container is ready to serve traffic by responding to HTTP requests.
```
apiVersion: v1
kind: Pod
metadata:
  name: basic-readiness-pod
spec:
  containers:
  - name: myapp
    image: nginx:latest
    ports:
    - containerPort: 80
    readinessProbe:
      httpGet:
        path: /
        port: 80
      initialDelaySeconds: 5
      periodSeconds: 10
```

httpGet: Sends an HTTP GET request to / on port 80.
initialDelaySeconds: Waits 5 seconds before starting checks.
periodSeconds: Runs the probe every 10 seconds.
If the probe fails, the pod is marked not ready and removed from Service endpoints.

- Example 2 : - 
```
apiVersion: v1
kind: Pod
metadata:
  name: advanced-readiness-pod
spec:
  containers:
  - name: myapp
    image: busybox:latest
    args:
    - /bin/sh
    - -c
    - "while true; do sleep 30; done"
    readinessProbe:
      tcpSocket:
        port: 8080
      exec:
        command:
        - sh
        - -c
        - |
          if curl -s http://localhost:8080/healthz | grep "ready"; then
            exit 0
          else
            exit 1
          fi
      initialDelaySeconds: 15
      periodSeconds: 5
      timeoutSeconds: 3
      failureThreshold: 5
      successThreshold: 2
```

tcpSocket: Ensures port 8080 is open.
exec: Runs a shell command inside the container to check /healthz endpoint for "ready".
timeoutSeconds: Probe must finish within 3 seconds.
failureThreshold: After 5 consecutive failures, pod is marked not ready.
successThreshold: Requires 2 consecutive successes before marking pod ready again.



## 🚀 Startup Probe
Checks whether a **slow-starting container** has finished initializing.

- Disables liveness/readiness checks until it succeeds, avoiding premature restarts.
- Use for apps with long boot times (legacy apps, large cache warm-up).
- Once it succeeds once, it's never checked again.

- Example 1 :- HTTP Startup Probe
```
apiVersion: v1
kind: Pod
metadata:
  name: basic-startup-pod
spec:
  containers:
  - name: myapp
    image: nginx:latest
    ports:
    - containerPort: 80
    startupProbe:
      httpGet:
        path: /
        port: 80
      failureThreshold: 30
      periodSeconds: 10
```

httpGet: Sends an HTTP GET request to / on port 80.
failureThreshold: 30 → allows up to 30 failed attempts.
periodSeconds: 10 → checks every 10 seconds.
This means the container has up to 5 minutes (30 × 10s) to start before being killed.


- Example 2 :- Exec Startup Probe with Long Initialization
```
apiVersion: v1
kind: Pod
metadata:
  name: advanced-startup-pod
spec:
  containers:
  - name: myapp
    image: busybox:latest
    args:
    - /bin/sh
    - -c
    - "sleep 200; touch /tmp/started; tail -f /dev/null"
    startupProbe:
      exec:
        command:
        - sh
        - -c
        - |
          if [ -f /tmp/started ]; then
            exit 0
          else
            exit 1
          fi
      initialDelaySeconds: 5
      periodSeconds: 10
      timeoutSeconds: 3
      failureThreshold: 40
```

exec: Runs a shell command inside the container.
Checks if /tmp/started exists (created after 200s).
failureThreshold: 40 × periodSeconds: 10s = 400s → gives the app ~6.5 minutes to finish initialization.
If the probe succeeds, Kubernetes switches to liveness probe and readiness probe checks.


## 🔍 Probe Mechanisms
- **HTTP GET** — success on 2xx/3xx response
- **TCP Socket** — success if port is open
- **Exec Command** — success if command exits with `0`

## ⚙️ Key Fields
`initialDelaySeconds`, `periodSeconds`, `timeoutSeconds`, `failureThreshold`, `successThreshold`

## 📌 Quick Rule
- **Startup → "Has it finished booting? Wait before checking anything else."**
- **Liveness → "Is it alive? Restart if not."**
- **Readiness → "Is it ready? Pause traffic if not."**
