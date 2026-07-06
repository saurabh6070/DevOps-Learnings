## 1. Containers in Kubernetes

### 1.1 Why Containers?

Before containers, deploying applications meant wrestling with dependency conflicts, environment inconsistencies, and "works on my machine" problems.

Containers solve this by **packaging the application together with everything it needs** to run:

- Application code
- Runtime (e.g., Node.js, Python interpreter)
- System libraries and dependencies
- Configuration

**Benefits for Kubernetes workloads:**
- **Portability** — runs identically in dev, staging, and production
- **Isolation** — processes and filesystems are separated from the host and each other
- **Efficiency** — share the OS kernel; much lighter than VMs
- **Fast startup** — seconds, not minutes like VMs
- **Immutability** — container images are versioned and don't change at runtime

---

### 1.2 Containers Inside Pods

> **Key rule:** You do not run containers directly in Kubernetes. You define **Pods**, and Pods contain containers.

A **Pod** is the smallest deployable unit in Kubernetes. It wraps one or more tightly coupled containers that:
- Share the **same network namespace** — they communicate via `localhost` and share ports
- Share **storage volumes** — data can be exchanged via mounted volumes
- Are scheduled and scaled **together** on the same node

**When to use multiple containers in one Pod (sidecar pattern):**
- A log collector running alongside your application
- A proxy (like Envoy) injected next to a service
- An init container that prepares data before the main container starts

```yaml
# Example: App container + sidecar log shipper in one Pod
apiVersion: v1
kind: Pod
metadata:
  name: app-with-sidecar
spec:
  containers:
  - name: app
    image: my-app:1.0
    ports:
    - containerPort: 8080
  - name: log-shipper
    image: fluentd:latest
    volumeMounts:
    - name: logs
      mountPath: /var/log/app
  volumes:
  - name: logs
    emptyDir: {}
```

> ⚠️ Pods are **ephemeral** — they are not self-healing. Use Deployments or ReplicaSets to ensure Pod availability.

---

### 1.3 Container Lifecycle

When a Pod is scheduled, here is what happens to each container:

```
1. Image Pull      → kubelet pulls the image from the registry (if not cached)
2. Init Containers → run sequentially before main containers start
3. Container Start → kubelet starts main containers via the runtime
4. Probes          → liveness, readiness, and startup probes begin
5. Running         → container serves traffic / does work
6. Termination     → graceful shutdown on SIGTERM, then SIGKILL after graceperiod
```

**Restart Policies** (defined at the Pod level, not per-container):

| Policy | Behavior |
|---|---|
| `Always` | Restarts container on any exit (default for Deployments) |
| `OnFailure` | Restarts only if container exits with a non-zero code |
| `Never` | Never restarts (used for one-off batch Jobs) |

**Health Probes** — tell Kubernetes when a container is actually ready or broken:

| Probe | Purpose |
|---|---|
| **Liveness Probe** | Is the container alive? If it fails, kubelet kills and restarts the container |
| **Readiness Probe** | Is the container ready to serve traffic? If it fails, removes the Pod from Service endpoints |
| **Startup Probe** | Gives slow-starting containers time to initialize before liveness probes kick in |

```yaml
livenessProbe:
  httpGet:
    path: /healthz
    port: 8080
  initialDelaySeconds: 10
  periodSeconds: 5
```

---

### 1.4 Container Runtimes & CRI

The **Container Runtime Interface (CRI)** is a plugin API that lets Kubernetes talk to any compatible container runtime — no hard coupling to Docker or any specific vendor.

```
kubectl → kube-apiserver → kubelet → CRI → containerd → container
```

This separation of concerns means:
- Kubernetes can support new runtimes without core changes
- Runtimes can be upgraded independently
- Specialized runtimes (e.g., **gVisor** for sandboxed containers, **Kata Containers** for VM-level isolation) can be plugged in

---

2. Init-Container & Multiple Containers in a Pod (Sidecar pattern)

001 -> In a multi-container pod, each container is expected to run a process that stays alive as long as the POD's lifecycle. For example in the multi-container pod that we talked about earlier that has a web application and logging agent, both the containers are expected to stay alive at all times. The process running in the log agent container is expected to stay alive as long as the web application is running. If any of them fails, the POD restarts.
But at times you may want to run a process that runs to completion in a container. For example a process that pulls a code or binary from a repository that will be used by the main web application. That is a task that will be run only  one time when the pod is first created. Or a process that waits  for an external service or database to be up before the actual application starts. That's where initContainers comes in.
An initContainer is configured in a pod like all other containers, except that it is specified inside a initContainers section.
When a POD is first created the initContainer is run, and the process in the initContainer must run to a completion before the real container hosting the application starts. 
You can configure multiple such initContainers as well, like how we did for multi-containers pod. In that case each init container is run one at a time in sequential order.
If any of the initContainers fail to complete, Kubernetes restarts the Pod repeatedly until the Init Container succeeds.
Incase all the PODs after initContainers are running, then Init-Containers goes to terminated state. Also, in the output of PODS, init-Containers are not counted for any POD.

002 -> Yaml file of Init-Container in a POD
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  labels:
    app: myapp
spec:
  containers:
  - name: myapp-container
    image: busybox:1.28
    command: ['sh', '-c', 'echo The app is running! && sleep 3600']
  initContainers:
  - name: init-myservice
    image: busybox:1.28
    command: ['sh', '-c', 'until nslookup myservice; do echo waiting for myservice; sleep 2; done;']
  - name: init-mydb
    image: busybox:1.28
    command: ['sh', '-c', 'until nslookup mydb; do echo waiting for mydb; sleep 2; done;']





---

## 3. 📘 Kubernetes Image Pull Policy, Tags, and Digests

### 3.1. Image Pull Policy

Kubernetes decides when to pull container images based on the **imagePullPolicy** setting:

- **Always**  
  - The image is pulled from the registry every time the Pod starts.  
  - Ensures the latest version is used, but increases startup time and network usage.  

- **IfNotPresent**  
  - The image is pulled only if it is not already present locally.  
  - Faster startup if the image exists on the node.  

- **Never** (rarely used)  
  - The image is never pulled; it must exist locally.  

---

### 3.2. Tags vs Digests

- **Tag**  
  - Human‑readable identifier (e.g., `nginx:1.21`).  
  - Mutable: the same tag can point to different image versions over time.  

- **Digest**  
  - Immutable SHA256 hash of the image content (e.g., `nginx@sha256:abc123...`).  
  - Guarantees exact image version.  

---

### 3.3. Default Behavior with `latest`

- If **no tag** is defined, Kubernetes defaults to `:latest`.  
- When using `:latest`, the **imagePullPolicy** defaults to **Always**.  
- This means the image will be pulled every time, even if it exists locally.  

---

### 3.4. Combined Scenarios

| Scenario | Behavior |
|----------|----------|
| **Tag not defined** (defaults to `latest`) + **imagePullPolicy=Always** | Image is always pulled from registry. |
| **Tag defined** (e.g., `nginx:1.21`) + **digest defined** | Image will not be pulled if already present locally, since digest ensures immutability. |
| **Tag defined only** + **IfNotPresent** | Image pulled only if missing locally. |
| **Digest defined only** | Exact image version is guaranteed; pull depends on policy. |

---

### 3.5. Best Practices

- Avoid using `:latest` in production.  
- Prefer **immutable digests** for reliability.  
- Use **tags** for readability, but pin to specific versions.  
- Combine **tag + digest** for clarity and immutability.  
- Set `imagePullPolicy=IfNotPresent` for stable workloads, `Always` for CI/CD pipelines.  

---
