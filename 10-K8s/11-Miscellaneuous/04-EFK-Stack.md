# 📊 EFK Stack in Kubernetes

> **EFK** = **E**lasticsearch + **F**luentd + **K**ibana
> A powerful, popular open-source stack used for **centralized logging** in Kubernetes clusters.

---

## 📌 1. Why Do We Need Centralized Logging?

In a Kubernetes cluster, applications run as **Pods** spread across multiple **Nodes**. This creates logging challenges:

- 🔁 Pods are **ephemeral** — when a Pod dies/restarts, its logs are lost.
- 🖥️ Multiple **nodes** mean logs are scattered everywhere.
- 📈 As the number of microservices grows, manually checking logs (`kubectl logs`) becomes impossible.
- 🔍 We need a **single place** to search, filter, and analyze logs from all Pods.

✅ **Solution:** A centralized logging stack like **EFK** collects, stores, and visualizes logs from the entire cluster in one place.

---

## 🧩 2. Components of the EFK Stack

| Component | Icon | Role |
|-----------|------|------|
| **Elasticsearch** | 🔎 | Stores & indexes log data; enables fast search |
| **Fluentd** | 🚚 | Collects, parses & forwards logs (log shipper/aggregator) |
| **Kibana** | 📊 | Web UI to visualize, search & analyze logs |

---

### 🔎 2.1 Elasticsearch

- A **distributed, RESTful search & analytics engine**.
- Stores logs as **JSON documents** inside **indices**.
- Provides powerful **full-text search**, filtering, and aggregation capabilities.
- Highly **scalable** — runs as a cluster of nodes (shards & replicas).
- Acts as the **database/backend** of the EFK stack.

### 🚚 2.2 Fluentd

- An open-source **data collector** (log forwarder/aggregator).
- Runs as a **DaemonSet** in Kubernetes → ensures **one Fluentd Pod per Node**.
- Reads container logs from:
  ```
  /var/log/containers/*.log
  ```
- **Parses, filters, and enriches** logs (adds metadata like pod name, namespace, container name).
- Sends processed logs to **Elasticsearch**.
- Lightweight alternative: **Fluent Bit** (often used in place of Fluentd for lower resource usage).

### 📊 2.3 Kibana

- A **web-based visualization dashboard** for Elasticsearch data.
- Lets users:
  - 🔍 Search logs using **KQL (Kibana Query Language)**
  - 📈 Build graphs, charts & dashboards
  - ⏱️ Filter logs by time range, namespace, pod, log level, etc.
  - 🚨 Set up alerts on specific log patterns

---

## ⚙️ 3. How EFK Works in Kubernetes (Architecture Flow)

```
   ┌────────────┐      ┌────────────┐      ┌────────────┐      ┌──────────┐
   │  App Pods  │ ───► │  Fluentd   │ ───► │Elasticsearch│ ───► │  Kibana  │
   │ (generate  │      │ (DaemonSet │      │  (stores &  │      │ (visual- │
   │   logs)    │      │  collects) │      │   indexes)  │      │  izes)   │
   └────────────┘      └────────────┘      └────────────┘      └──────────┘
```

### 🔄 Step-by-Step Flow:

1. **📝 Log Generation** — Application containers write logs to `stdout` / `stderr`.
2. **📂 Log Storage on Node** — Kubelet/container runtime writes these logs to files on the node at `/var/log/containers/`.
3. **🚚 Log Collection** — Fluentd (running as a DaemonSet on every node) tails these log files.
4. **🧹 Parsing & Enrichment** — Fluentd parses logs (JSON/regex) and adds Kubernetes metadata (pod name, namespace, labels) using the **Fluentd Kubernetes metadata plugin**.
5. **📤 Forwarding** — Fluentd ships the structured logs to **Elasticsearch**.
6. **🔎 Indexing** — Elasticsearch indexes and stores the logs (e.g., daily indices like `logstash-2026.07.30`).
7. **📊 Visualization** — Kibana connects to Elasticsearch and lets users search/visualize logs in real time.

---

## 🏗️ 4. Kubernetes Deployment Model

| Component | Kubernetes Object Used | Reason |
|-----------|------------------------|--------|
| **Elasticsearch** | `StatefulSet` | Needs stable network identity & persistent storage |
| **Fluentd** | `DaemonSet` | Must run on **every node** to collect all node-level logs |
| **Kibana** | `Deployment` | Stateless UI, can scale independently |

### 📦 Supporting Kubernetes Resources

- **PersistentVolume (PV) / PersistentVolumeClaim (PVC)** 💾 — for Elasticsearch data persistence
- **ConfigMap** 🗂️ — to store Fluentd configuration (parsing rules, output plugins)
- **Service** 🌐 — to expose Elasticsearch & Kibana within/outside the cluster
- **ServiceAccount + RBAC (ClusterRole/ClusterRoleBinding)** 🔐 — Fluentd needs permission to read pod metadata via the Kubernetes API
- **Namespace** 🏷️ — commonly deployed in a dedicated `logging` or `kube-logging` namespace

---

## 🚀 5. Sample Deployment Overview

