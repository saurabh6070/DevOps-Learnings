# 📊 ELK Stack on Kubernetes — Complete Student Notes

> A structured guide to understanding and deploying the **ELK Stack (Elasticsearch, Logstash, Kibana)** for centralized logging inside **Kubernetes** clusters.

---

## 📖 1. Introduction

Kubernetes runs applications as distributed **pods** spread across multiple **nodes**. Every pod produces its own logs, and these logs are:

- 🔥 **Ephemeral** — lost when a pod restarts, crashes, or gets rescheduled
- 📦 **Distributed** — scattered across many nodes and namespaces
- 🌊 **High-volume** — hundreds/thousands of containers generating logs continuously

Manually running `kubectl logs` on every pod does not scale. This is where the **ELK Stack** comes in — it collects, stores, and visualizes logs from an entire cluster in **one centralized place**.

---

## 🧩 2. What is the ELK Stack?

**ELK** is an acronym for three open-source tools developed by **Elastic**:

| Letter | Tool | Purpose |
|--------|------|---------|
| **E** | Elasticsearch | Stores, indexes, and searches log data |
| **L** | Logstash | Collects, parses, transforms, and forwards logs |
| **K** | Kibana | Visualizes data through dashboards and charts |

> 💡 **Note:** When **Beats** (lightweight log shippers) are added to the stack, it is officially called the **Elastic Stack**.

---

## ⚙️ 3. Core Components Explained

### 🔍 3.1 Elasticsearch — The Storage & Search Engine
- A distributed, JSON-based search and analytics engine.
- Stores logs as structured, searchable **documents** inside **indices**.
- Runs as a **StatefulSet** in Kubernetes (needs stable network identity + persistent storage).
- Supports horizontal scaling via multiple nodes/shards for high availability.

### 🔄 3.2 Logstash — The Processing Pipeline
- An ETL (Extract–Transform–Load) engine with a **3-stage pipeline**:
  1. **Input** — receives raw logs (from Filebeat, files, etc.)
  2. **Filter** — parses, enriches, and structures the data (e.g., using `grok`, `json`, `kubernetes_metadata`)
  3. **Output** — forwards the processed data (usually to Elasticsearch)
- Can run multiple isolated pipelines in parallel (e.g., separate pipelines for logs vs. metrics).
- Typically deployed as a **Deployment** in Kubernetes.

### 📈 3.3 Kibana — The Visualization Layer
- Web UI for exploring Elasticsearch data.
- Provides dashboards, real-time search, filters, and alerting integrations.
- Deployed as a **Deployment + Service** (often exposed via Ingress).

### 🚚 3.4 Beats / Filebeat — The Lightweight Shipper
- **Filebeat** is a lightweight agent that tails log files and ships them onward.
- Tracks read position so no logs are lost on restart.
- Comes with pre-built **modules** for common formats (NGINX, MySQL, Kubernetes, AWS, etc.) that auto-configure parsing and dashboards.
- Deployed as a **DaemonSet** — ensuring **one Filebeat pod runs on every node** to capture all container logs on that node.

---

## 🏗️ 4. ELK Architecture in Kubernetes

### 🔗 Standard Log Flow

```
Application Pods
      │  (writes logs to stdout/stderr)
      ▼
/var/log/containers/*.log (on each Node)
      │
      ▼
Filebeat (DaemonSet — 1 pod per Node)
      │  (tails + ships logs)
      ▼
Logstash (Deployment — parses & enriches)
      │
      ▼
Elasticsearch (StatefulSet — stores & indexes)
      │
      ▼
Kibana (Deployment — dashboards & search)
      │
      ▼
Alerting Tools (e.g., ElastAlert2 → Slack/Email/PagerDuty)
```

### 📌 Why Logs Need a Shipping Layer
Since container logs live at the node/runtime level and disappear when a pod dies, Kubernetes needs an agent (Filebeat/Fluentd) on **every node** to continuously collect and forward logs before they're lost.

---

## 🚀 5. Deploying ELK on Kubernetes

There are three common approaches:

### 🅰️ 5.1 Using Helm Charts (Most Common)
Elastic provides official Helm charts for quick, repeatable deployment.

```bash
# Add the official Elastic Helm repository
helm repo add elastic https://helm.elastic.co
helm repo update

# Create a dedicated namespace
kubectl create namespace logging

# Install Elasticsearch
helm install elasticsearch elastic/elasticsearch -n logging

# Install Kibana
helm install kibana elastic/kibana -n logging

# Install Filebeat (DaemonSet)
helm install filebeat elastic/filebeat -n logging

# Install Logstash
helm install logstash elastic/logstash -n logging
```

### 🅱️ 5.2 Using ECK (Elastic Cloud on Kubernetes) Operator
- A **Kubernetes Operator** that manages Elasticsearch, Kibana, and Beats as native Custom Resources (CRDs).
- Handles scaling, upgrades, TLS, and failover automatically.
- Best suited for **production-grade**, self-managed clusters.

### 🅲️ 5.3 Using Raw YAML Manifests
- Manually defining `StatefulSet`, `DaemonSet`, `Deployment`, `Service`, `ConfigMap`, and `PVC` objects.
- Offers maximum control but requires more manual maintenance.

---

## 🗂️ 6. Key Kubernetes Objects Used by ELK

