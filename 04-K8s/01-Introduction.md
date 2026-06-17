# 📘 Kubernetes — Introduction: Architecture & Functions

---

## 📑 Table of Contents

1. [What is Kubernetes?](#1-what-is-kubernetes)
   - 1.1 [The Problem it Solves](#11-the-problem-it-solves)
   - 1.2 [Alternatives & Why Kubernetes Wins](#12-alternatives--why-kubernetes-wins)
2. [Cluster Architecture](#2-cluster-architecture)
   - 2.1 [Control Plane Components](#21-control-plane-components)
   - 2.2 [Node (Data Plane) Components](#22-node-data-plane-components)
   - 2.3 [Cluster Add-ons](#23-cluster-add-ons)
3. [Containers in Kubernetes](#3-containers-in-kubernetes)
   - 3.1 [Why Containers?](#31-why-containers)
   - 3.2 [Containers Inside Pods](#32-containers-inside-pods)
   - 3.3 [Container Lifecycle](#33-container-lifecycle)
   - 3.4 [Container Runtimes & CRI](#34-container-runtimes--cri)
4. [Core Kubernetes Objects](#4-core-kubernetes-objects)
   - 4.1 [Object Model: Spec & Status](#41-object-model-spec--status)
   - 4.2 [Defining Objects — YAML Manifests](#42-defining-objects--yaml-manifests)
   - 4.3 [Required Fields in Every Manifest](#43-required-fields-in-every-manifest)
   - 4.4 [Server-Side Field Validation](#44-server-side-field-validation)
5. [Object Management Techniques](#5-object-management-techniques)
   - 5.1 [Imperative Commands](#51-imperative-commands)
   - 5.2 [Imperative Object Configuration](#52-imperative-object-configuration)
   - 5.3 [Declarative Object Configuration](#53-declarative-object-configuration)
6. [Naming, Labeling & Organizing Objects](#6-naming-labeling--organizing-objects)
   - 6.1 [Names and UIDs](#61-names-and-uids)
   - 6.2 [Labels and Selectors](#62-labels-and-selectors)
   - 6.3 [Namespaces](#63-namespaces)
   - 6.4 [Field Selectors](#64-field-selectors)
   - 6.5 [Annotations](#65-annotations)
7. [Object Relationships & Lifecycle Control](#7-object-relationships--lifecycle-control)
   - 7.1 [Finalizers](#71-finalizers)
   - 7.2 [Owners and Dependents](#72-owners-and-dependents)
   - 7.3 [Recommended Labels](#73-recommended-labels)
8. [Storage Versions & API Versioning](#8-storage-versions--api-versioning)
9. [The Kubernetes Philosophy](#9-the-kubernetes-philosophy)
10. [Essential kubectl Commands](#10-essential-kubectl-commands)
11. [Summary](#11-summary)

---

## 1. What is Kubernetes?

Kubernetes (abbreviated **K8s** — because there are 8 letters between the "K" and "s") is an **open-source container orchestration platform** that automates the deployment, scaling, and operational management of containerized applications.

It was originally built by Google, and is now maintained by the **Cloud Native Computing Foundation (CNCF)**.

> **Simple mental model:** Think of Kubernetes as an operating system for your data center. Just like an OS manages processes on a single machine, Kubernetes manages containers across an entire cluster of machines.

---

### 1.1 The Problem it Solves

Running one container on one machine is easy. Running hundreds of containers across dozens of machines is not. Here's what breaks without an orchestrator:

| Challenge | Without K8s | With K8s |
|---|---|---|
| Container crashes | Manual restart required | Auto-restarted by kubelet |
| High traffic | Manually spin up containers | Auto-scales via HPA |
| Deploying updates | Downtime or manual coordination | Rolling updates, zero downtime |
| Service discovery | Hardcoded IPs | DNS-based service discovery |
| Resource allocation | Guesswork | Scheduler handles bin-packing |
| Configuration management | Files scattered across servers | ConfigMaps & Secrets in cluster |

---

### 1.2 Alternatives & Why Kubernetes Wins

| Tool | Strength | Limitation |
|---|---|---|
| **Docker Swarm** | Simple, fast setup | Limited ecosystem, fewer features |
| **Apache Mesos** | Handles multi-workload (non-container too) | Complex to operate |
| **HashiCorp Nomad** | Lightweight, works with VMs too | Smaller community |
| **Kubernetes** | Full-featured, cloud-native, CNCF-backed | Steeper learning curve |

**Why teams choose Kubernetes:**
- Massive community and ecosystem (Helm, Operators, service meshes)
- Native support on all major clouds (EKS, GKE, AKS)
- Extensible via **Custom Resource Definitions (CRDs)** and controllers
- Enterprise-grade RBAC, multi-tenancy, audit logging

---

## 2. Cluster Architecture

A Kubernetes cluster is made up of two logical layers:

- **Control Plane** — the brain; makes decisions, stores state, manages the cluster
- **Worker Nodes** — the muscle; run your actual containerized applications inside Pods

```
┌─────────────────────────── Kubernetes Cluster ───────────────────────────┐
│                                                                           │
│   ┌──────────────────── Control Plane ────────────────────┐              │
│   │  kube-apiserver  │  etcd  │  scheduler  │  controller │              │
│   └───────────────────────────────────────────────────────┘              │
│                              │                                            │
│         ┌────────────────────┼────────────────────┐                      │
│         ▼                    ▼                     ▼                      │
│   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                  │
│   │  Worker     │    │  Worker     │    │  Worker     │                  │
│   │  Node 1     │    │  Node 2     │    │  Node 3     │                  │
│   │  [Pod][Pod] │    │  [Pod][Pod] │    │  [Pod]      │                  │
│   └─────────────┘    └─────────────┘    └─────────────┘                  │
└───────────────────────────────────────────────────────────────────────────┘
```

---

### 2.1 Control Plane Components

#### 🔹 kube-apiserver

The **front door** of the entire Kubernetes cluster. Every interaction — from `kubectl` commands to internal controller loops — goes through the API server.

- Exposes the Kubernetes REST API
- Authenticates and authorizes every request
- Validates object manifests before persisting them to etcd
- **Horizontally scalable** — run multiple instances for HA

```bash
# All kubectl commands hit the API server
kubectl get pods  →  HTTP GET /api/v1/namespaces/default/pods
```

---

#### 🔹 etcd

A **distributed, consistent key-value store** that holds the entire state of your cluster — every object, every configuration, every secret.

- Built on the Raft consensus algorithm for strong consistency
- Only the API server communicates with etcd directly
- **Critical:** if etcd data is lost without a backup, your cluster state is gone

> ⚠️ **Instructor Tip:** Always set up automated etcd backups before running production workloads. Use `etcdctl snapshot save` on a schedule.

```bash
# Manually backup etcd
ETCDCTL_API=3 etcdctl snapshot save snapshot.db \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key
```

---

#### 🔹 kube-scheduler

Watches for **newly created Pods that have no node assigned** and selects the best node to run them on.

The scheduler considers:
- **Resource requests vs. available capacity** (CPU, memory)
- **Node affinity / anti-affinity** rules
- **Taints and tolerations**
- **Data locality** (keep Pods near their data)
- **Deadlines and priority classes**

> The scheduler does NOT start Pods — it only decides *where* they should run. The kubelet on the selected node does the actual work.

---

#### 🔹 kube-controller-manager

Runs a set of **controller loops** as a single binary process. Each controller watches the cluster state and makes changes to drive it toward the desired state.

| Controller | Responsibility |
|---|---|
| **Node Controller** | Detects and responds when nodes go unreachable |
| **Job Controller** | Creates Pods for one-off batch tasks, tracks completion |
| **ReplicaSet Controller** | Ensures the correct number of Pod replicas are running |
| **Endpoints Controller** | Populates the Endpoints object (connects Services to Pods) |
| **ServiceAccount Controller** | Creates default service accounts in new namespaces |

> **Key concept:** Controllers follow a **reconciliation loop** — observe current state, compare to desired state, act to close the gap.

---

#### 🔹 cloud-controller-manager *(optional)*

Integrates Kubernetes with cloud-provider APIs. It runs only when Kubernetes is deployed on a cloud platform.

- Provisions **cloud load balancers** when a `Service` of type `LoadBalancer` is created
- Manages **cloud storage volumes**
- Updates node objects with cloud metadata (region, zone, instance type)

Supported providers include AWS, GCP, Azure, OpenStack, and more via vendor plugins.

---

### 2.2 Node (Data Plane) Components

Every worker node runs these three components:

#### 🔹 kubelet

The **primary agent** on each node. It communicates with the API server and ensures the containers described in PodSpecs are running and healthy.

- Watches for Pods assigned to its node
- Pulls container images and starts containers via the container runtime
- Reports node and Pod status back to the control plane
- Runs **liveness and readiness probes** to check container health

> The kubelet does NOT manage containers it did not create via Kubernetes (e.g., containers started with plain `docker run`).

---

#### 🔹 kube-proxy

A **network proxy** running on each node that maintains network rules to implement Kubernetes **Services**.

- Uses the OS packet filtering layer (e.g., iptables or IPVS) to route traffic
- Enables `ClusterIP`, `NodePort`, and `LoadBalancer` service types to function
- Not responsible for Pod-to-Pod networking — that's handled by the CNI plugin (e.g., Calico, Flannel)

---

#### 🔹 Container Runtime

The software that actually **executes containers** on the node. Kubernetes interfaces with runtimes via the **Container Runtime Interface (CRI)**.

Common runtimes:

| Runtime | Notes |
|---|---|
| **containerd** | Default runtime in most modern clusters (used by EKS, GKE) |
| **CRI-O** | Lightweight, built specifically for Kubernetes |
| **Docker Engine** | Deprecated as a K8s runtime since v1.24; use containerd instead |

---

### 2.3 Cluster Add-ons

Add-ons extend cluster capabilities beyond the base components. Most are deployed as Pods managed by Deployments or DaemonSets.

| Add-on | Purpose |
|---|---|
| **CoreDNS** | Provides cluster-wide DNS resolution for Services and Pods |
| **Kubernetes Dashboard** | Web UI for managing and monitoring cluster resources |
| **Metrics Server** | Collects resource usage (CPU/memory) — required by HPA |
| **Cluster Logging** | Centralized log collection (e.g., Fluentd → Elasticsearch) |
| **CNI Plugin** | Handles Pod networking (Calico, Flannel, Cilium, Weave) |

---

## 3. Containers in Kubernetes

### 3.1 Why Containers?

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

### 3.2 Containers Inside Pods

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

### 3.3 Container Lifecycle

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

### 3.4 Container Runtimes & CRI

The **Container Runtime Interface (CRI)** is a plugin API that lets Kubernetes talk to any compatible container runtime — no hard coupling to Docker or any specific vendor.

```
kubectl → kube-apiserver → kubelet → CRI → containerd → container
```

This separation of concerns means:
- Kubernetes can support new runtimes without core changes
- Runtimes can be upgraded independently
- Specialized runtimes (e.g., **gVisor** for sandboxed containers, **Kata Containers** for VM-level isolation) can be plugged in

---

## 4. Core Kubernetes Objects

### 4.1 Object Model: Spec & Status

Every Kubernetes resource is an **object** — a persistent record of intent stored in etcd. All objects share the same fundamental model:

| Field | Description |
|---|---|
| `spec` | **Desired state** — what you want (defined by you) |
| `status` | **Actual state** — what currently exists (reported by Kubernetes) |

The control plane runs a continuous **reconciliation loop**: compare `status` against `spec` and take action to make them match.

**Example:**
```
You set spec.replicas: 3
Status shows 2 Pods running
→ ReplicaSet controller creates 1 more Pod
→ Now status matches spec ✓
```

---

### 4.2 Defining Objects — YAML Manifests

Objects are declared in YAML (or JSON) and submitted to the API server. This is the **declarative** approach — you describe what you want, Kubernetes figures out how to achieve it.

```yaml
# Example: Deployment manifest
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  namespace: default
  labels:
    app: nginx
spec:
  replicas: 2
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.14.2
        ports:
        - containerPort: 80
        resources:
          requests:
            cpu: "100m"
            memory: "128Mi"
          limits:
            cpu: "250m"
            memory: "256Mi"
```

Apply it:

```bash
kubectl apply -f deployment.yaml

# Or directly from a URL
kubectl apply -f https://k8s.io/examples/application/deployment.yaml
```

---

### 4.3 Required Fields in Every Manifest

Every Kubernetes object manifest must include these four fields:

| Field | Example | Purpose |
|---|---|---|
| `apiVersion` | `apps/v1` | Which API group and version to use |
| `kind` | `Deployment` | What type of object to create |
| `metadata` | `name: my-app` | Unique identifier + optional labels/annotations |
| `spec` | *(varies by kind)* | Desired state definition |

To discover which `apiVersion` a resource uses:

```bash
kubectl api-resources
kubectl api-versions
kubectl explain deployment.spec  # deep-dive into any field
```

---

### 4.4 Server-Side Field Validation

Introduced in **Kubernetes v1.25**, server-side validation catches errors before they cause problems.

| Validation Level | Behavior |
|---|---|
| `Strict` | Request rejected on any validation error |
| `Warn` | Warning returned but request accepted |
| `Ignore` | No validation |

```bash
# Default — strict validation enabled
kubectl apply -f manifest.yaml --validate=true

# Warn mode — useful during migration
kubectl apply -f manifest.yaml --validate=warn

# Older clusters (<v1.27) fall back to client-side validation
```

---

## 5. Object Management Techniques

There are three ways to manage Kubernetes objects. Choose based on your team's workflow.

### 5.1 Imperative Commands

Run operations directly — no manifest files required.

```bash
# Create a deployment
kubectl create deployment nginx --image=nginx

# Scale it
kubectl scale deployment nginx --replicas=3

# Expose it
kubectl expose deployment nginx --port=80 --type=NodePort

# Delete it
kubectl delete deployment nginx
```

**✅ Good for:** Quick experiments, one-off tasks, learning  
**❌ Avoid for:** Production environments — no history, hard to track changes

---

### 5.2 Imperative Object Configuration

Work with manifest files, but use imperative commands (`create`, `replace`, `delete`).

```bash
kubectl create -f nginx.yaml
kubectl replace -f nginx.yaml
kubectl delete -f nginx.yaml
```

**✅ Good for:** Teams transitioning to YAML-based workflows  
**❌ Limitation:** `replace` overwrites the entire object — manual merging needed for partial updates

---

### 5.3 Declarative Object Configuration

The **recommended production approach.** Apply a directory of manifests; Kubernetes figures out what to create, update, or delete.

```bash
# Preview changes before applying
kubectl diff -f configs/

# Apply all manifests in a directory
kubectl apply -f configs/

# Apply recursively
kubectl apply -R -f configs/
```

**✅ Good for:** GitOps, CI/CD pipelines, team collaboration, auditing  
**How it works:** Kubernetes stores a `last-applied-configuration` annotation and merges changes intelligently

---

## 6. Naming, Labeling & Organizing Objects

### 6.1 Names and UIDs

Every object has:
- **Name** — unique within a namespace for a given resource type (e.g., two Pods can't both be named `my-pod` in the same namespace)
- **UID** — globally unique across the entire cluster and its lifetime

**Naming constraints:**

| Format | Max Length | Rules |
|---|---|---|
| DNS Subdomain | 253 chars | lowercase, alphanumeric, `-`, `.` |
| DNS Label | 63 chars | lowercase, alphanumeric, `-` (must start/end alphanumeric) |
| Path Segment | — | no `/`, `%`, or `..` |

```yaml
metadata:
  name: nginx-pod-v1    # DNS label format
  namespace: production
```

---

### 6.2 Labels and Selectors

**Labels** are key/value pairs attached to objects. They are the primary way to organize and select groups of objects.

```yaml
metadata:
  labels:
    app: payments-service
    environment: production
    version: "2.3.1"
    tier: backend
```

**Selectors** let controllers and Services filter objects by labels:

```bash
# Equality-based
kubectl get pods -l environment=production,tier=backend

# Set-based
kubectl get pods -l 'environment in (production, staging)'
kubectl get pods -l 'version notin (1.0, 1.1)'

# Existence check
kubectl get pods -l 'canary'          # label exists
kubectl get pods -l '!canary'         # label does not exist
```

Used internally by: `Services`, `Deployments`, `ReplicaSets`, `NetworkPolicies`, `PodAffinity` rules.

---

### 6.3 Namespaces

Namespaces provide **virtual cluster isolation** within a physical cluster. They're ideal for:
- Separating environments (dev / staging / prod) on one cluster
- Multi-team isolation with RBAC and ResourceQuotas
- Avoiding naming conflicts across teams

**Default namespaces:**

| Namespace | Purpose |
|---|---|
| `default` | Where resources go when no namespace is specified |
| `kube-system` | Kubernetes internal components (API server, scheduler, etc.) |
| `kube-public` | Publicly readable; used for cluster info |
| `kube-node-lease` | Holds node heartbeat lease objects |

```bash
# Create and use a namespace
kubectl create namespace team-alpha
kubectl run nginx --image=nginx --namespace=team-alpha
kubectl get pods -n team-alpha

# Set a default namespace for your context
kubectl config set-context --current --namespace=team-alpha
```

> ⚠️ Not all objects are namespaced. Nodes, PersistentVolumes, ClusterRoles, and StorageClasses are cluster-scoped.

```bash
# Check if a resource is namespaced
kubectl api-resources --namespaced=true
kubectl api-resources --namespaced=false
```

---

### 6.4 Field Selectors

Filter objects based on the **values of resource fields** (not labels).

```bash
# Get only Running pods
kubectl get pods --field-selector status.phase=Running

# Get services NOT in the default namespace
kubectl get services --field-selector metadata.namespace!=default

# Chain multiple selectors
kubectl get pods --field-selector status.phase=Running,spec.nodeName=node01

# Works across resource types
kubectl get pods,services --field-selector metadata.namespace=default
```

> Supported fields vary by resource type. Check `kubectl explain <resource>` for what's filterable.

---

### 6.5 Annotations

Annotations attach **arbitrary, non-identifying metadata** to objects. Unlike labels, annotations are not used for selection — they carry richer, unstructured information.

```yaml
metadata:
  annotations:
    # Build information
    build.company.com/git-commit: "a1b2c3d"
    build.company.com/pipeline-id: "1234"
    
    # Operational notes
    kubernetes.io/change-cause: "Updated image to v2.3.1"
    
    # Tool integrations
    prometheus.io/scrape: "true"
    prometheus.io/port: "9090"
```

**Common uses:**
- Storing deployment metadata (git SHA, build ID, CI pipeline URL)
- Configuration for ingress controllers, monitoring tools, service meshes
- `kubectl rollout history` uses the `change-cause` annotation for rollout records

---

## 7. 📘 Kubernetes Image Pull Policy, Tags, and Digests

### 7.1. Image Pull Policy

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

### 7.2. Tags vs Digests

- **Tag**  
  - Human‑readable identifier (e.g., `nginx:1.21`).  
  - Mutable: the same tag can point to different image versions over time.  

- **Digest**  
  - Immutable SHA256 hash of the image content (e.g., `nginx@sha256:abc123...`).  
  - Guarantees exact image version.  

---

### 7.3. Default Behavior with `latest`

- If **no tag** is defined, Kubernetes defaults to `:latest`.  
- When using `:latest`, the **imagePullPolicy** defaults to **Always**.  
- This means the image will be pulled every time, even if it exists locally.  

---

### 7.4. Combined Scenarios

| Scenario | Behavior |
|----------|----------|
| **Tag not defined** (defaults to `latest`) + **imagePullPolicy=Always** | Image is always pulled from registry. |
| **Tag defined** (e.g., `nginx:1.21`) + **digest defined** | Image will not be pulled if already present locally, since digest ensures immutability. |
| **Tag defined only** + **IfNotPresent** | Image pulled only if missing locally. |
| **Digest defined only** | Exact image version is guaranteed; pull depends on policy. |

---

### 7.5. Best Practices

- Avoid using `:latest` in production.  
- Prefer **immutable digests** for reliability.  
- Use **tags** for readability, but pin to specific versions.  
- Combine **tag + digest** for clarity and immutability.  
- Set `imagePullPolicy=IfNotPresent` for stable workloads, `Always` for CI/CD pipelines.  

---


## 8. Object Relationships & Lifecycle Control

### 8.1 Finalizers

Finalizers are **pre-deletion hooks** that prevent an object from being deleted until cleanup is complete.

How they work:
1. You (or a controller) add a finalizer key to `metadata.finalizers`
2. When you delete the object, Kubernetes sets `metadata.deletionTimestamp` instead of deleting immediately
3. The responsible controller performs cleanup, then removes the finalizer key
4. Once `metadata.finalizers` is empty, the object is deleted

```yaml
metadata:
  finalizers:
  - kubernetes.io/pv-protection   # Prevents PV deletion while in use
  - storage.company.com/cleanup   # Custom finalizer for external storage cleanup
```

> ⚠️ If a controller that manages a finalizer crashes, objects can get stuck in `Terminating`. You can force-remove finalizers, but only after verifying cleanup is safe:
> ```bash
> kubectl patch pvc my-pvc -p '{"metadata":{"finalizers":null}}'
> ```

---

### 8.2 Owners and Dependents

Kubernetes tracks parent-child relationships between objects via `ownerReferences`.

```
Deployment → owns → ReplicaSet → owns → Pods
```

```yaml
# Automatically set by controllers — you rarely write this manually
metadata:
  ownerReferences:
  - apiVersion: apps/v1
    kind: ReplicaSet
    name: nginx-rs-abc123
    uid: d9607e19-f88f-11e6-a518-42010a800195
    controller: true
    blockOwnerDeletion: true
```

**Garbage Collection Policies:**

| Policy | Behavior | When to use |
|---|---|---|
| **Foreground** | Owner stays until all dependents are deleted | Ensure clean teardown |
| **Background** | Owner deleted immediately; dependents removed async | Faster deletion |
| **Orphan** | Dependents are kept after owner deletion | Reuse Pods after ReplicaSet deletion |

```bash
# Delete with explicit policy
kubectl delete deployment nginx --cascade=foreground
kubectl delete deployment nginx --cascade=orphan
```

---

### 8.3 Recommended Labels

The `app.kubernetes.io/` label prefix is a **community standard** for tooling interoperability (Helm, dashboards, operators all recognize these).

| Label | Description | Example Value |
|---|---|---|
| `app.kubernetes.io/name` | Application name | `mysql` |
| `app.kubernetes.io/instance` | Unique release instance | `mysql-production` |
| `app.kubernetes.io/version` | Application version | `8.0.32` |
| `app.kubernetes.io/component` | Component within an app | `database`, `cache`, `frontend` |
| `app.kubernetes.io/part-of` | Higher-level application | `wordpress` |
| `app.kubernetes.io/managed-by` | Tool managing this object | `helm`, `argocd` |

```yaml
metadata:
  labels:
    app.kubernetes.io/name: mysql
    app.kubernetes.io/instance: mysql-production
    app.kubernetes.io/version: "8.0.32"
    app.kubernetes.io/component: database
    app.kubernetes.io/part-of: wordpress
    app.kubernetes.io/managed-by: helm
```

---

## 9. Storage Versions & API Versioning

Kubernetes API is **versioned** to allow evolution without breaking existing clients.

**API version stages:**

| Stage | Stability | Example |
|---|---|---|
| `v1` | Stable / GA | `core/v1` (Pods, Services) |
| `v1beta1` | Beta — mostly stable | `apps/v1beta1` |
| `v1alpha1` | Alpha — may change | `policy/v1alpha1` |

**API Groups:**

```bash
kubectl api-versions    # Lists all available API versions
kubectl api-resources   # Lists all resource types with their API groups
```

Common groups:

```
core             → pods, services, configmaps, secrets (no group prefix)
apps/v1          → deployments, statefulsets, daemonsets, replicasets
batch/v1         → jobs, cronjobs
networking.k8s.io/v1  → ingresses, networkpolicies
rbac.authorization.k8s.io/v1 → roles, clusterroles
```

**Storage Versions in etcd:**
- Objects are stored in etcd using a designated **storage version**
- When you use an older API version, the API server transparently converts it to the storage version
- Important for: encryption at rest, API migrations, and CRD versioning

For Custom Resource Definitions (CRDs), you must declare a storage version:

```yaml
versions:
- name: v1
  served: true
  storage: true    # ← only one version can be the storage version
- name: v1beta1
  served: true
  storage: false
```

---

## 10. The Kubernetes Philosophy

Understanding how Kubernetes *thinks* makes you a better operator.

> **Linux says:** *"Everything is a file."*  
> **Kubernetes says:** *"Everything is an API."*

Every resource in Kubernetes — Pods, Services, Deployments, Secrets, even Nodes — is an **API object** with a versioned schema. This consistency means:

- One unified way to create, read, update, and delete any resource (`kubectl`)
- Declarative configuration works identically for all resource types
- Custom resources (CRDs) get the same API treatment as built-in types
- Everything is observable, auditable, and automatable

The **control loop** pattern is equally fundamental:

```
Watch → Analyze → Act → Repeat
```

Every controller in Kubernetes (and every well-written Operator) follows this loop. This is why Kubernetes is so resilient — there's always something watching and correcting drift.

---

## 11. Essential kubectl Commands

```bash
# ── Cluster Exploration ──────────────────────────────────────
kubectl cluster-info                        # View cluster endpoint
kubectl get nodes                           # List all nodes
kubectl describe node <node-name>           # Detailed node info
kubectl top nodes                           # CPU/memory usage per node

# ── API Discovery ─────────────────────────────────────────────
kubectl api-versions                        # List all API versions
kubectl api-resources                       # List all resource types
kubectl explain pod.spec.containers         # Deep-dive into any field

# ── Working with Pods ─────────────────────────────────────────
kubectl get pods -A                         # All pods across all namespaces
kubectl get pods -n kube-system             # Pods in kube-system namespace
kubectl get pods -o wide                    # Shows node assignment + IPs
kubectl describe pod <pod-name>             # Full pod details + events
kubectl logs <pod-name> -c <container>      # Container logs
kubectl exec -it <pod-name> -- /bin/bash    # Shell into a container

# ── Deployments ───────────────────────────────────────────────
kubectl rollout status deployment/my-app    # Watch rollout progress
kubectl rollout history deployment/my-app   # View rollout history
kubectl rollout undo deployment/my-app      # Roll back to previous version

# ── Object Management ─────────────────────────────────────────
kubectl apply -f manifest.yaml              # Create or update
kubectl delete -f manifest.yaml             # Delete from manifest
kubectl diff -f manifest.yaml               # Preview changes
kubectl get all -n <namespace>              # All resources in namespace

# ── Labels & Selectors ────────────────────────────────────────
kubectl get pods -l app=nginx               # Filter by label
kubectl label pod my-pod env=staging        # Add a label
kubectl annotate pod my-pod owner=team-a    # Add an annotation
```

---

## 12. Summary

Here's what you've covered in this section:

| Topic | Key Takeaway |
|---|---|
| **What is K8s** | Open-source orchestrator for containers; manages deployment, scaling, healing |
| **Control Plane** | API server, etcd, scheduler, and controller manager — the brain of the cluster |
| **Worker Nodes** | kubelet + kube-proxy + container runtime — where your apps actually run |
| **Containers** | Packaged in Pods; share network + storage; managed by kubelet via CRI |
| **Object Model** | Spec (desired) vs Status (actual); controllers close the gap |
| **Manifests** | YAML files with apiVersion, kind, metadata, spec — submitted via `kubectl apply` |
| **Labels** | Key/value tags for organizing and selecting objects |
| **Namespaces** | Virtual isolation within a cluster — for teams, environments, or RBAC |
| **Finalizers** | Pre-deletion hooks to ensure safe cleanup |
| **API Versioning** | Stable/beta/alpha; all resources are versioned API objects |
| **Philosophy** | Everything is an API; control loops reconcile desired vs actual state |
