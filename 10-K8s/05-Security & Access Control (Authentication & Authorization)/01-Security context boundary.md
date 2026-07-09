# 🔐 Kubernetes ServiceAccounts & Token Expiration / Management


## 📖 What is a ServiceAccount?

A **ServiceAccount (SA)** is a Kubernetes identity used by **Pods and processes** (not humans) to authenticate against the **API server** and, optionally, external systems (cloud APIs, Vault, etc.).

- 🏷️ Every namespace automatically gets a `default` ServiceAccount
- 🧑‍💻 Human users authenticate differently (certs, OIDC, etc.) — SAs are for **workloads**
- 🔑 Each SA can have RBAC **Roles/ClusterRoles** bound to it to control what it can do
- 📛 Best practice: never rely on `default` — create a **dedicated SA per workload**

### 🧭 Why This Matters

Tokens issued to ServiceAccounts are how your app pods prove "who they are" to the Kubernetes API — and increasingly, to external systems via **OIDC federation**. Misconfigured or long-lived tokens are one of the most common Kubernetes security gaps.

---

## 🛠️ Basic Usage

```bash
# Create a service account
kubectl create serviceaccount my-app-sa -n my-namespace

# List all service accounts in a namespace
kubectl get serviceaccounts -n my-namespace
kubectl get sa -n my-namespace          # shorthand

# List across all namespaces
kubectl get sa --all-namespaces

# Describe a service account (shows mounted secrets, if any)
kubectl describe sa my-app-sa -n my-namespace

# Delete a service account
kubectl delete sa my-app-sa -n my-namespace
```

### 🔗 Attaching an SA to a Pod / Deployment

```yaml
spec:
  template:
    spec:
      serviceAccountName: my-app-sa
      automountServiceAccountToken: true   # 🚫 set false if pod doesn't call the API
      containers:
        - name: app
          image: myregistry/my-app:latest
```

> 💡 If `serviceAccountName` is omitted, the pod silently uses the `default` SA of its namespace — always set it explicitly.

---

## 📄 Creating & Binding a ServiceAccount

### 🎯 Full RBAC Example (Least Privilege)

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-app-sa
  namespace: my-namespace
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: my-app-role
  namespace: my-namespace
rules:
  - apiGroups: [""]
    resources: ["pods", "configmaps"]
    verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: my-app-binding
  namespace: my-namespace
subjects:
  - kind: ServiceAccount
    name: my-app-sa
    namespace: my-namespace
roleRef:
  kind: Role
  name: my-app-role
  apiGroup: rbac.authorization.k8s.io
```

### 🌐 Cluster-Wide Access (Use Sparingly)

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: my-app-cluster-binding
subjects:
  - kind: ServiceAccount
    name: my-app-sa
    namespace: my-namespace
roleRef:
  kind: ClusterRole
  name: view          # ⚠️ avoid cluster-admin unless absolutely required
  apiGroup: rbac.authorization.k8s.io
```

```bash
kubectl apply -f rbac.yaml

# Quick imperative alternative
kubectl create rolebinding my-app-binding \
  --role=my-app-role \
  --serviceaccount=my-namespace:my-app-sa \
  -n my-namespace
```

---

## 🎫 Understanding Token Types

| Aspect | 🗝️ Legacy Secret-Based Token | ✅ Bound (Projected) Token — Default since 1.24 |
|---|---|---|
| ⏱️ Expiration | ♾️ Never expires (until manually deleted) | Short-lived, default **~1 hour**, configurable |
| 📦 Storage | Stored as a `Secret` object in etcd | Mounted via **projected volume** in-memory, not a Secret |
| 🎯 Audience | Valid for any API consumer | **Audience-scoped** — bound to intended recipient |
| 🔄 Rotation | Manual only | **Auto-rotated** by kubelet before expiry |
| 🔒 Risk if leaked | High — usable indefinitely | Low — expires quickly, scoped to pod/namespace |
| 🧩 Where mounted | `/var/run/secrets/kubernetes.io/serviceaccount/` (legacy Secret) | Same path by default, but backed by TokenRequest API |

