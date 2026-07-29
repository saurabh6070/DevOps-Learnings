# ⛵ Helm — The Kubernetes Package Manager

---

## 📖 1. What is Helm?

**Helm** is the official **package manager for Kubernetes**. It helps you define, install, and upgrade even the most complex Kubernetes applications.

> 💡 **Simple Analogy:** If Kubernetes is like Ubuntu, then Helm is like `apt`, and a Helm **Chart** is like a `.deb` package.

Helm packages multiple Kubernetes YAML files (Deployments, Services, ConfigMaps, Secrets, Ingress, etc.) into a **single reusable unit** called a **Chart**, making applications easy to install, configure, version, and share.

---

## ❓ 2. Why Do We Need Helm?

Without Helm, deploying an app in Kubernetes means manually writing and applying many YAML files:

```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f configmap.yaml
kubectl apply -f ingress.yaml
```

This becomes painful when:
- 🔁 You need to deploy the **same app** across Dev, Staging, and Production with different configs
- 📦 You want to **share** an application (like MySQL, Nginx, Prometheus) with others
- 🔄 You need **easy upgrades and rollbacks**
- 🧩 You have **many interdependent** YAML files to manage

### ✅ Helm Solves This By Providing:
| Problem | Helm's Solution |
|---|---|
| Repetitive YAML writing | Reusable templated Charts |
| Different configs per environment | `values.yaml` overrides |
| Manual tracking of deployed versions | Release history & versioning |
| Difficult rollback | One command rollback |
| Sharing applications | Public/private Chart repositories |

---

## 🏗️ 3. Helm Architecture

### Helm 3 Architecture (Current — Client-Only)
```
 ┌─────────────┐        ┌──────────────────┐        ┌────────────┐
 │  Helm CLI   │  --->  │ Kubernetes API    │  --->  │   Cluster  │
 │ (Client)    │        │ Server            │        │  Resources │
 └─────────────┘        └──────────────────┘        └────────────┘
```

- 🖥️ **Helm Client** — CLI tool (`helm`) used by developers/DevOps engineers
- 🔌 Talks **directly** to the Kubernetes API server using your kubeconfig
- 🗄️ Stores **release information as Kubernetes Secrets** inside the cluster (in the target namespace)

> ⚠️ **Note (Important for exams/interviews):** Helm 2 used a server-side component called **Tiller**, which had major security issues (cluster-wide admin access). **Tiller was removed in Helm 3** — Helm 3 is client-only and much more secure.

---

## 📦 4. Helm Charts — The Core Concept

A **Chart** is a collection of files that describe a related set of Kubernetes resources.

### 📁 Standard Chart Directory Structure
```
mychart/
├── Chart.yaml          # 📄 Metadata about the chart (name, version, description)
├── values.yaml         # ⚙️ Default configuration values
├── charts/             # 📚 Dependent/sub-charts
├── templates/          # 🧩 Kubernetes YAML templates (uses Go templating)
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── _helpers.tpl    # 🔧 Reusable template snippets/functions
│   └── NOTES.txt       # 📝 Post-install usage instructions
└── .helmignore          # 🚫 Files to ignore when packaging
```

### 📄 Chart.yaml Example
```yaml
apiVersion: v2
name: mychart
description: A Helm chart for my application
version: 0.1.0          # Chart version
appVersion: "1.0.0"      # Version of the app it deploys
```

### ⚙️ values.yaml Example
```yaml
replicaCount: 2

image:
  repository: nginx
  tag: "1.25"

service:
  type: ClusterIP
  port: 80
```

### 🧩 Template Example (templates/deployment.yaml)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}-deployment
spec:
  replicas: {{ .Values.replicaCount }}
  template:
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
```

> 🔑 **Key Idea:** Helm uses **Go templating** (`{{ }}`) to inject values from `values.yaml` into the YAML manifests dynamically.

---

## 🧠 5. Important Helm Objects (Built-in Variables)

| Object | Description |
|---|---|
| `.Values` | 🔢 Values from `values.yaml` or `--set` flag |
| `.Release` | 🚀 Info about the release (Name, Namespace, IsInstall, IsUpgrade) |
| `.Chart` | 📄 Info from `Chart.yaml` |
| `.Files` | 📂 Access to non-template files in the chart |
| `.Capabilities` | ☸️ Info about the Kubernetes cluster/API versions |

---

## 🌐 6. Helm Repositories

A **repository** is a place where packaged charts are stored and shared (similar to Docker Hub for containers).

```bash
# ➕ Add a repository
helm repo add bitnami https://charts.bitnami.com/bitnami

# 🔄 Update repo index
helm repo update

# 🔍 Search for a chart
helm search repo nginx

# 📋 List added repos
helm repo list
```

Popular public repositories: **Bitnami**, **Prometheus Community**, **Ingress-Nginx**, **Elastic**

---

## 🛠️ 7. Essential Helm Commands (Cheat Sheet)

### 🚀 Installing & Managing Releases
```bash
# Install a chart (creates a "release")
helm install my-release bitnami/nginx