| Kubernetes Object | Used For |
|--------------------|---------|
| 🧱 **StatefulSet** | Elasticsearch (stable pod identity + persistent storage) |
| 🛰️ **DaemonSet** | Filebeat/Fluentd (one log-collector pod per node) |
| 📦 **Deployment** | Logstash, Kibana (stateless components) |
| 💾 **PersistentVolumeClaim (PVC)** | Storing Elasticsearch index data durably |
| 🗺️ **ConfigMap** | Storing Logstash/Filebeat pipeline configurations |
| 🔐 **Secret** | Storing credentials and TLS certificates |
| 🌐 **Service** | Internal communication (e.g., `elasticsearch.logging.svc`) |
| 🚪 **Ingress** | Exposing the Kibana dashboard externally |

---

## 📝 7. Sample Filebeat Kubernetes Config (DaemonSet Snippet)

```yaml
filebeat.autodiscover:
  providers:
    - type: kubernetes
      node: ${NODE_NAME}
      hints.enabled: true

output.logstash:
  hosts: ["logstash.logging.svc:5044"]
```

## 📝 8. Sample Logstash Pipeline (Input → Filter → Output)

```conf
input {
  beats {
    port => 5044
  }
}

filter {
  json {
    source => "message"
  }
  kubernetes_metadata {}
}

output {
  elasticsearch {
    hosts => ["elasticsearch.logging.svc:9200"]
    index => "k8s-logs-%{+YYYY.MM.dd}"
  }
}
```

---

## ✅ 9. Best Practices for ELK on Kubernetes

- 📐 **Log in structured JSON** from applications instead of free-text — makes parsing reliable.
  ```
  ❌ Bad:  logger.info(f"User {id} placed order {order_id}")
  ✅ Good: logger.info("order_placed", extra={"user_id": id, "order_id": order_id})
  ```
- 🧭 Use **index lifecycle management (ILM)** to roll over and delete old indices automatically.
- 🔒 Enable **TLS + authentication** between Filebeat, Logstash, and Elasticsearch.
- 📊 Set proper **resource requests/limits** (CPU/memory) on Elasticsearch pods to avoid OOM kills.
- 🌍 Use **node affinity / anti-affinity** to spread Elasticsearch pods across nodes for high availability.
- 🧹 Apply **retention policies** to control storage cost and index growth.
- 🚨 Integrate with alerting tools (e.g., **ElastAlert2**) for proactive incident detection.
- 🔁 Prefer **Filebeat/Fluentd/Vector** over heavier custom shippers for lower resource overhead.

---

## ⚖️ 10. ELK vs. Alternatives (Quick Comparison)

| Feature | Logstash | Fluentd | Vector |
|---------|----------|---------|--------|
| 🏢 Origin | Elastic | CNCF (Kubernetes-native) | Rust-based, high performance |
| ⚡ Resource Usage | Heavier (JVM-based) | Lightweight | Very lightweight |
| 🔌 Plugin Ecosystem | Extensive | Extensive | Growing |
| 🎯 Best Fit | Complex transformations | Native k8s logging | High-throughput pipelines |

---

## 🎯 11. Common Use Cases

- 🐞 **Debugging microservices** — trace an error across dozens of pods instantly
- ⏱️ **Reducing MTTR** (Mean Time To Recovery) during incidents
- 📉 **Real-time dashboards** for service health and error rates
- 🔍 **Security & audit log analysis**
- 📢 **Automated alerting** on error spikes or anomalies

---

## 🌟 12. Advantages of ELK on Kubernetes

- ✅ Centralized, searchable view of logs from the entire cluster
- ✅ Scales horizontally with cluster growth
- ✅ Rich visualization and dashboarding via Kibana
- ✅ Wide plugin/module ecosystem for parsing common log formats
- ✅ Strong community and enterprise support

## ⚠️ 13. Challenges to Keep in Mind

- ⚠️ Elasticsearch can be **resource-heavy** (JVM heap, storage I/O)
- ⚠️ Requires careful **capacity planning** for high log volumes
- ⚠️ Operational overhead of managing Elasticsearch cluster health (shards, replicas)
- ⚠️ Security configuration (TLS, RBAC, authentication) needs deliberate setup

---

## 🧠 14. Quick Recap (Summary Table)

| Concept | Key Takeaway |
|---------|---------------|
| 🔤 ELK | Elasticsearch + Logstash + Kibana |
| 🚚 Log Shipper | Filebeat (DaemonSet, one per node) |
| 🗃️ Storage | Elasticsearch (StatefulSet) |
| 🔧 Processing | Logstash (input → filter → output) |
| 📊 Visualization | Kibana dashboards |
| 🚀 Deployment | Helm charts / ECK Operator / raw YAML |
| 🎯 Goal | Centralized, searchable, real-time cluster logging |

---

## 📚 15. Suggested Practice Steps for Students

1. 🎓 Spin up a local Kubernetes cluster (Minikube / Kind).
2. 🎓 Deploy Elasticsearch + Kibana using the official Helm chart.
3. 🎓 Deploy Filebeat as a DaemonSet and point it to Logstash/Elasticsearch.
4. 🎓 Generate sample application logs and verify they appear in Kibana.
5. 🎓 Build a simple Kibana dashboard to visualize error rates.

---

*📌 End of Notes — ELK Stack on Kubernetes*