> 📌 **Since Kubernetes v1.24**, creating a ServiceAccount **no longer auto-generates** a matching long-lived Secret. Kubelet instead uses the **TokenRequest API** to mint short-lived, auto-rotating tokens mounted directly into pods.

---

## ⏱️ Token Expiration & Rotation

### 🔁 How Rotation Works

1. 🧾 Kubelet requests a token via TokenRequest API with a TTL (default 1 hour, minimum enforced ~10 minutes)
2. 📂 Token is projected into the pod's filesystem
3. ⏳ At roughly **80% of TTL**, kubelet proactively requests a **new token** and rewrites the file
4. 🔄 Your application must **re-read the token file** periodically — never cache it permanently in memory

### ⚙️ Configuring Expiration

```yaml
volumes:
  - name: sa-token
    projected:
      sources:
        - serviceAccountToken:
            path: token
            expirationSeconds: 3600   # ⏱️ 1 hour TTL, auto-rotated
            audience: my-api          # 🎯 optional audience restriction
```

| Setting | Notes |
|---|---|
| `expirationSeconds` | Requested TTL; API server may enforce min/max bounds |
| Cluster-wide default | Configurable via API server flag `--service-account-max-token-expiration` |
| Minimum enforced | Typically **10 minutes**, cluster-dependent |
| Client-go / SDKs | Most Kubernetes client libraries auto-handle token refresh from the mounted file |

### 🚦 What Happens on Expiration

- ❌ Expired tokens are rejected by the API server with `401 Unauthorized`
- ✅ As long as the **pod is running**, kubelet keeps the token refreshed — expiration issues usually mean your app is **caching a stale token** instead of re-reading the file
- 🛑 If a pod is deleted, its projected tokens become invalid immediately

---

## 🧾 Requesting Tokens Manually

Useful for debugging, CI/CD pipelines, or external tooling.

```bash
# Request a token with default 1-hour expiry
kubectl create token my-app-sa -n my-namespace

# Custom duration
kubectl create token my-app-sa -n my-namespace --duration=15m
kubectl create token my-app-sa -n my-namespace --duration=24h

# Scoped to a specific audience (e.g., Vault, external API)
kubectl create token my-app-sa -n my-namespace --audience=vault --duration=15m

# Use the token to test API access
TOKEN=$(kubectl create token my-app-sa -n my-namespace)
curl -H "Authorization: Bearer $TOKEN" https://<api-server>/api/v1/namespaces/my-namespace/pods
```

> ⚠️ `kubectl create token` requires Kubernetes **v1.24+** and the `TokenRequest` API to be enabled (enabled by default in modern clusters).

---

## 📦 Projected Volume Tokens (Fine-Grained Control)

Full pod example combining SA binding + custom token TTL + audience scoping:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-app-pod
  namespace: my-namespace
spec:
  serviceAccountName: my-app-sa
  containers:
    - name: app
      image: myregistry/my-app:latest
      volumeMounts:
        - name: sa-token
          mountPath: /var/run/secrets/tokens
          readOnly: true
  volumes:
    - name: sa-token
      projected:
        sources:
          - serviceAccountToken:
              path: token
              expirationSeconds: 1800     # 30 minutes
              audience: internal-service
```

Application-side, read the token fresh on each use (or on file-change events) rather than caching indefinitely:

```bash
TOKEN_PATH=/var/run/secrets/tokens/token
TOKEN=$(cat "$TOKEN_PATH")
```

---

## ⚠️ Legacy Long-Lived Tokens

Only create these for **legacy integrations** that cannot consume short-lived tokens (rare in modern setups).

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: my-app-sa-token
  annotations:
    kubernetes.io/service-account.name: my-app-sa
type: kubernetes.io/service-account-token
```

```bash
# Apply and retrieve
kubectl apply -f legacy-token-secret.yaml
kubectl get secret my-app-sa-token -n my-namespace -o jsonpath='{.data.token}' | base64 -d
```

🚩 **Risks of legacy tokens:**
- ♾️ Never expire automatically → long attack window if leaked
- 🗄️ Sit in etcd as plaintext-decodable Secrets
- 🔍 Harder to audit usage/lifetime
- 🧹 Must be manually rotated and deleted

---

## ☁️ Cloud Identity Federation