# Install with custom values file
helm install my-release ./mychart -f custom-values.yaml

# Install with inline value override
helm install my-release ./mychart --set replicaCount=3

# Install into a specific namespace
helm install my-release ./mychart -n my-namespace --create-namespace
```

### 📋 Viewing Releases
```bash
helm list                  # List releases in current namespace
helm list -A                # List releases across ALL namespaces
helm status my-release       # Show status of a release
helm get values my-release   # Show values used in a release
helm get manifest my-release # Show rendered Kubernetes manifests
```

### ⬆️ Upgrading & ⏪ Rolling Back
```bash
helm upgrade my-release ./mychart --set replicaCount=5

helm history my-release           # View revision history
helm rollback my-release 1         # Rollback to revision 1
```

### 🗑️ Uninstalling
```bash
helm uninstall my-release
```

### 🧪 Testing & Debugging
```bash
helm template ./mychart          # Render templates locally (no install)
helm install --dry-run --debug my-release ./mychart   # Simulate install
helm lint ./mychart                # Check chart for syntax/best-practice issues
```

### 📦 Packaging & Creating Charts
```bash
helm create mychart      # Scaffold a new chart
helm package mychart      # Package chart into a .tgz archive
helm dependency update    # Download chart dependencies
```

---

## 🔄 8. Helm Release Lifecycle

```
helm install ──► Release (Revision 1)
      │
      ▼
helm upgrade ──► Release (Revision 2)
      │
      ▼
helm rollback 1 ──► Release (Revision 3, reverts to config of Rev 1)
      │
      ▼
helm uninstall ──► Release removed
```

> 🧾 Every `install`/`upgrade` creates a new **revision**, so you always have a history to roll back to.

---

## 🪝 9. Helm Hooks

Hooks let you run jobs at specific points in a release lifecycle (e.g., before install, after upgrade).

| Hook | Trigger Point |
|---|---|
| `pre-install` | 🕐 Before resources are installed |
| `post-install` | ✅ After all resources are installed |
| `pre-upgrade` | 🔼 Before upgrade |
| `post-upgrade` | 🔽 After upgrade |
| `pre-delete` | 🗑️ Before deletion |
| `post-delete` | ✅ After deletion |

```yaml
metadata:
  annotations:
    "helm.sh/hook": pre-install
```

**Common use case:** Running a database migration Job before the app deployment.

---

## 🧬 10. Helm Dependencies (Sub-charts)

Charts can depend on other charts (e.g., a web app chart that depends on a Redis chart).

### `Chart.yaml`
```yaml
dependencies:
  - name: redis
    version: "17.x.x"
    repository: "https://charts.bitnami.com/bitnami"
```

```bash
helm dependency update   # Downloads dependencies into charts/ folder
```

---

## ⚔️ 11. Helm vs Plain kubectl (Quick Comparison)

| Feature | `kubectl apply` | 🎯 Helm |
|---|---|---|
| Templating | ❌ No | ✅ Yes (Go templates) |
| Versioning/Rollback | ❌ Manual | ✅ Built-in (`helm rollback`) |
| Reusability across environments | ❌ Hard | ✅ Easy (`values.yaml`) |
| Package sharing | ❌ Not designed for it | ✅ Charts + Repositories |
| Dependency management | ❌ No | ✅ Yes (sub-charts) |

---

## ✅ 12. Helm Best Practices

- 🏷️ Always **pin chart versions** in production (`helm install ... --version x.y.z`)
- 🔐 Store secrets separately — avoid hardcoding sensitive data in `values.yaml`; use **Helm Secrets** or **Sealed Secrets**
- 🧪 Run `helm lint` and `helm template` before every deployment
- 📁 Keep environment-specific values in separate files: `values-dev.yaml`, `values-prod.yaml`
- 🧾 Use `helm diff` plugin to preview changes before upgrading
- 🗂️ Maintain a clean **naming convention** for releases (e.g., `app-env-component`)

---

## 📝 13. Quick Revision Summary

| Term | Meaning |
|---|---|
| **Chart** | 📦 Package of Kubernetes YAML templates |
| **Release** | 🚀 A deployed instance of a chart |
| **Repository** | 🌐 Storage location for sharing charts |
| **Values.yaml** | ⚙️ Default configuration for a chart |
| **Revision** | 🔢 A version/snapshot of a release |
| **Tiller** | ⚠️ Server-side component in Helm 2 (removed in Helm 3) |

---

## 🎯 14. Sample Exam/Interview Questions

1. ❓ What problem does Helm solve compared to plain `kubectl apply`?
2. ❓ What is the difference between Helm 2 and Helm 3 architecture?
3. ❓ What is stored in `values.yaml` and how does it interact with `templates/`?
4. ❓ How do you rollback a failed Helm release?
5. ❓ What are Helm hooks and where would you use `pre-install`?
6. ❓ How does Helm store release state in the cluster?

---

> 📚 **Study Tip:** Practice by running `helm create mychart`, then modify `values.yaml` and `templates/deployment.yaml`, and observe changes using `helm template ./mychart`.
