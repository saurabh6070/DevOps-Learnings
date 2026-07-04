# ☸️ DevSecOps — Kubernetes Security

---

## 📑 Table of Contents

1. [Why Kubernetes Security Matters](#1-why-kubernetes-security-matters)
   - 1.1 [K8s Security Threat Surface](#11-k8s-security-threat-surface)
   - 1.2 [K8s Security Checklist at a Glance](#12-k8s-security-checklist-at-a-glance)
2. [Namespaces — Isolation and Multi-Tenancy](#2-namespaces--isolation-and-multi-tenancy)
   - 2.1 [Why Namespaces Matter for Security](#21-why-namespaces-matter-for-security)
   - 2.2 [Creating Namespaces](#22-creating-namespaces)
   - 2.3 [Resource Quotas — Limiting CPU and Memory](#23-resource-quotas--limiting-cpu-and-memory)
   - 2.4 [LimitRange — Default Resource Limits per Pod](#24-limitrange--default-resource-limits-per-pod)
3. [RBAC — Role-Based Access Control](#3-rbac--role-based-access-control)
   - 3.1 [RBAC Core Concepts](#31-rbac-core-concepts)
   - 3.2 [Service Accounts](#32-service-accounts)
   - 3.3 [Roles and RoleBindings — Namespace Scoped](#33-roles-and-rolebindings--namespace-scoped)
   - 3.4 [ClusterRoles and ClusterRoleBindings — Cluster Scoped](#34-clusterroles-and-clusterrolebindings--cluster-scoped)
   - 3.5 [RBAC Best Practices](#35-rbac-best-practices)
4. [Network Policies](#4-network-policies)
   - 4.1 [Default K8s Networking Behaviour](#41-default-k8s-networking-behaviour)
   - 4.2 [How Network Policies Work](#42-how-network-policies-work)
   - 4.3 [CNI Plugin Requirement](#43-cni-plugin-requirement)
   - 4.4 [Default Deny All — Namespace Isolation](#44-default-deny-all--namespace-isolation)
   - 4.5 [Allow Specific Pod Communication](#45-allow-specific-pod-communication)
   - 4.6 [Egress Control](#46-egress-control)
5. [Kyverno — Policy Enforcement via Admission Control](#5-kyverno--policy-enforcement-via-admission-control)
   - 5.1 [What is Admission Control?](#51-what-is-admission-control)
   - 5.2 [What is Kyverno?](#52-what-is-kyverno)
   - 5.3 [Installing Kyverno](#53-installing-kyverno)
   - 5.4 [Validation Policy — Block latest Image Tag](#54-validation-policy--block-latest-image-tag)
   - 5.5 [Mutation Policy — Auto-add Labels](#55-mutation-policy--auto-add-labels)
   - 5.6 [Generation Policy — Auto-create Resources](#56-generation-policy--auto-create-resources)
   - 5.7 [More Kyverno Policy Examples](#57-more-kyverno-policy-examples)
6. [Pod Security — Hardening at the Pod Level](#6-pod-security--hardening-at-the-pod-level)
   - 6.1 [Pod Security Context](#61-pod-security-context)
   - 6.2 [Pod Security Admission (PSA)](#62-pod-security-admission-psa)
7. [Secrets Management](#7-secrets-management)
   - 7.1 [The Problem with Kubernetes Secrets](#71-the-problem-with-kubernetes-secrets)
   - 7.2 [Native Kubernetes Secrets — Limitations](#72-native-kubernetes-secrets--limitations)
   - 7.3 [ESO — External Secrets Operator with Vault](#73-eso--external-secrets-operator-with-vault)
   - 7.4 [ESO Setup — Step by Step](#74-eso-setup--step-by-step)
8. [Kubernetes Security in CI/CD](#8-kubernetes-security-in-cicd)
9. [K8s Security — Defence in Depth](#9-k8s-security--defence-in-depth)
10. [Summary](#10-summary)

---

## 🔐 1. Why Kubernetes Security Matters

Kubernetes clusters are complex, distributed systems with many components, APIs, and moving parts. A single misconfiguration — an open NetworkPolicy, an overly permissive RBAC role, an unencrypted secret — can give an attacker lateral movement across your entire infrastructure.

### 🔹 1.1 K8s Security Threat Surface

```
┌──────────────────────────────────────────────────────────────────────┐
│                  Kubernetes Security Threat Surface                  │
├───────────────────────┬──────────────────────────────────────────────┤
│  🌐  Network          │  All Pods can talk to all Pods by default    │
│  🔑  RBAC             │  Over-permissive roles, default SA misuse    │
│  🔒  Secrets          │  Base64 encoded only — not encrypted at rest │
│  🖼️  Images           │  Unscanned images with CVEs running in Pods  │
│  📋  Policies         │  No admission control = any config deployed  │
│  👤  Pod Identity     │  Containers running as root inside clusters  │
│  🏗️  Namespaces       │  No isolation between teams/environments     │
│  🤝  Supply Chain     │  Malicious Helm charts, third-party operators│
└───────────────────────┴──────────────────────────────────────────────┘
```

---

### 🔹 1.2 K8s Security Checklist at a Glance

| ✅ Control | 📖 Why It Matters |
|---|---|
| Namespaces + ResourceQuotas | Isolate teams; prevent noisy-neighbour resource exhaustion |
| RBAC with least privilege | Limit what each service account and user can do |
| Network Policies (default deny) | Stop lateral movement between Pods and namespaces |
| Kyverno policies | Enforce security standards at admission time |
| Non-root Pod security context | Prevent privilege escalation inside containers |
| External Secrets (ESO + Vault) | Keep secrets encrypted and out of Git |
| Image scanning (Trivy) | Block CVE-infected images before they enter the cluster |
| Audit logging | Full trail of who did what in the cluster |

---

## 🗂️ 2. Namespaces — Isolation and Multi-Tenancy

### 🔹 2.1 Why Namespaces Matter for Security

A Kubernetes namespace is a **logical division of the cluster** — it provides isolation for ownership, resource management, and access control across different teams or environments sharing the same physical cluster.

**Real-world example:**
> A company runs a single EKS cluster. Three product teams — Payments, Shipment, and Scores — all deploy their workloads to this cluster. Without namespaces, all Pods can see each other, consume unlimited resources, and share the same RBAC permissions. With namespaces, each team gets full isolation: their own resource budget, their own RBAC policies, and their own network boundary.

```
Single K8s Cluster
├── 🏦  payment-ns     (Payments Team)
│       └── Pods, Services, Secrets, ConfigMaps
├── 🚚  shipment-ns    (Shipment Team)
│       └── Pods, Services, Secrets, ConfigMaps
└── 🎯  score-ns       (Scores Team)
        └── Pods, Services, Secrets, ConfigMaps
```

**Security benefits of namespaces:**
- Scoped RBAC — a developer in `payment-ns` cannot access resources in `shipment-ns`
- Scoped NetworkPolicies — restrict cross-namespace Pod communication
- ResourceQuotas — each team gets a capped resource budget; one team cannot starve another
- Scoped Secrets — secrets in `payment-ns` are invisible to `shipment-ns`

---

### 🔹 2.2 Creating Namespaces

```bash
# Create namespaces for each team
kubectl create ns payment-ns
kubectl create ns shipment-ns
kubectl create ns score-ns

# Verify
kubectl get namespaces

# Deploy workloads scoped to their namespace
kubectl create deploy nginx-payments --image=nginx -n payment-ns
kubectl create deploy nginx-shipment --image=nginx -n shipment-ns

# List pods in a specific namespace
kubectl get pods -n payment-ns
kubectl get pods -n shipment-ns
```

**Namespace manifest (declarative):**

```yaml
# namespace-payment.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: payment-ns
  labels:
    team: payments
    environment: production
    pod-security.kubernetes.io/enforce: restricted   # PSA label
```

```bash
kubectl apply -f namespace-payment.yaml
```

---

### 🔹 2.3 Resource Quotas — Limiting CPU and Memory

A **ResourceQuota** limits the total amount of CPU, memory, and object counts that all resources within a namespace can consume. This prevents one team from consuming all cluster resources.

```yaml
# resourcequota-payment.yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: payment-ns-quota
  namespace: payment-ns
spec:
  hard:
    # ── Compute Resources ──────────────────────────────────────
    requests.cpu: "4"            # Total CPU requests across all Pods
    requests.memory: "8Gi"       # Total memory requests across all Pods
    limits.cpu: "8"              # Total CPU limits across all Pods
    limits.memory: "16Gi"        # Total memory limits across all Pods

    # ── Object Count Limits ────────────────────────────────────
    pods: "20"                   # Max 20 Pods in this namespace
    services: "10"               # Max 10 Services
    persistentvolumeclaims: "5"  # Max 5 PVCs
    secrets: "20"                # Max 20 Secrets
    configmaps: "20"             # Max 20 ConfigMaps
```

```bash
kubectl apply -f resourcequota-payment.yaml

# Check quota usage
kubectl describe resourcequota payment-ns-quota -n payment-ns
```

---

### 🔹 2.4 LimitRange — Default Resource Limits per Pod

A **LimitRange** sets default CPU and memory requests/limits for every Pod in a namespace — so Pods without explicit resource definitions still get sensible defaults.

```yaml
# limitrange-payment.yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: payment-ns-limits
  namespace: payment-ns
spec:
  limits:
  - type: Container
    default:
      cpu: "500m"
      memory: "256Mi"
    defaultRequest:
      cpu: "100m"
      memory: "128Mi"
    max:
      cpu: "2"
      memory: "2Gi"
    min:
      cpu: "50m"
      memory: "64Mi"
```

```bash
kubectl apply -f limitrange-payment.yaml
kubectl describe limitrange payment-ns-limits -n payment-ns
```

> ⚠️ **Without ResourceQuotas and LimitRanges:** A single misconfigured Pod could request unlimited CPU/memory, causing an OOMKill on other critical Pods — effectively a self-inflicted Denial of Service within the cluster.

---

## 🔑 3. RBAC — Role-Based Access Control

### 🔹 3.1 RBAC Core Concepts

Kubernetes RBAC controls **who can do what to which resources** in the cluster. It is built on four core objects:

```
┌─────────────────────────────────────────────────────────────────────┐
│                        RBAC Components                              │
├─────────────────────┬───────────────────────────────────────────────┤
│  👤  ServiceAccount │  An identity for a Pod or application         │
│  📋  Role           │  A set of permissions (namespace-scoped)      │
│  🔗  RoleBinding    │  Binds a ServiceAccount to a Role             │
│  🌐  ClusterRole    │  A set of permissions (cluster-wide)          │
│  🔗  ClusterRoleBinding │  Binds a SA to a ClusterRole (cluster-wide) │
└─────────────────────┴───────────────────────────────────────────────┘
```

---

### 🔹 3.2 Service Accounts

A **ServiceAccount** is the identity used by Pods to interact with the Kubernetes API server. Every Pod is automatically assigned the `default` ServiceAccount if none is specified.

> ⚠️ **Security Risk:** The `default` ServiceAccount often has broader permissions than needed. Always create a dedicated, minimal ServiceAccount for each application — this is the principle of least privilege applied to Pods.

```yaml
# serviceaccount-payments.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: payments-sa
  namespace: payment-ns
automountServiceAccountToken: false   # Disable auto-mount if API access not needed
```

```bash
kubectl apply -f serviceaccount-payments.yaml
kubectl get serviceaccounts -n payment-ns
```

**Use the ServiceAccount in a Pod:**

```yaml
# deployment-payments.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: payments-app
  namespace: payment-ns
spec:
  replicas: 2
  selector:
    matchLabels:
      app: payments
  template:
    metadata:
      labels:
        app: payments
    spec:
      serviceAccountName: payments-sa    # ← Assign dedicated SA
      automountServiceAccountToken: false
      containers:
      - name: payments
        image: payments-app:1.0
        resources:
          requests:
            cpu: "100m"
            memory: "128Mi"
          limits:
            cpu: "500m"
            memory: "256Mi"
```

---

### 🔹 3.3 Roles and RoleBindings — Namespace Scoped

A **Role** defines a set of permissions within a specific namespace. A **RoleBinding** grants those permissions to a ServiceAccount (or user/group).

```yaml
# role-payments-readonly.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: payments-readonly
  namespace: payment-ns
rules:
  # ── Allow reading Pods and their logs ──────────────────────
  - apiGroups: [""]
    resources: ["pods", "pods/log"]
    verbs: ["get", "list", "watch"]

  # ── Allow reading ConfigMaps ────────────────────────────────
  - apiGroups: [""]
    resources: ["configmaps"]
    verbs: ["get", "list"]

  # ── Allow reading Deployments ───────────────────────────────
  - apiGroups: ["apps"]
    resources: ["deployments"]
    verbs: ["get", "list", "watch"]
```

```yaml
# rolebinding-payments.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: payments-readonly-binding
  namespace: payment-ns
subjects:
  - kind: ServiceAccount
    name: payments-sa
    namespace: payment-ns
roleRef:
  kind: Role
  name: payments-readonly
  apiGroup: rbac.authorization.k8s.io
```

```bash
kubectl apply -f role-payments-readonly.yaml
kubectl apply -f rolebinding-payments.yaml

# Verify permissions
kubectl auth can-i get pods --namespace=payment-ns --as=system:serviceaccount:payment-ns:payments-sa
kubectl auth can-i delete pods --namespace=payment-ns --as=system:serviceaccount:payment-ns:payments-sa
# Output: yes / no
```

---

### 🔹 3.4 ClusterRoles and ClusterRoleBindings — Cluster Scoped

Use **ClusterRole** when a ServiceAccount needs permissions across **all namespaces** in the cluster (e.g., a monitoring agent, a CI/CD operator, a logging DaemonSet).

```yaml
# clusterrole-monitoring.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: cluster-monitoring-role
rules:
  # ── Read Pods across all namespaces ─────────────────────────
  - apiGroups: [""]
    resources: ["pods", "nodes", "namespaces", "services", "endpoints"]
    verbs: ["get", "list", "watch"]

  # ── Read metrics ────────────────────────────────────────────
  - apiGroups: ["metrics.k8s.io"]
    resources: ["pods", "nodes"]
    verbs: ["get", "list"]
```

```yaml
# clusterrolebinding-monitoring.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: cluster-monitoring-binding
subjects:
  - kind: ServiceAccount
    name: monitoring-sa
    namespace: monitoring-ns
roleRef:
  kind: ClusterRole
  name: cluster-monitoring-role
  apiGroup: rbac.authorization.k8s.io
```

```bash
kubectl apply -f clusterrole-monitoring.yaml
kubectl apply -f clusterrolebinding-monitoring.yaml

# Check all RBAC resources
kubectl get roles,rolebindings -n payment-ns
kubectl get clusterroles,clusterrolebindings | grep -v system
```

> 📌 **Full RBAC reference and lab commands:**
> [github.com/iam-veeramalla/DevSecOps-Zero-to-Hero — Kubernetes README](https://github.com/iam-veeramalla/DevSecOps-Zero-to-Hero/blob/main/05-Kubernetes/README.md)

---

### 🔹 3.5 RBAC Best Practices

| ✅ Best Practice | 📖 Reason |
|---|---|
| Never use the `default` ServiceAccount | It may have unintended permissions inherited from cluster setup |
| Set `automountServiceAccountToken: false` | Prevents the SA token from being auto-mounted if the app doesn't call the API |
| Use `Role` over `ClusterRole` where possible | Namespace scope = limited blast radius |
| Avoid wildcard `*` verbs or resources | Always specify the exact actions and resources needed |
| Audit RBAC regularly | Use `kubectl auth can-i` and tools like `rbac-lookup` or `KubiScan` |
| Separate read vs write roles | Read-only roles for monitoring/logging; write roles only for operators |

---

## 🌐 4. Network Policies

### 🔹 4.1 Default K8s Networking Behaviour

By default in Kubernetes, **all Pods can communicate with all other Pods across all namespaces** — with no restrictions. This flat network model is convenient for development but is a critical security risk in production.

```
Without NetworkPolicy:
payment-pod ──────────────► database-pod (payment-ns)   ✅ allowed
payment-pod ──────────────► secrets-pod  (shipment-ns)  ✅ allowed (DANGEROUS!)
payment-pod ──────────────► any-pod      (any-ns)       ✅ allowed (DANGEROUS!)
```

A compromised Pod in any namespace can reach **any other Pod in the entire cluster** — enabling lateral movement and data exfiltration.

---

### 🔹 4.2 How Network Policies Work

**NetworkPolicy** resources define rules for **which Pods can communicate with which other Pods**, based on:
- **Pod label selectors** — target specific Pods by their labels
- **Namespace selectors** — allow/block traffic from entire namespaces
- **IP blocks** — allow/block specific CIDR ranges (for external traffic)

> 💡 **Critical point:** NetworkPolicy rules use **label selectors and namespace selectors only** — not IP addresses (for Pod-to-Pod) — because Pod IPs are ephemeral and change on restart.

---

### 🔹 4.3 CNI Plugin Requirement

> ⚠️ **NetworkPolicies only work if your CNI plugin supports them.** The default Kubernetes networking does not enforce NetworkPolicies.

| 🌐 Environment | 🔌 CNI | 📋 NetworkPolicy Support |
|---|---|---|
| Self-managed cluster | Calico | ✅ Full support |
| Self-managed cluster | Flannel | ❌ Does not support NetworkPolicy |
| Self-managed cluster | Cilium | ✅ Full support + L7 rules |
| **AWS EKS** | **VPC CNI (default)** | ✅ **Supported natively — no extra CNI install needed** |
| GKE | Calico / Dataplane V2 | ✅ Supported |
| AKS | Azure CNI / Calico | ✅ Supported |

```bash
# Install Calico on a self-managed cluster
kubectl apply -f https://raw.githubusercontent.com/projectcalico/calico/v3.25.0/manifests/calico.yaml

# Verify Calico pods are running
kubectl get pods -n kube-system | grep calico
```

---

### 🔹 4.4 Default Deny All — Namespace Isolation

The **recommended starting point** is to deny all ingress and egress for a namespace, then explicitly allow only what is needed:

```yaml
# networkpolicy-default-deny.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: payment-ns
spec:
  podSelector: {}          # Applies to ALL Pods in payment-ns
  policyTypes:
  - Ingress
  - Egress
  # No rules defined = deny everything ✅
```

```bash
kubectl apply -f networkpolicy-default-deny.yaml

# Test: try to curl from one pod to another — should be blocked
kubectl exec -it <pod-name> -n payment-ns -- curl http://shipment-svc.shipment-ns
# Expected: connection refused or timeout ✅
```

---

### 🔹 4.5 Allow Specific Pod Communication

After applying default-deny, explicitly allow only required communication:

```yaml
# networkpolicy-allow-payments-to-db.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-payments-to-db
  namespace: payment-ns
spec:
  podSelector:
    matchLabels:
      app: database             # This policy applies to database Pods
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: payments         # Only payments Pods may connect
    ports:
    - protocol: TCP
      port: 5432                # Only on PostgreSQL port
```

```yaml
# networkpolicy-allow-dns.yaml
# Always allow DNS resolution (required for all Pods to function)
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-dns
  namespace: payment-ns
spec:
  podSelector: {}
  policyTypes:
  - Egress
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          kubernetes.io/metadata.name: kube-system
    ports:
    - protocol: UDP
      port: 53
    - protocol: TCP
      port: 53
```

---

### 🔹 4.6 Egress Control

Restrict outbound traffic from Pods — especially critical for preventing data exfiltration:

```yaml
# networkpolicy-restrict-egress.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: payments-restrict-egress
  namespace: payment-ns
spec:
  podSelector:
    matchLabels:
      app: payments
  policyTypes:
  - Egress
  egress:
  # ── Allow DNS ──────────────────────────────────────────────
  - to:
    - namespaceSelector:
        matchLabels:
          kubernetes.io/metadata.name: kube-system
    ports:
    - protocol: UDP
      port: 53

  # ── Allow connection to internal database only ─────────────
  - to:
    - podSelector:
        matchLabels:
          app: database
    ports:
    - protocol: TCP
      port: 5432

  # ── Allow HTTPS to specific external payment gateway ───────
  - to:
    - ipBlock:
        cidr: 203.0.113.0/24   # Payment gateway IP range
    ports:
    - protocol: TCP
      port: 443
```

```bash
# Apply all network policies
kubectl apply -f networkpolicy-default-deny.yaml
kubectl apply -f networkpolicy-allow-payments-to-db.yaml
kubectl apply -f networkpolicy-allow-dns.yaml

# Inspect applied policies
kubectl get networkpolicies -n payment-ns
kubectl describe networkpolicy default-deny-all -n payment-ns
```

---

## 🛡️ 5. Kyverno — Policy Enforcement via Admission Control

### 🔹 5.1 What is Admission Control?

**Admission Controllers** are plugins that intercept API server requests **after authentication and authorisation, but before the object is persisted to etcd**. There are two types:

```
kubectl apply → API Server → Authentication → Authorisation
                                                    ↓
                                         Admission Controllers
                                         ├── Validating Webhook  → Accept or Reject
                                         └── Mutating Webhook   → Modify before save
                                                    ↓
                                              etcd (persisted)
```

| 🔧 Type | 📖 Purpose | 💡 Example |
|---|---|---|
| **Validating** | Accept or reject a resource creation/modification | Block Pods with `image:latest` |
| **Mutating** | Automatically modify a resource before it is saved | Auto-inject security labels on every Pod |

---

### 🔹 5.2 What is Kyverno?

**Kyverno** is a Kubernetes-native policy engine that runs as an **Admission Controller**. Policies are written as Kubernetes YAML manifests (no Rego / custom language needed) making them easy to write, read, and version-control in Git.

**Kyverno can:**
- ✅ **Validate** — block non-compliant resources from being created
- ✅ **Mutate** — automatically patch resources (add labels, set defaults)
- ✅ **Generate** — automatically create companion resources (e.g., default NetworkPolicy on new Namespace)
- ✅ **Verify Images** — enforce image signing with Cosign

---

### 🔹 5.3 Installing Kyverno

```bash
# Install Kyverno via Helm (recommended)
helm repo add kyverno https://kyverno.github.io/kyverno/
helm repo update

helm install kyverno kyverno/kyverno \
  --namespace kyverno \
  --create-namespace

# Verify installation
kubectl get pods -n kyverno
kubectl get crds | grep kyverno
```

---

### 🔹 5.4 Validation Policy — Block latest Image Tag

Using `latest` as a Docker image tag is a bad practice — it makes deployments non-deterministic and non-reproducible. Kyverno can **block any Pod deployment that uses the `latest` tag**:

```yaml
# kyverno-block-latest-tag.yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: disallow-latest-tag
  annotations:
    policies.kyverno.io/title: Disallow Latest Tag
    policies.kyverno.io/severity: high
    policies.kyverno.io/description: >
      Using 'latest' as the image tag is non-deterministic and may cause
      security vulnerabilities to be deployed silently. Require explicit
      version tags on all container images.
spec:
  validationFailureAction: Enforce     # Enforce = block; Audit = log only
  background: true
  rules:
  - name: require-image-tag
    match:
      any:
      - resources:
          kinds:
          - Pod
    validate:
      message: "Image tag 'latest' is not allowed. Specify an explicit version tag (e.g., nginx:1.25.3)."
      pattern:
        spec:
          containers:
          - image: "!*:latest"         # Block any image ending in :latest
          initContainers:
          - image: "!*:latest"
```

```bash
kubectl apply -f kyverno-block-latest-tag.yaml

# Test: try to deploy a pod with latest tag
kubectl run test --image=nginx:latest -n payment-ns
# Expected output:
# Error: admission webhook "validate.kyverno.svc-fail" denied the request:
# Image tag 'latest' is not allowed. ✅
```

---

### 🔹 5.5 Mutation Policy — Auto-add Labels

Kyverno can automatically **patch resources** to add missing labels, annotations, or security settings — ensuring consistency across all Pods:

```yaml
# kyverno-mutate-add-labels.yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: add-default-labels
spec:
  rules:
  - name: add-team-label
    match:
      any:
      - resources:
          kinds:
          - Pod
    mutate:
      patchStrategicMerge:
        metadata:
          labels:
            +(managed-by): "kyverno"       # Add if not present
            +(environment): "production"   # Add if not present
```

```bash
kubectl apply -f kyverno-mutate-add-labels.yaml

# Deploy a Pod without labels — Kyverno will auto-add them
kubectl run auto-labeled --image=nginx:1.25 -n payment-ns
kubectl get pod auto-labeled -n payment-ns --show-labels
# Output: Labels include managed-by=kyverno, environment=production ✅
```

---

### 🔹 5.6 Generation Policy — Auto-create Resources

Kyverno can **automatically generate companion resources** when a new Namespace is created — for example, automatically applying a default NetworkPolicy to every new Namespace:

```yaml
# kyverno-generate-networkpolicy.yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: add-default-networkpolicy
spec:
  rules:
  - name: default-deny-on-new-namespace
    match:
      any:
      - resources:
          kinds:
          - Namespace
    generate:
      apiVersion: networking.k8s.io/v1
      kind: NetworkPolicy
      name: default-deny-all
      namespace: "{{request.object.metadata.name}}"
      synchronize: true       # Keep the generated resource in sync
      data:
        spec:
          podSelector: {}
          policyTypes:
          - Ingress
          - Egress
```

```bash
kubectl apply -f kyverno-generate-networkpolicy.yaml

# Create a new namespace — default-deny NetworkPolicy is auto-created
kubectl create ns new-team-ns
kubectl get networkpolicy -n new-team-ns
# Output: default-deny-all is automatically present ✅
```

---

### 🔹 5.7 More Kyverno Policy Examples

**Block privileged containers:**

```yaml
# kyverno-block-privileged.yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: disallow-privileged-containers
spec:
  validationFailureAction: Enforce
  rules:
  - name: check-privileged
    match:
      any:
      - resources:
          kinds: [Pod]
    validate:
      message: "Privileged containers are not allowed."
      pattern:
        spec:
          containers:
          - =(securityContext):
              =(privileged): "false"
```

**Require resource limits on all containers:**

```yaml
# kyverno-require-limits.yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-resource-limits
spec:
  validationFailureAction: Enforce
  rules:
  - name: check-container-resources
    match:
      any:
      - resources:
          kinds: [Pod]
    validate:
      message: "CPU and memory limits are required on all containers."
      pattern:
        spec:
          containers:
          - resources:
              limits:
                cpu: "?*"
                memory: "?*"
```

```bash
# Check Kyverno policy reports
kubectl get policyreport -A
kubectl describe policyreport -n payment-ns
```

---

## 🔒 6. Pod Security — Hardening at the Pod Level

### 🔹 6.1 Pod Security Context

A **securityContext** defines privilege and access control settings at the Pod or container level — the Kubernetes equivalent of Docker's runtime hardening flags.

```yaml
# secure-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-payments-pod
  namespace: payment-ns
spec:
  # ── Pod-level security context ─────────────────────────────
  securityContext:
    runAsNonRoot: true               # Must run as non-root
    runAsUser: 1000                  # Run as UID 1000
    runAsGroup: 3000                 # Run as GID 3000
    fsGroup: 2000                    # Volume files owned by GID 2000
    seccompProfile:
      type: RuntimeDefault           # Apply default seccomp profile

  serviceAccountName: payments-sa
  automountServiceAccountToken: false

  containers:
  - name: payments
    image: payments-app:1.2.3        # Explicit version tag (no latest!)
    # ── Container-level security context ─────────────────────
    securityContext:
      allowPrivilegeEscalation: false   # Cannot gain more privileges
      readOnlyRootFilesystem: true      # Read-only filesystem
      capabilities:
        drop: ["ALL"]                   # Drop all Linux capabilities
        add: ["NET_BIND_SERVICE"]       # Add only what is explicitly needed
    resources:
      requests:
        cpu: "100m"
        memory: "128Mi"
      limits:
        cpu: "500m"
        memory: "256Mi"
    ports:
    - containerPort: 3000
    volumeMounts:
    - name: tmp-volume
      mountPath: /tmp                  # Writable /tmp only

  volumes:
  - name: tmp-volume
    emptyDir: {}
```

```bash
kubectl apply -f secure-pod.yaml
kubectl describe pod secure-payments-pod -n payment-ns
```

---

### 🔹 6.2 Pod Security Admission (PSA)

**Pod Security Admission** is a built-in Kubernetes admission controller (GA since v1.25) that enforces the **Pod Security Standards** at the namespace level. Apply it via namespace labels:

| 🏷️ Profile | 📖 Description | 🔧 Use Case |
|---|---|---|
| `privileged` | No restrictions | System namespaces (kube-system) |
| `baseline` | Prevents known privilege escalations | General workloads |
| `restricted` | Strongest security — requires non-root, no privilege escalation, drop all caps | Security-sensitive production workloads |

```yaml
# namespace-with-psa.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: payment-ns
  labels:
    # ── Enforce restricted profile — violating Pods are REJECTED ──
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/enforce-version: latest

    # ── Warn profile — violating Pods are WARNED but allowed ──────
    pod-security.kubernetes.io/warn: restricted
    pod-security.kubernetes.io/warn-version: latest

    # ── Audit profile — violations logged to audit log ────────────
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/audit-version: latest
```

```bash
kubectl apply -f namespace-with-psa.yaml

# Test: try deploying a privileged pod to the restricted namespace
kubectl run priv-test --image=nginx:1.25 \
  --overrides='{"spec":{"containers":[{"name":"priv-test","image":"nginx:1.25","securityContext":{"privileged":true}}]}}' \
  -n payment-ns
# Expected: Pod rejected by PSA ✅
```

---

## 🔐 7. Secrets Management

### 🔹 7.1 The Problem with Kubernetes Secrets

Kubernetes Secrets appear to be secure — they have a dedicated API object, they can be RBAC-protected, and they are not visible in plain `kubectl describe`. But the reality is more concerning:

> ⚠️ **Kubernetes Secrets are NOT encrypted by default. They are only Base64-encoded — which is trivially reversible by anyone who can access the object.**

```bash
# Create a secret
kubectl create secret generic db-creds \
  --from-literal=password=SuperSecret123 \
  -n payment-ns

# Anyone with 'get secret' permission can decode it in seconds
kubectl get secret db-creds -n payment-ns -o jsonpath='{.data.password}' | base64 -d
# Output: SuperSecret123   ← fully visible ❌
```

---

### 🔹 7.2 Native Kubernetes Secrets — Limitations

| ⚠️ Limitation | 💥 Impact |
|---|---|
| Base64 encoded, not encrypted | Anyone with API access can decode the value |
| Stored in etcd in plaintext (without encryption at rest configured) | etcd backup = all secrets exposed |
| Anyone with namespace access can read secrets | RBAC alone is insufficient if namespace is shared |
| Cannot store secrets in Git safely | GitOps workflows cannot include secret manifests |
| No automatic rotation | Leaked credentials remain valid until manually rotated |
| No audit trail of secret access | Cannot tell who read a secret or when |

**The GitOps problem:**
> You want to store all Kubernetes manifests in Git for GitOps. But you cannot commit a Secret manifest to Git — the Base64-encoded value is easily decoded, and your credentials are now public. This is the gap that **External Secrets Operator (ESO)** solves.

---

### 🔹 7.3 ESO — External Secrets Operator with Vault

**External Secrets Operator (ESO)** is a Kubernetes operator that **pulls secrets from external secret management systems** (HashiCorp Vault, AWS Secrets Manager, GCP Secret Manager, Azure Key Vault) and automatically creates native Kubernetes Secret objects from them.

```
┌─────────────────────────────────────────────────────────────────────────┐
│               ESO + Vault — How It Works                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Git Repo (safe to commit)                                              │
│  └── ExternalSecret manifest  ──────────────────────────────────┐      │
│      (references Vault path,                                    │      │
│       no actual secret value)                                   ▼      │
│                                                      ESO Controller     │
│                                                           │             │
│                                                           ▼             │
│                                                    HashiCorp Vault      │
│                                                  (actual secret stored) │
│                                                           │             │
│                                                           ▼             │
│                                              K8s Secret (auto-created)  │
│                                              └── Pod reads it as env var│
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Key benefits:**
- ✅ Secret values **never stored in Git** — only references to Vault paths
- ✅ Secrets are **automatically rotated** when updated in Vault
- ✅ Full **audit trail** in Vault of every secret access
- ✅ Works perfectly with **GitOps** (ArgoCD, Flux) — manifests are safe to commit
- ✅ Centralised secret management across multiple clusters

---

### 🔹 7.4 ESO Setup — Step by Step

**Step 1 — Install ESO via Helm:**

```bash
helm repo add external-secrets https://charts.external-secrets.io
helm repo update

helm install external-secrets external-secrets/external-secrets \
  --namespace external-secrets \
  --create-namespace

# Verify
kubectl get pods -n external-secrets
kubectl get crds | grep external-secrets
```

**Step 2 — Store the secret in Vault:**

```bash
# Enable KV secrets engine in Vault
vault secrets enable -path=secret kv-v2

# Store the database password
vault kv put secret/payment-app/db-creds \
  password="SuperSecret123" \
  username="payments_user"

# Verify
vault kv get secret/payment-app/db-creds
```

**Step 3 — Create a Vault policy for ESO:**

```bash
vault policy write eso-payment-policy - <<EOF
path "secret/data/payment-app/*" {
  capabilities = ["read"]
}
EOF
```

**Step 4 — Create a SecretStore (connects ESO to Vault):**

```yaml
# secretstore-vault.yaml
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: vault-backend
  namespace: payment-ns
spec:
  provider:
    vault:
      server: "http://<VAULT_IP>:8200"
      path: "secret"
      version: "v2"
      auth:
        kubernetes:
          mountPath: "kubernetes"
          role: "eso-payment-role"
          serviceAccountRef:
            name: payments-sa
```

```bash
kubectl apply -f secretstore-vault.yaml
kubectl get secretstore -n payment-ns
```

**Step 5 — Create an ExternalSecret (safe to commit to Git):**

```yaml
# externalsecret-db-creds.yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: db-credentials
  namespace: payment-ns
spec:
  refreshInterval: "1h"           # Auto-sync every hour
  secretStoreRef:
    name: vault-backend
    kind: SecretStore
  target:
    name: db-creds-secret         # Name of the K8s Secret to create
    creationPolicy: Owner
  data:
  - secretKey: password           # Key in the K8s Secret
    remoteRef:
      key: payment-app/db-creds   # Vault path
      property: password          # Vault field
  - secretKey: username
    remoteRef:
      key: payment-app/db-creds
      property: username
```

```bash
kubectl apply -f externalsecret-db-creds.yaml

# ESO pulls from Vault and creates the K8s Secret automatically
kubectl get externalsecret -n payment-ns
kubectl get secret db-creds-secret -n payment-ns
```

**Step 6 — Use the auto-created Secret in a Pod:**

```yaml
# deployment with secret from ESO
spec:
  containers:
  - name: payments
    image: payments-app:1.2.3
    env:
    - name: DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: db-creds-secret     # Created automatically by ESO
          key: password
    - name: DB_USERNAME
      valueFrom:
        secretKeyRef:
          name: db-creds-secret
          key: username
```

> ✅ **The `externalsecret-db-creds.yaml` file is completely safe to commit to Git** — it contains only Vault path references, never the actual secret values. The ESO controller handles fetching and syncing.

---

## ⚙️ 8. Kubernetes Security in CI/CD

A complete DevSecOps pipeline for Kubernetes deployments:

```yaml
# .github/workflows/k8s-security-pipeline.yaml
name: K8s Secure Deployment Pipeline

on: [push, pull_request]

jobs:
  k8s-security:
    runs-on: ubuntu-latest
    steps:

      # ── 1. Checkout ───────────────────────────────────────────────
      - uses: actions/checkout@v4

      # ── 2. GitLeaks — scan for secrets in manifests ───────────────
      - uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      # ── 3. Checkov — scan K8s manifests for misconfigurations ─────
      - name: Checkov K8s Scan
        run: |
          pip install checkov
          checkov -d ./k8s --framework kubernetes --output cli

      # ── 4. Trivy — scan K8s manifests for CVEs ────────────────────
      - name: Trivy Manifest Scan
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: config
          scan-ref: ./k8s
          severity: CRITICAL,HIGH
          exit-code: 1

      # ── 5. Kyverno CLI — test policies against manifests ──────────
      - name: Kyverno Policy Test
        run: |
          curl -LO https://github.com/kyverno/kyverno/releases/latest/download/kyverno-cli_linux_amd64.tar.gz
          tar -xzf kyverno-cli_linux_amd64.tar.gz
          ./kyverno apply ./policies/ --resource ./k8s/

      # ── 6. Deploy to K8s (only if all checks pass) ────────────────
      - name: Deploy to EKS
        run: |
          aws eks update-kubeconfig --region us-east-1 --name my-cluster
          kubectl apply -f ./k8s/
```

---

## 🔒 9. K8s Security — Defence in Depth

```
┌──────────────────────────────────────────────────────────────────────┐
│            KUBERNETES SECURITY — DEFENCE IN DEPTH                   │
├────────┬─────────────────────────────────────────────────────────────┤
│ Layer  │ Control                                                      │
├────────┼─────────────────────────────────────────────────────────────┤
│   1    │ 🗂️  Namespaces + ResourceQuotas → Team isolation + limits   │
│   2    │ 🔑  RBAC (least privilege)       → Minimal SA permissions   │
│   3    │ 🌐  NetworkPolicy (default deny) → Block lateral movement   │
│   4    │ 🛡️  Kyverno Policies            → Admission control gates   │
│   5    │ 🔒  Pod SecurityContext          → Non-root, read-only FS   │
│   6    │ 🏷️  Pod Security Admission       → Namespace-level profiles │
│   7    │ 🔐  ESO + Vault                  → Encrypted external secrets│
│   8    │ 🔍  Trivy + Checkov in CI/CD     → CVE and misconfig gates  │
│   9    │ 📝  Audit Logging                → Full API activity trail  │
│  10    │ 🤖  Dependabot                   → Auto-update K8s versions │
└────────┴─────────────────────────────────────────────────────────────┘
```

| 🔢 Layer | 🛠️ Control | 🎯 What It Prevents |
|---|---|---|
| 1 | Namespaces + ResourceQuotas | Resource exhaustion, cross-team data access |
| 2 | RBAC least privilege | Over-permissive SA tokens, API server abuse |
| 3 | NetworkPolicy default deny | Lateral movement, cross-namespace Pod communication |
| 4 | Kyverno Admission Control | `latest` tags, privileged containers, missing limits |
| 5 | Pod SecurityContext | Root execution, privilege escalation, writable filesystem |
| 6 | Pod Security Admission | Cluster-wide enforcement of security profiles |
| 7 | ESO + Vault | Secrets in Git, unencrypted secrets in etcd |
| 8 | Trivy + Checkov | CVE-infected images, misconfigured manifests |
| 9 | Audit Logging | Undetected API abuse, insider threats |
| 10 | Dependabot | Outdated Kubernetes API versions and Helm charts |

---

## ✅ 10. Summary

| 🏷️ Topic | 💡 Key Takeaway |
|---|---|
| 🗂️ **Namespaces** | Logically divide the cluster per team — scoped RBAC, NetworkPolicies, and ResourceQuotas |
| 📊 **ResourceQuota** | Cap CPU, memory, and object count per namespace — prevent noisy-neighbour issues |
| 🔑 **RBAC** | Create dedicated ServiceAccounts per app; use Role (not ClusterRole) where possible |
| 👤 **Default SA** | Never use the default ServiceAccount — always create a minimal, dedicated one |
| 🌐 **NetworkPolicy** | Default-deny all, then explicitly allow only required Pod communication |
| 🔌 **CNI for NP** | NetworkPolicies require a compatible CNI — Calico, Cilium, or AWS VPC CNI on EKS |
| 🛡️ **Kyverno** | Policy-as-code admission control — validate, mutate, and generate K8s resources |
| 🚫 **Block latest** | Use Kyverno to block `image:latest` — enforce explicit version tags |
| 🔒 **SecurityContext** | Set `runAsNonRoot`, `readOnlyRootFilesystem`, `drop ALL caps` on every Pod |
| 🏷️ **PSA** | Apply `restricted` PSA profile to production namespaces via namespace labels |
| ⚠️ **K8s Secrets** | Not encrypted — Base64 only; anyone with get-secret permission can decode them |
| 🔐 **ESO + Vault** | Pull secrets from Vault into K8s automatically — safe for GitOps, auto-rotated |
| ⚙️ **CI/CD** | Run GitLeaks + Checkov + Trivy + Kyverno CLI on every PR before deploying |

---