Instead of embedding cloud credentials or using long-lived tokens for **cloud API access**, federate the SA's OIDC identity with the cloud provider:

| Platform | Mechanism | Icon |
|---|---|---|
| AWS | IAM Roles for Service Accounts (**IRSA**) | 🟧 |
| GCP | **Workload Identity** | 🟦 |
| Azure | **Azure AD Workload Identity** | 🟪 |
| HashiCorp Vault | Kubernetes Auth Method (JWT/OIDC) | 🟩 |

```yaml
# Example: GKE Workload Identity annotation
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-app-sa
  namespace: my-namespace
  annotations:
    iam.gke.io/gcp-service-account: my-gcp-sa@project-id.iam.gserviceaccount.com
```

> 🎯 This lets short-lived Kubernetes SA tokens be **exchanged** for short-lived cloud credentials — no static keys anywhere.

---

## 🧹 Management Best Practices

- 🎯 **Least privilege** — scope Roles tightly; avoid `cluster-admin` and wildcard verbs/resources
- 📛 **Never use `default` SA** for application workloads — always create dedicated ones
- 🚫 **Disable auto-mount** for pods that don't need API access:
  ```yaml
  automountServiceAccountToken: false
  ```
- ⏱️ **Prefer short `expirationSeconds`** for sensitive/external-facing tokens
- 🎯 **Scope audiences** explicitly when tokens are consumed by non-Kubernetes systems
- 🔄 **Avoid legacy Secret tokens** unless there's no alternative; rotate them regularly if used
- 🔍 **Audit periodically**:
  ```bash
  kubectl get sa --all-namespaces
  kubectl get rolebinding,clusterrolebinding --all-namespaces -o wide
  ```
- 🗑️ **Remove orphaned SAs** and unused RoleBindings — common privilege-creep source
- ☁️ **Use OIDC/Workload Identity federation** instead of static cloud credentials
- 📊 **Monitor API server audit logs** for unusual SA token usage patterns

---

## 🚨 Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| ❌ `401 Unauthorized` | Cached/expired token | Re-read token file; check `expirationSeconds` |
| 🚫 `403 Forbidden` | Missing/incorrect RBAC binding | `kubectl auth can-i <verb> <resource> --as=system:serviceaccount:<ns>:<sa>` |
| 🕵️ Token not mounting | `automountServiceAccountToken: false` set | Explicitly set `true` on pod/SA |
| 🔁 App breaks after ~1 hr | Not handling token rotation | Read token from file each request, don't cache in memory long-term |
| 🌐 External service rejects token | Wrong/missing `audience` | Set correct `audience` in projected token or `kubectl create token` |

Useful diagnostic commands:

```bash
kubectl describe sa <name> -n <namespace>
kubectl auth can-i list pods --as=system:serviceaccount:<ns>:<sa>
kubectl get events -n <namespace> --field-selector involvedObject.name=<pod>
```

---

## ✅ Quick Reference Cheat Sheet

```bash
# Create SA
kubectl create sa my-app-sa -n my-namespace

# Bind RBAC role
kubectl create rolebinding my-binding --role=my-role --serviceaccount=my-namespace:my-app-sa

# Request short-lived token
kubectl create token my-app-sa --duration=15m

# Test permissions
kubectl auth can-i get pods --as=system:serviceaccount:my-namespace:my-app-sa

# Audit all SAs
kubectl get sa --all-namespaces

# Check bindings for a specific SA
kubectl get rolebinding,clusterrolebinding --all-namespaces -o json | \
  jq '.items[] | select(.subjects[]?.name=="my-app-sa")'
```

| ✅ Do | 🚫 Don't |
|---|---|
| Use dedicated SA per workload | Use `default` SA for apps |
| Use short-lived, audience-scoped tokens | Rely on long-lived Secret tokens |
| Disable auto-mount when unneeded | Leave auto-mount on for every pod blindly |
| Federate cloud identity via OIDC | Embed static cloud credentials in pods |
| Regularly audit SAs & bindings | Let unused SAs/bindings pile up |

---

📚 **References:** Kubernetes official documentation on Service Accounts, Managing Service Accounts, and Configuring Service Accounts for Pods (TokenRequest API / bound tokens).
