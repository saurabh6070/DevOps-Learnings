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
