# 🛡️ Kubernetes RBAC — Roles, ClusterRoles & Bindings


---


## 📖 Core Concepts

| Concept | 📝 Description | 🌐 Scope |
|---|---|---|
| 👤 ServiceAccount | Identity used by pods/processes to talk to the API Server | Namespace |
| 📄 Role | Set of permissions (verbs on resources) | Namespace |
| 🌍 ClusterRole | Set of permissions across the whole cluster | Cluster-wide |
| 🔗 RoleBinding | Binds a Role (permissions) to a subject (SA/User/Group) | Namespace |
| 🔗 ClusterRoleBinding | Binds a ClusterRole to a subject cluster-wide | Cluster-wide |

> 💡 **Key idea:** A **Role/ClusterRole** defines *what* can be done. A **RoleBinding/ClusterRoleBinding** defines *who* gets to do it. Neither works without the other.

---

## 🛠️ Usage — Imperative Commands

### 1️⃣ List ServiceAccounts

```bash
kubectl get sa kube-scheduler -n kube-system
kubectl get sa myscheduler -n kube-system
```

### 2️⃣ Create a ConfigMap from a File

```bash
kubectl create configmap my-scheduler-config --from-file=/root/my-scheduler-config.yaml -n kube-system
kubectl get cm my-scheduler-config -n kube-system
```

### 3️⃣ List ClusterRoleBindings

```bash
kubectl get clusterrolebinding
```

### 🎯 Other Handy Imperative RBAC Commands

```bash
# Create a ServiceAccount
kubectl create serviceaccount my-service-account -n default

# Create a Role imperatively
kubectl create role pod-reader --verb=get,list --resource=pods -n default

# Create a ClusterRole imperatively
kubectl create clusterrole node-reader --verb=get,list,watch --resource=nodes

# Bind a Role to a ServiceAccount
kubectl create rolebinding pod-reader-binding \
  --role=pod-reader \
  --serviceaccount=default:my-service-account \
  -n default

# Bind a ClusterRole to a User cluster-wide
kubectl create clusterrolebinding cluster-admin-binding \
  --clusterrole=cluster-admin-role \
  --user=adminuser

# Check what a subject can do (great for debugging RBAC)
kubectl auth can-i list pods --as=system:serviceaccount:default:my-service-account
```

---

## 🏷️ Namespace & Default ServiceAccount

> 📌 Whenever a **Namespace** is created:
> - 🚫 **No Role** exists in it initially
> - ✅ A **`default` ServiceAccount`** is **always** auto-created

The `default` ServiceAccount acts like a **user identity**, authenticated by the **API Server** whenever any list/create/delete operation is performed on resources in that namespace.

```bash
kubectl get sa -n my-namespace
# NAME      SECRETS   AGE
# default   0         10s
```

> ⚠️ **Best practice:** Don't rely on the `default` SA for application workloads — create a dedicated ServiceAccount per app.

---

## 👤 ServiceAccount

A **ServiceAccount** is like a "user" for **machines/pods** — it's what the API Server checks against when a pod tries to perform an action.

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-service-account
  namespace: default
```

```bash
kubectl apply -f service-account.yaml
kubectl get sa my-service-account -n default
```

---

## 📄 Role vs ClusterRole

### 📘 Role — Namespace Scoped

A **Role** defines what actions a subject can perform on resources **within a single namespace**.

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: default
  name: admin-role
rules:
  - apiGroups: [""]
    resources: ["pods", "services"]
    verbs: ["get", "list", "create", "delete", "update"]
```

### 🌍 ClusterRole — Cluster Scoped

A **ClusterRole** defines permissions at the **cluster level** — across all namespaces, and for cluster-scoped resources like `nodes` or `namespaces`.

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: cluster-admin-role
rules:
  - apiGroups: [""]
    resources: ["nodes"]
    verbs: ["get", "list", "watch"]
  - apiGroups: [""]
    resources: ["namespaces"]
    verbs: ["get", "list"]
```

### ⚖️ Comparison

| Aspect | 📘 Role | 🌍 ClusterRole |
|---|---|---|
| Scope | Single namespace | Entire cluster |
| Resource types | Namespaced resources (pods, services, etc.) | Namespaced **and** cluster-scoped (nodes, namespaces, PVs) |
| Reusability | Must be re-created per namespace | Can be bound in any namespace via RoleBinding, or cluster-wide via ClusterRoleBinding |

---

## 🔗 RoleBinding vs ClusterRoleBinding

### 🔗 RoleBinding

