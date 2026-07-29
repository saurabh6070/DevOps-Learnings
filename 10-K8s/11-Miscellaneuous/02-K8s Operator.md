# ⚙️ Kubernetes Operators — Complete Student Notes

---

## 📌 1. What is a Kubernetes Operator?

A **Kubernetes Operator** is a software extension that uses **Custom Resources (CRs)** to manage applications and their components in a Kubernetes-native way.

In simple words:

> An Operator is a **human operator's knowledge, packaged into code**, that runs inside the cluster and automatically manages a complex, stateful application — just like a real DevOps engineer would.

- Operators extend Kubernetes' native capabilities to handle **application-specific operational tasks**.
- They are built on two core Kubernetes concepts:
  - **Custom Resource Definitions (CRDs)**
  - **Controllers** (control loops)

---

## 🎯 2. Why Do We Need Operators?

Kubernetes natively knows how to manage **stateless** applications well using built-in objects like `Deployment`, `ReplicaSet`, and `Service`. But it does **not** understand application-specific operational knowledge such as:

| Challenge | Example |
|---|---|
| 🗄️ Stateful app management | Databases like PostgreSQL, MySQL, MongoDB |
| 🔄 Backup & restore | Automated snapshotting of data |
| 📈 Scaling with app logic | Adding a replica to a DB cluster correctly |
| 🔧 Upgrades | Rolling upgrade of a distributed system without downtime |
| 🚨 Self-healing | Detecting a failed database node and re-electing a leader |
| 🔐 Configuration management | Rotating credentials, TLS certs, etc. |

**Operators solve this gap** by encoding this operational knowledge into software that runs continuously inside the cluster.

---

## 🧩 3. Core Building Blocks of an Operator

### 🔹 3.1 Custom Resource Definition (CRD)
A CRD extends the Kubernetes API by defining a **new resource type** (e.g., `MySQLCluster`, `KafkaTopic`).

```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: mysqlclusters.db.example.com
spec:
  group: db.example.com
  names:
    kind: MySQLCluster
    plural: mysqlclusters
  scope: Namespaced
  versions:
    - name: v1
      served: true
      storage: true
```

### 🔹 3.2 Custom Resource (CR)
A CR is an **instance** of the CRD — how the user requests the desired state.

```yaml
apiVersion: db.example.com/v1
kind: MySQLCluster
metadata:
  name: my-database
spec:
  replicas: 3
  version: "8.0"
  storageSize: 10Gi
```

### 🔹 3.3 Controller (Reconciliation Loop)
The **controller** is the "brain" of the Operator. It continuously watches the CR and the cluster's actual state, then takes action to match the **desired state**.

```
   ┌─────────────┐        Watch/Observe        ┌─────────────────┐
   │  Custom      │ ───────────────────────────▶ │   Operator      │
   │  Resource    │                              │   Controller    │
   │  (Desired    │ ◀─────────────────────────── │   (Reconcile    │
   │   State)     │        Take Action           │    Loop)        │
   └─────────────┘                              └─────────────────┘
                                                          │
                                                          ▼
                                                 ┌─────────────────┐
                                                 │  Actual Cluster │
                                                 │  State (Pods,   │
                                                 │  PVCs, Services)│
                                                 └─────────────────┘
```

This continuous loop is called the **Reconciliation Loop**:

```
observe → diff (desired vs actual) → act → repeat
```

---

## 🏗️ 4. Operator Architecture (How It Works Internally)

1. **User applies a Custom Resource (CR)** — e.g., `kubectl apply -f mysqlcluster.yaml`
2. The **Kubernetes API server** stores the CR object in `etcd`.
3. The **Operator's controller** (running as a Pod, usually a `Deployment`) watches the API server for changes to this CR type.
4. The controller compares the **desired state** (from the CR spec) with the **current state** of the cluster.
5. If there is a difference, the controller takes corrective action — creating/updating/deleting Pods, PVCs, Services, ConfigMaps, etc.
6. The controller updates the CR's **`status`** subresource to reflect the current state.
7. This loop repeats continuously (event-driven + periodic resync).

---

## 🆚 5. Operator vs Controller vs Custom Resource

| Concept | Role |
|---|---|
| 🧾 **Custom Resource (CR)** | Declares *what* the user wants (desired state) |
| 📐 **Custom Resource Definition (CRD)** | Defines the *schema* of the new resource type |
| 🤖 **Controller** | Watches resources and reconciles state (a generic pattern, built into K8s core too, e.g., `ReplicaSet` controller) |
| ⚙️ **Operator** | A controller **+ CRD combined**, specifically designed to manage **application-specific, domain knowledge** (usually stateful apps) |

> 💡 **Key takeaway:** Every Operator uses a controller, but not every controller is an Operator. Built-in controllers (like the Deployment controller) manage generic K8s objects; Operators manage **custom, application-specific** objects.

---

## 📊 6. Operator Capability Levels (Maturity Model)

The **Operator Framework** defines 5 levels of Operator maturity:

| Level | Name | Capability |
|---|---|---|
| 1️⃣ | **Basic Install** | Automated app provisioning and configuration |
| 2️⃣ | **Seamless Upgrades** | Patch and minor version upgrades |
| 3️⃣ | **Full Lifecycle** | App lifecycle: backup, restore, failure recovery |
| 4️⃣ | **Deep Insights** | Metrics, alerts, log processing, workload analysis |
| 5️⃣ | **Auto Pilot** | Auto-scaling, auto-healing, auto-tuning, anomaly detection |

---

## 🛠️ 7. Building an Operator — Common Frameworks

