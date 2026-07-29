# 📊 Prometheus & Grafana in Kubernetes

> A complete reference guide covering monitoring and visualization for Kubernetes clusters using **Prometheus** (metrics collection & alerting) and **Grafana** (visualization & dashboards).

---

## 📌 1. Overview

| Tool | Purpose | Role |
|------|----------|------|
| 🔥 **Prometheus** | Metrics collection, storage, querying & alerting | Monitoring engine |
| 📈 **Grafana** | Visualization & dashboarding | UI/Analytics layer |
| 🚨 **Alertmanager** | Routes & manages alerts fired by Prometheus | Notification engine |

**Why use them together in Kubernetes?**
- Kubernetes clusters are dynamic (pods scale, restart, move nodes) — Prometheus's **pull-based, service-discovery-driven** model fits this perfectly.
- Grafana turns raw Prometheus metrics into human-readable, real-time dashboards.
- Together they form the industry-standard **CNCF observability stack** for K8s.

---

## 🏗️ 2. Architecture in a Kubernetes Cluster

```
                ┌───────────────────────────┐
                │        Grafana            │
                │  (Dashboards / Alerts UI) │
                └─────────────▲─────────────┘
                              │ PromQL queries
                ┌─────────────┴─────────────┐
                │        Prometheus         │
                │  (Scrapes & stores metrics)│
                └───▲─────────▲─────────▲────┘
                    │         │         │
         ┌──────────┘   ┌─────┘     ┌───┘
         │               │            │
   ┌─────┴─────┐   ┌─────┴─────┐ ┌────┴──────┐
   │ Node       │   │ kube-state│ │ App Pods   │
   │ Exporter   │   │ -metrics  │ │ (/metrics) │
   └────────────┘   └───────────┘ └────────────┘
```

### 🔑 Key Components

- **🎯 Prometheus Server** — scrapes and stores time-series metrics.
- **📤 Exporters** — expose metrics in Prometheus format:
  - `node-exporter` → node/host-level metrics (CPU, memory, disk)
  - `kube-state-metrics` → K8s object state (Deployments, Pods, ReplicaSets, etc.)
  - `cAdvisor` (built into kubelet) → container resource usage
- **🚨 Alertmanager** — deduplicates, groups, and routes alerts (Slack, email, PagerDuty, etc.)
- **📈 Grafana** — queries Prometheus and renders dashboards.
- **🧭 Service Discovery** — Prometheus auto-discovers scrape targets via the Kubernetes API (Pods, Services, Endpoints, Nodes).

---

## ⚙️ 3. Prometheus in Kubernetes

### 3.1 🔍 How Metric Collection Works

Prometheus uses **service discovery + relabeling** instead of static configs:

1. Queries the K8s API server for Pods/Services/Endpoints.
2. Filters targets using **annotations** or **CRDs** (`ServiceMonitor` / `PodMonitor`).
3. Scrapes the `/metrics` HTTP endpoint on each target at a defined interval.
4. Stores results as time-series data with labels (`pod`, `namespace`, `job`, etc.).

**Example pod annotations for auto-scraping (legacy method):**
```yaml
metadata:
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "9100"
    prometheus.io/path: "/metrics"
```

### 3.2 🧩 ServiceMonitor & PodMonitor (Prometheus Operator CRDs)

When using the **Prometheus Operator**, scrape configuration is done declaratively via CRDs instead of editing `prometheus.yml` manually.

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: my-app-monitor
  labels:
    release: prometheus
spec:
  selector:
    matchLabels:
      app: my-app
  endpoints:
    - port: metrics
      interval: 30s
      path: /metrics
```

> 💡 **PodMonitor** works the same way but targets Pods directly (useful when there's no Service in front of them).

### 3.3 📦 Installation Options

| Method | Description |
|--------|-------------|
| 🎁 **kube-prometheus-stack (Helm)** | Recommended — bundles Prometheus, Grafana, Alertmanager, exporters & CRDs |
| 🛠️ **Prometheus Operator** | Manages Prometheus as a Kubernetes-native resource |
| 📄 **Manual YAML manifests** | Full control, more maintenance overhead |

**Quick install via Helm:**
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm install monitoring prometheus-community/kube-prometheus-stack \
  --namespace monitoring --create-namespace
```

### 3.4 🗃️ Storage & Retention

- Default storage: local TSDB (Time Series Database) on disk via `PersistentVolumeClaim`.
- Default retention: **15 days** (configurable via `--storage.tsdb.retention.time`).
- For long-term storage, integrate with **Thanos**, **Cortex**, or **Mimir**.

### 3.5 📝 PromQL Basics (Prometheus Query Language)

| Query | Meaning |
|-------|---------|
| `up` | Shows which targets are up (1) or down (0) |
| `node_memory_MemAvailable_bytes` | Available memory per node |
| `rate(container_cpu_usage_seconds_total[5m])` | CPU usage rate over 5 minutes |
| `sum(kube_pod_status_phase{phase="Running"}) by (namespace)` | Running pods grouped by namespace |
| `kube_deployment_status_replicas_unavailable > 0` | Detect unhealthy deployments |

---

## 📈 4. Grafana in Kubernetes

