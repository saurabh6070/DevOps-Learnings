# 📊 Metrics Server & cAdvisor — Resource Usage Profiling

## 📖 Introduction

Kubernetes does **not** ship with a built-in solution to monitor or analyse the resource usage (CPU/Memory) of Pods and Nodes. To view "live" resource consumption, you need to install a separate, open-source monitoring add-on.

Some popular options for monitoring a Kubernetes cluster include:

- 🟢 **Metrics Server** (lightweight, in-memory, built for basic autoscaling/monitoring)
- 🔶 **Prometheus**
- 🔍 **Elastic Stack (ELK)**
- 🐶 **Datadog**
- 🦄 **Dynatrace**

This note focuses on **Metrics Server**, the simplest and most commonly used option for quick resource visibility.

---

## ⚙️ What is Metrics Server?

**Metrics Server** is a cluster-wide aggregator of resource usage data.

- 🧠 It is an **in-memory** metrics server — it does **not** store any data on disk.
- ⏳ Because nothing is persisted, Metrics Server provides **only real-time (current) metrics** — it does **not** provide historical data.
- 📈 If you need historical trends and long-term analysis, you must use a full monitoring stack like Prometheus, Elastic Stack, Datadog, or Dynatrace instead.

> 💡 **Key takeaway:** Metrics Server = live snapshot of resource usage. Not a replacement for full observability tools.

---

## 🕵️ Role of cAdvisor (Container Advisor)

- **cAdvisor (Container Advisor)** is a component built into the **Kubelet** running on every node.
- 📡 cAdvisor continuously collects **container-level metrics** (CPU, memory, etc.) from the Kubelet and feeds this data to the **Metrics Server in real time**.
- 🔄 Data flow: `Containers → cAdvisor (inside Kubelet) → Metrics Server → kubectl top`

---

## 🛠️ Installing Metrics Server

The installation steps differ depending on your environment.

### ▶️ Option 1: Minikube

```bash
minikube addons enable metrics-server
```

### ▶️ Option 2: Other Environments (Generic)

```bash
git clone https://github.com/kubernetes-incubator/metrics-server
```

### ▶️ Option 3: Main / Recommended Method (KodeKloud Repo)

```bash
git clone https://github.com/kodekloudhub/kubernetes-metrics-server.git
cd kubernetes-metrics-server
kubectl create -f .
```

> ⚠️ **Note:** Right after installation, Metrics Server needs a short warm-up period to start collecting data. Running `kubectl top` immediately may return an error — see below.

---

## 📉 Viewing Resource Usage with `kubectl top`

Once Metrics Server is installed and running, you can check live resource consumption of Nodes and Pods.

### 🖥️ Monitor Node CPU/Memory Consumption

```bash
kubectl top node
```

### 📦 Monitor Pod CPU/Memory Consumption

```bash
kubectl top pods
```

---

## 🧪 Sample Output / Logs

Right after installing Metrics Server, the metrics API may not be ready yet:

```bash
$ kubectl top node
error: metrics not available yet
```

⏱️ Wait a few moments, then retry. Once ready, you'll see actual usage data:

```bash
$ kubectl top node
NAME           CPU(cores)   CPU%   MEMORY(bytes)   MEMORY%
controlplane   324m         0%     1146Mi           0%
node01         263m         0%     295Mi            0%
```

```bash
$ kubectl top pods
NAME       CPU(cores)   MEMORY(bytes)
elephant   15m          31Mi
lion       1m           18Mi
rabbit     112m         252Mi
```

---

## 🗂️ Quick Recap

| Concept | Details |
|---|---|
| 🚫 Built-in monitoring | Not available by default in Kubernetes |
| 🧰 Common tools | Metrics Server, Prometheus, Elastic Stack, Datadog, Dynatrace |
| 💾 Metrics Server storage | In-memory only — **no disk storage** |
| 🕓 Historical data | ❌ Not supported by Metrics Server |
| 🔌 Data source | cAdvisor (inside Kubelet) → Metrics Server |
| 📟 Commands | `kubectl top node`, `kubectl top pods` |
| ⏳ First run | May show `metrics not available yet` — wait and retry |

---

## ❓ Frequently Asked Questions (For Revision)

**Q1. Does Kubernetes provide monitoring out of the box?**
No. You must install a separate add-on such as Metrics Server, Prometheus, or Elastic Stack.

**Q2. Why can't Metrics Server show historical/past usage data?**
Because it is an in-memory server and does not persist any data to disk — it only reflects real-time metrics.

**Q3. What is cAdvisor and where does it run?**
cAdvisor (Container Advisor) is a component embedded within the Kubelet on each node. It collects container-level metrics and forwards them to the Metrics Server.

**Q4. Which command shows Node-level resource usage? Which shows Pod-level?**
- Node level → `kubectl top node`
- Pod level → `kubectl top pods`

**Q5. Why might `kubectl top node` fail right after installation?**
Metrics Server needs a short time to start scraping and aggregating data; until then, it returns `error: metrics not available yet`.