| Framework | Language | Notes |
|---|---|---|
| 🧰 **Operator SDK** | Go, Ansible, Helm | Most popular, part of the Operator Framework by Red Hat |
| 🐍 **Kopf** | Python | Simple Python-based Operator framework |
| 🔧 **KUDO** | YAML-based (declarative) | No coding required for simple operators |
| 🧱 **Kubebuilder** | Go | Scaffolding tool for building CRDs & controllers |
| ☕ **Java Operator SDK** | Java | For Java-based Operators |

### Basic steps to build an Operator (using Operator SDK):
```bash
# 1. Initialize a new operator project
operator-sdk init --domain=example.com --repo=github.com/example/mysql-operator

# 2. Create a new API (CRD + Controller)
operator-sdk create api --group db --version v1 --kind MySQLCluster --resource --controller

# 3. Implement reconciliation logic in controllers/mysqlcluster_controller.go

# 4. Build and push the operator image
make docker-build docker-push IMG=myrepo/mysql-operator:v1

# 5. Deploy the operator to the cluster
make deploy IMG=myrepo/mysql-operator:v1
```

---

## 🌐 8. Popular Real-World Operators

| Operator | Manages |
|---|---|
| 🐘 **PostgreSQL Operator (Zalando/Crunchy)** | PostgreSQL clusters |
| 🍃 **MongoDB Community Operator** | MongoDB replica sets |
| 📨 **Strimzi Operator** | Apache Kafka clusters |
| 🔍 **Elastic Cloud on Kubernetes (ECK)** | Elasticsearch & Kibana |
| 📊 **Prometheus Operator** | Prometheus, Alertmanager monitoring stack |
| 🔐 **Cert-Manager** | TLS certificate issuance & renewal |
| 🐬 **MySQL Operator** | MySQL/InnoDB clusters |
| 🦾 **Argo CD Operator** | GitOps continuous delivery |

> 🔎 Browse hundreds of community Operators at **[OperatorHub.io](https://operatorhub.io)**.

---

## 📦 9. Installing & Managing Operators — OLM

**OLM (Operator Lifecycle Manager)** helps install, upgrade, and manage the lifecycle of Operators in a cluster declaratively.

Key OLM responsibilities:
- 📥 Installing Operators from a catalog (like OperatorHub)
- 🔄 Automatic or manual upgrades
- 🔗 Managing dependencies between Operators
- 🔑 RBAC and permission management for Operators

```bash
# Install OLM on a cluster
operator-sdk olm install

# Install an operator from OperatorHub
kubectl create -f https://operatorhub.io/install/prometheus.yaml
```

---

## ✅ 10. Advantages of Using Operators

- 🤖 **Automation** of complex, repetitive operational tasks
- 🩹 **Self-healing** applications (auto-restart, failover)
- 📏 **Consistency** — same operational logic applied every time
- ⏱️ **Faster recovery** from failures without manual intervention
- 📚 **Encodes expert knowledge** into reusable software
- 🔁 **Declarative management** — just define desired state via CR

---

## ⚠️ 11. Challenges / Limitations

- 🧠 Requires **deep application knowledge** to build correctly
- 🐛 Poorly written Operators can introduce **bugs or instability**
- 🔓 Operators often need **elevated RBAC permissions** (security risk if misconfigured)
- 🧪 **Testing** an Operator's reconciliation logic thoroughly is complex
- 📦 Adds **operational overhead** for simple, stateless applications (may be overkill)

---

## 🆚 12. Operator vs Helm Chart

| Aspect | Helm Chart | Operator |
|---|---|---|
| 📦 Purpose | Templating & packaging K8s manifests | Ongoing lifecycle management with logic |
| 🧠 Intelligence | No runtime logic (static templates) | Active, continuous reconciliation |
| 🔄 Day-2 operations | ❌ Not handled (manual) | ✅ Handled automatically (backups, scaling, healing) |
| 🛠️ Best for | Simple/stateless app deployment | Complex/stateful applications |
| ⚙️ Runs continuously? | ❌ No (one-time install/upgrade) | ✅ Yes (runs as a controller Pod) |

> 💡 In practice, Helm and Operators are often used **together** — Helm to install the Operator itself, and the Operator then manages the actual application.

---

## 🧪 13. Example: End-to-End Flow

1. Admin installs the **Strimzi Kafka Operator** in the cluster.
2. Developer creates a Custom Resource:
   ```yaml
   apiVersion: kafka.strimzi.io/v1beta2
   kind: Kafka
   metadata:
     name: my-kafka-cluster
   spec:
     kafka:
       replicas: 3
       storage:
         type: persistent-claim
         size: 100Gi
   ```
3. The Strimzi Operator detects this CR and automatically:
   - Creates StatefulSets for Kafka brokers
   - Provisions PersistentVolumeClaims
   - Sets up Services for internal/external access
   - Configures ZooKeeper (or KRaft) coordination
4. If a broker Pod crashes, the Operator detects the drift and **recreates it automatically**.

---

## 📝 14. Quick Revision Summary

- **Operator = CRD + Controller + Domain-specific operational logic**
- Solves the problem of managing **stateful, complex applications** on Kubernetes
- Works via a continuous **reconcile loop**: `observe → diff → act`
- Maturity ranges from **Basic Install** to **Auto Pilot** (5 capability levels)
- Built using frameworks like **Operator SDK, Kubebuilder, Kopf, KUDO**
- Managed at scale using **OLM (Operator Lifecycle Manager)**
- Real examples: **Prometheus Operator, Strimzi, ECK, Postgres Operator**

---

## ❓ 15. Quick Self-Check Questions

1. What are the two main Kubernetes concepts an Operator is built on?
2. What is the difference between a CRD and a CR?
3. Explain the reconciliation loop in your own words.
4. Name any two real-world Kubernetes Operators and what they manage.
5. What is OLM, and why is it useful?
6. How does an Operator differ from a Helm chart?

---

*📘 End of Notes — Kubernetes Operators*