### 4.1 📥 Installation

Grafana is typically installed alongside Prometheus via `kube-prometheus-stack`, or standalone:

```bash
helm repo add grafana https://grafana.github.io/helm-charts
helm install grafana grafana/grafana --namespace monitoring
```

**Retrieve the default admin password:**
```bash
kubectl get secret grafana -n monitoring \
  -o jsonpath="{.data.admin-password}" | base64 --decode
```

### 4.2 🔌 Connecting Grafana to Prometheus (Data Source)

```yaml
apiVersion: 1
datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus-operated.monitoring.svc:9090
    isDefault: true
```

### 4.3 📊 Pre-built Dashboards (Grafana.com IDs)

| Dashboard | ID | Use Case |
|-----------|----|----|
| Kubernetes Cluster Monitoring | `315` | Cluster-wide overview |
| Node Exporter Full | `1860` | Node-level resource metrics |
| Kubernetes Pods | `6417` | Pod-level CPU/memory |
| Kube-state-metrics | `13332` | K8s object health |

> 💡 Import via **Grafana UI → Dashboards → Import → Enter Dashboard ID**.

### 4.4 🗂️ Dashboard-as-Code (ConfigMap Provisioning)

Dashboards can be version-controlled and auto-loaded via `ConfigMaps` labeled for the Grafana sidecar:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: my-dashboard
  labels:
    grafana_dashboard: "1"
data:
  my-dashboard.json: |
    { ... dashboard JSON ... }
```

---

## 🚨 5. Alerting with Alertmanager

### 5.1 Defining Alert Rules (PrometheusRule CRD)

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: high-cpu-alert
  labels:
    release: prometheus
spec:
  groups:
    - name: cpu-alerts
      rules:
        - alert: HighCPUUsage
          expr: sum(rate(container_cpu_usage_seconds_total[5m])) by (pod) > 0.9
          for: 5m
          labels:
            severity: critical
          annotations:
            summary: "High CPU usage detected on {{ $labels.pod }}"
```

### 5.2 🔔 Routing Alerts (Alertmanager Config)

```yaml
route:
  receiver: "slack-notifications"
  group_by: ["alertname", "namespace"]
receivers:
  - name: "slack-notifications"
    slack_configs:
      - api_url: "https://hooks.slack.com/services/XXX"
        channel: "#alerts"
```

---

## 🔐 6. Security & RBAC Considerations

- ✅ Run Prometheus with a dedicated `ServiceAccount` and minimal `ClusterRole` (read-only access to pods, services, endpoints).
- ✅ Restrict Grafana admin access; use **OAuth/LDAP/SSO** integration for teams.
- ✅ Expose Grafana via `Ingress` with TLS — never expose Prometheus directly to the internet.
- ✅ Use `NetworkPolicies` to limit which namespaces can be scraped/accessed.
- ✅ Store secrets (Slack webhooks, DB passwords) using `Secrets`, not plain ConfigMaps.

---

## 🧰 7. Best Practices

- 📏 **Right-size retention & storage** — use remote-write to Thanos/Mimir for long-term data instead of growing local disk indefinitely.
- 🏷️ **Consistent labeling** — standardize `namespace`, `app`, `team` labels across all workloads for easier querying.
- 🎯 **Use ServiceMonitors over annotations** when running Prometheus Operator — more maintainable at scale.
- 🚦 **Set meaningful alert thresholds** — avoid alert fatigue; use `for:` durations to prevent flapping alerts.
- 📊 **Organize Grafana dashboards by folders/teams** for large clusters.
- 🔄 **GitOps your monitoring stack** — manage Helm values, ServiceMonitors, and dashboards as code (ArgoCD/Flux).
- 🧪 **Test alerts in staging** before enabling in production.

---

## 🧾 8. Handy Cheat Sheet — kubectl Commands

```bash
# Check Prometheus pods
kubectl get pods -n monitoring

# Port-forward Prometheus UI
kubectl port-forward svc/prometheus-operated 9090:9090 -n monitoring

# Port-forward Grafana UI
kubectl port-forward svc/grafana 3000:80 -n monitoring

# View ServiceMonitors
kubectl get servicemonitors -n monitoring

# View PrometheusRules (alerts)
kubectl get prometheusrules -n monitoring

# Check Alertmanager status
kubectl port-forward svc/alertmanager-operated 9093:9093 -n monitoring
```

---

## 📚 9. Quick Recap

| Concept | Key Takeaway |
|---------|--------------|
| 🔥 Prometheus | Pull-based metrics collection using K8s service discovery |
| 🧩 ServiceMonitor/PodMonitor | Declarative scrape config via CRDs |
| 📈 Grafana | Visualizes Prometheus data via dashboards |
| 🚨 Alertmanager | Routes alerts to Slack/Email/PagerDuty |
| 📦 kube-prometheus-stack | Easiest way to deploy the full stack via Helm |

---

## 🔗 10. References

- Prometheus Docs: https://prometheus.io/docs/
- Grafana Docs: https://grafana.com/docs/
- kube-prometheus-stack (Helm chart): https://github.com/prometheus-community/helm-charts
- Prometheus Operator: https://prometheus-operator.dev/