A **RoleBinding** binds a **Role** to one or more subjects (User, Group, or ServiceAccount), granting them those permissions **within that namespace**.

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: admin-rolebinding
  namespace: default
subjects:
  - kind: User
    name: "johndoe"
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: admin-role
  apiGroup: rbac.authorization.k8s.io
```

### 🔗 ClusterRoleBinding

A **ClusterRoleBinding** binds a **ClusterRole** to a subject **across the entire cluster** — unlike RoleBinding, it isn't limited to one namespace.

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: cluster-admin-rolebinding
subjects:
  - kind: User
    name: "adminuser"
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: cluster-admin-role
  apiGroup: rbac.authorization.k8s.io
```

### ⚖️ Comparison

| Aspect | 🔗 RoleBinding | 🔗 ClusterRoleBinding |
|---|---|---|
| Binds | Role → Subject | ClusterRole → Subject |
| Scope of effect | One namespace | Entire cluster |
| Can bind a ClusterRole? | ✅ Yes (scoped to that namespace only) | ✅ Yes (cluster-wide) |
| Typical use | Per-namespace app permissions | Cluster admins, monitoring agents, controllers |

> 💡 A **RoleBinding can reference a ClusterRole** — this grants the ClusterRole's permissions but **only within that RoleBinding's namespace**. Handy for reusing a common ClusterRole (like `view` or `edit`) across many namespaces without duplicating Role definitions.

---

## 🧩 End-to-End Example: SA + Role + Binding + Pod

### 1️⃣ Create the ServiceAccount

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-service-account
```

### 2️⃣ Create a Role to Read Pods

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: default
  name: pod-reader
rules:
  - apiGroups: [""]
    resources: ["pods"]
    verbs: ["get", "list"]
```

### 3️⃣ Create a RoleBinding

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: pod-reader-binding
  namespace: default
subjects:
  - kind: ServiceAccount
    name: my-service-account
    namespace: default
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

### 4️⃣ Create a Pod that Uses the ServiceAccount

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  serviceAccountName: my-service-account
  containers:
    - name: nginx-container
      image: nginx
```

### 5️⃣ Apply All Resources

```bash
kubectl apply -f service-account.yaml
kubectl apply -f role.yaml
kubectl apply -f role-binding.yaml
kubectl apply -f pod.yaml
```

### 🔍 Verify

```bash
kubectl get sa my-service-account -n default
kubectl get role pod-reader -n default
kubectl get rolebinding pod-reader-binding -n default
kubectl auth can-i list pods --as=system:serviceaccount:default:my-service-account
```

---

## ✅ Quick Reference Table

| Resource | 🌐 Scope | 🔗 Binds To | 🎯 Purpose |
|---|---|---|---|
| 👤 ServiceAccount | Namespace | — | Identity for pods/processes |
| 📄 Role | Namespace | Subjects via RoleBinding | Defines allowed actions in a namespace |
| 🌍 ClusterRole | Cluster | Subjects via RoleBinding/ClusterRoleBinding | Defines allowed actions cluster-wide (or reusable across namespaces) |
| 🔗 RoleBinding | Namespace | Role or ClusterRole → Subject | Grants permissions within one namespace |
| 🔗 ClusterRoleBinding | Cluster | ClusterRole → Subject | Grants permissions across entire cluster |

---

## 🧹 Best Practices

- 🎯 **Least privilege** — grant only the verbs/resources a subject actually needs
- 📛 **Avoid `default` ServiceAccount** for application workloads — always create dedicated SAs
- 🌍 **Prefer Role + RoleBinding** over ClusterRole + ClusterRoleBinding unless cluster-wide access is genuinely required
- ♻️ **Reuse ClusterRoles** (e.g., built-in `view`, `edit`, `admin`) via namespace-scoped **RoleBindings** to avoid duplicating rule definitions
- 🔍 **Audit regularly**:
  ```bash
  kubectl get roles,rolebindings --all-namespaces
  kubectl get clusterroles,clusterrolebindings
  ```
- 🚫 **Avoid wildcard permissions** (`resources: ["*"]`, `verbs: ["*"]`) except for true cluster-admin cases
- 🧪 **Test before deploying** using `kubectl auth can-i ... --as=<subject>`
- 🗑️ **Clean up unused Roles/Bindings** — orphaned bindings are a common privilege-creep and security risk

---

📚 **References:** Kubernetes official documentation on RBAC Authorization, Role and ClusterRole, RoleBinding and ClusterRoleBinding, and ServiceAccounts.