### 🏷️ Namespace
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: logging
```

### 🔎 Elasticsearch (StatefulSet - simplified)
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: elasticsearch
  namespace: logging
spec:
  serviceName: elasticsearch
  replicas: 3
  selector:
    matchLabels:
      app: elasticsearch
  template:
    metadata:
      labels:
        app: elasticsearch
    spec:
      containers:
        - name: elasticsearch
          image: docker.elastic.co/elasticsearch/elasticsearch:8.13.0
          ports:
            - containerPort: 9200
            - containerPort: 9300
  volumeClaimTemplates:
    - metadata:
        name: es-data
      spec:
        accessModes: ["ReadWriteOnce"]
        resources:
          requests:
            storage: 10Gi
```

### 🚚 Fluentd (DaemonSet - simplified)
```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd
  namespace: logging
spec:
  selector:
    matchLabels:
      app: fluentd
  template:
    metadata:
      labels:
        app: fluentd
    spec:
      serviceAccountName: fluentd
      containers:
        - name: fluentd
          image: fluent/fluentd-kubernetes-daemonset:v1-debian-elasticsearch
          env:
            - name: FLUENT_ELASTICSEARCH_HOST
              value: "elasticsearch.logging.svc.cluster.local"
            - name: FLUENT_ELASTICSEARCH_PORT
              value: "9200"
          volumeMounts:
            - name: varlog
              mountPath: /var/log
      volumes:
        - name: varlog
          hostPath:
            path: /var/log
```

### 📊 Kibana (Deployment - simplified)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kibana
  namespace: logging
spec:
  replicas: 1
  selector:
    matchLabels:
      app: kibana
  template:
    metadata:
      labels:
        app: kibana
    spec:
      containers:
        - name: kibana
          image: docker.elastic.co/kibana/kibana:8.13.0
          ports:
            - containerPort: 5601
          env:
            - name: ELASTICSEARCH_HOSTS
              value: "http://elasticsearch.logging.svc.cluster.local:9200"
```

> 💡 **Note:** These are simplified examples for learning purposes. Production setups need resource limits, security (TLS, auth), persistent volumes, and proper RBAC.

---

## ✅ 6. Advantages of EFK Stack

- 🌍 **Centralized logging** — all logs in one searchable place
- 🔍 **Powerful search** — full-text search across huge log volumes
- 📊 **Rich visualization** — dashboards, graphs, and alerts via Kibana
- 📦 **Kubernetes-native** — Fluentd DaemonSet auto-collects logs from every node
- 🆓 **Open source** — no licensing cost (core features)
- 🔌 **Extensible** — many Fluentd plugins for different sources/outputs

---

## ⚠️ 7. Challenges / Limitations

- 💰 **Resource-heavy** — Elasticsearch needs significant CPU/RAM/storage
- 🛠️ **Complex setup & maintenance** — cluster tuning, index lifecycle management
- 📈 **Scaling issues** — large log volumes can overwhelm Elasticsearch without proper sharding
- 🔐 **Security** — needs extra configuration for authentication, TLS, RBAC
- 🧹 **Index management** — old indices must be cleaned up (via ILM - Index Lifecycle Management) or storage fills up

---

## 🔄 8. EFK vs ELK vs EFK Alternatives

| Stack | Log Shipper | Notes |
|-------|-------------|-------|
| **ELK** | Logstash | Heavier, more resource-intensive shipper |
| **EFK** | Fluentd | Lightweight, Kubernetes-native (CNCF project) ✅ |
| **EFK (Lite)** | Fluent Bit | Even lighter than Fluentd, popular for edge/sidecar use |
| **Loki Stack** | Promtail | Alternative by Grafana Labs — lighter, uses label-based indexing (not full-text) |

> 🏆 **Fluentd** and **Fluent Bit** are both **CNCF (Cloud Native Computing Foundation)** graduated projects, making EFK a very "cloud-native" choice for Kubernetes logging.

---

## 🎯 9. Key Interview / Exam Points

- ❓ **Why DaemonSet for Fluentd?** → Ensures exactly one Fluentd Pod runs per node, so it can collect logs from all Pods on that node via the host's log directory.
- ❓ **Why StatefulSet for Elasticsearch?** → Needs stable pod identity/hostname and persistent storage for its data shards.
- ❓ **Where does Kubernetes store container logs on a node?** → `/var/log/containers/` (symlinked to `/var/log/pods/`).
- ❓ **Difference between Fluentd and Fluent Bit?** → Fluentd is fuller-featured with more plugins; Fluent Bit is lightweight, written in C, ideal for resource-constrained environments.
- ❓ **What replaces Logstash in EFK?** → **Fluentd** (hence "E-F-K" instead of "E-L-K").

---

## 📚 10. Quick Summary

| Question | Answer |
|----------|--------|
| **Full Form** | Elasticsearch + Fluentd + Kibana |
| **Purpose** | Centralized log aggregation & visualization for Kubernetes |
| **Log Collector** | Fluentd (DaemonSet) |
| **Storage/Search Engine** | Elasticsearch (StatefulSet) |
| **Visualization Tool** | Kibana (Deployment) |
| **Deployment Namespace** | Usually `logging` / `kube-logging` |
| **CNCF Project?** | ✅ Yes (Fluentd is a CNCF graduated project) |

---

> 📝 **End of Notes — EFK Stack for Kubernetes**
