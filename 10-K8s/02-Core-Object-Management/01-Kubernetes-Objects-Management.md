## 🧩 1. Core Kubernetes Objects

### 1.1 Object Model: Spec & Status

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

### 1.2 Defining Objects — YAML Manifests

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

### 1.3 Required Fields in Every Manifest

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

### 1.4 Server-Side Field Validation

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

## ⚙️ 2. Object Management Techniques

There are three ways to manage Kubernetes objects. Choose based on your team's workflow.

**Sample Pod file for Commands and Arguments:**

```yaml
spec:
  containers:
  - name: test
    image: ubuntu
    command: [ "sleeep 5000" ]
# OR
    command: [ "sleep","5000" ]
# OR
    command: [ "sleep" ]
    args: [ "5000" ]
# OR
    command:
    - "sleep"
    - "5000"
```

**To deploy any object, there are two approaches:**
- **Imperative Method** — Using a command to deploy a Pod or any other resource
- **Declarative Method** — Using a YAML file to deploy a Pod or any other resource

---

### 2.1 Imperative Commands

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

### 2.2 Imperative Object Configuration

Work with manifest files, but use imperative commands (`create`, `replace`, `delete`).

```bash
kubectl create -f nginx.yaml
kubectl replace -f nginx.yaml
kubectl delete -f nginx.yaml
```

**✅ Good for:** Teams transitioning to YAML-based workflows
**❌ Limitation:** `replace` overwrites the entire object — manual merging needed for partial updates

---

### 2.3 Declarative Object Configuration

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

## 🏷️ 3. Naming, Labeling & Organizing Objects

### 3.1 Names and UIDs

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

### 3.2 Labels and Selectors

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

# If we want to remove headings in output of list pods
kubectl get pods --selector 'version notin (1.0, 1.1)' --no-headers | wc -l

# To list pods with all labels
kubectl get all --selector environment=production,tier=backend
```

Used internally by: `Services`, `Deployments`, `ReplicaSets`, `NetworkPolicies`, `PodAffinity` rules.

---

### 3.3 Namespaces

Namespaces provide **virtual cluster isolation** within a physical cluster. They're ideal for:
- Separating environments (dev / staging / prod) on one cluster
- Multi-team isolation with RBAC and ResourceQuotas
- Avoiding naming conflicts across teams

**Change default namespace:**

```bash
kubectl config --help
kubectl config set-context --help
kubectl config set-context --current --namespace=alpha-ns
```

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

### 3.4 Field Selectors

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

### 3.5 Annotations

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

## 🔍 4. JSON Path Expressions & Custom Columns with kubectl

kubectl commands sent to the API server return responses in **JSON format**. kubectl converts this output into tabular format and keeps only relevant information. Although the `-o` option shows more detail, it still won't show everything — this is where **JSON Path queries** come in, to filter and format kubectl output for easy interpretation of large data.

**How to build a JSON Path query in kubectl:**
- Identify the kubectl command → e.g. `kubectl get pods`
- Familiarize yourself with the JSON output → e.g. `kubectl get pods -o json`
- Form the JSON Path query → e.g. `.items[0].spec.containers[0].image`
- Use the JSON Path query with the kubectl command → e.g. `kubectl get pods -o=jsonpath='{ .items[0].spec.containers[0].image }'`

**JSON Path query examples:**

```bash
# Node names in the cluster
kubectl get nodes -o=jsonpath='{ .items[*].metadata.name }'

# Hardware architecture of each node in the cluster (e.g. amd64)
kubectl get nodes -o=jsonpath='{ .items[*].status.nodeInfo.architecture }'

# CPU capacity of each node in the cluster
kubectl get nodes -o=jsonpath='{ .items[*].status.capacity.cpu }'

# Node name + CPU capacity (output not easily readable yet)
kubectl get nodes -o=jsonpath='{ .items[*].metadata.name } { .items[*].status.capacity.cpu }'

# Node name + CPU capacity, formatted with a newline
kubectl get nodes -o=jsonpath='{ .items[*].metadata.name } { "\n" } { .items[*].status.capacity.cpu }'

# Node names in tabular format using custom columns
kubectl get nodes -o=custom-columns=NODE:.metadata.name

# Node name + CPU capacity in tabular format
kubectl get nodes -o=custom-columns=NODE:.metadata.name,CPU:.metadata.status.capacity.cpu
```

**Sorting:**

```bash
kubectl get nodes --sort-by=.metadata.name
```

**Listing using a loop:**

```bash
# Node name + CPU capacity in tabular format, row by row
kubectl get nodes -o=jsonpath='{range .items[*]} {.metadata.name} {"\t"} {.status.capacity.cpu} {"\n"} {end}'
```

---

## 🗂️ 5. Storage Versions & API Versioning

Kubernetes API is **versioned** to allow evolution without breaking existing clients.

In Linux, there's a well-known saying: *"Everything in Linux is a file."*
In Kubernetes, a similar idea applies: *"Everything in Kubernetes is an API."*
Here, API refers to the API version you declare in your YAML manifests. To explore what's available, you can list all API versions and resources with the commands below.

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
core                            → pods, services, configmaps, secrets (no group prefix)
apps/v1                         → deployments, statefulsets, daemonsets, replicasets
batch/v1                        → jobs, cronjobs
networking.k8s.io/v1            → ingresses, networkpolicies
rbac.authorization.k8s.io/v1     → roles, clusterroles
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

## 🔗 6. Object Relationships & Lifecycle Control

### 6.1 Finalizers

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

### 6.2 Owners and Dependents

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

### 6.3 Recommended Labels

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

### 6.4 🩺 Liveness, Readiness & Startup Probes

#### 💓 Liveness Probe
Checks whether a container is **still running properly**.

- If it fails, the kubelet **restarts** the container.
- Use it to recover from deadlocks or stuck processes.
- Example: an app that's running but stuck won't serve traffic — a liveness probe catches this.

#### ✅ Readiness Probe
Checks whether a container is **ready to receive traffic**.

- If it fails, the Pod is **removed from Service endpoints** (no restart).
- Use it during startup, warm-up, or temporary dependency issues.
- Example: an app waiting on a DB connection shouldn't get traffic yet.

#### 🚀 Startup Probe
Checks whether a **slow-starting container** has finished initializing.

- Disables liveness/readiness checks until it succeeds, avoiding premature restarts.
- Use for apps with long boot times (legacy apps, large cache warm-up).
- Once it succeeds once, it's never checked again.

#### 🔍 Probe Mechanisms
- **HTTP GET** — success on 2xx/3xx response
- **TCP Socket** — success if port is open
- **Exec Command** — success if command exits with `0`

#### ⚙️ Key Fields
`initialDelaySeconds`, `periodSeconds`, `timeoutSeconds`, `failureThreshold`, `successThreshold`

#### 📌 Quick Rule
- **Startup → "Has it finished booting? Wait before checking anything else."**
- **Liveness → "Is it alive? Restart if not."**
- **Readiness → "Is it ready? Pause traffic if not."**


---

## 💡 7. The Kubernetes Philosophy

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

## 💻 8. Essential kubectl Commands

```bash
# ── Autocompletion ─────────────────────────────────────────────
alias k=kubectl
complete -F __start_kubectl k                # Enable autocompletion for short form 'k'
source <(kubectl completion bash)            # Enable autocompletion

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

## 📋 9. Summary

Here's what you've covered so far:

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
