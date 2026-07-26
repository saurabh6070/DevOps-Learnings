# 🕸️ Weave Net — CNI Plugin Deep Dive

**Weave Net** is one of the earliest and most popular **third-party CNI plugins** for Kubernetes, designed to create a simple, resilient virtual network connecting containers across multiple nodes — without requiring complex external routing configuration.

> 📌 **Recap:** As covered earlier, CNI plugins are responsible for satisfying Kubernetes' core networking model (unique pod IPs, NAT-free pod-to-pod communication) — Weave Net is one specific implementation of that contract.

---

## 🧠 1. What Is Weave Net?

- 🏢 Developed by **Weaveworks**.
- 🌐 Creates a **virtual, software-defined network** across all nodes in the cluster.
- 🔗 Each pod gets a **unique IP** from Weave's own address space, and can communicate with **any other pod**, on **any node**, **without needing manual routing tables** configured on each node.
- 🧩 Implements the **CNI** interface — Kubernetes invokes Weave the same way it invokes Bridge, Calico, Flannel, or any other CNI plugin.

---

## 🏗️ 2. Core Architecture

### 🕵️ 2.1 Weave Agent (weave pod) Per Node
- Weave Net runs as a **pod on every node** (a DaemonSet), often visible as `weave-net-xxxxx` pods in the `kube-system` namespace.
- Each Weave agent is responsible for networking on its own node and **communicates with Weave agents on other nodes** to build a full mesh understanding of the cluster network.

### 🌉 2.2 Weave Bridge on Each Node
- On every node, Weave creates its own **bridge interface**, similar in concept to Docker's `docker0`, but managed by Weave.
- All pod veth pairs on that node connect into this **Weave bridge**.

### 🚇 2.3 Mesh Overlay Network Between Nodes
Instead of requiring the underlying physical network to know how to route pod-subnet traffic (as plain routing-based CNI setups need), Weave creates an **overlay network**:

- 📦 Traffic between pods on **different nodes** is **encapsulated** by the sending node's Weave agent.
- 🚚 The encapsulated packet is carried across the existing physical network to the destination node — the underlying network only ever sees traffic between **node IPs**, not pod IPs.
- 📭 The receiving node's Weave agent **decapsulates** the packet and delivers it to the correct local pod via the bridge.

```
Pod A (Node 1)                              Pod B (Node 2)
     │                                           │
   veth                                        veth
     │                                           │
 Weave Bridge (Node 1)                  Weave Bridge (Node 2)
     │                                           │
 Weave Agent (encapsulate) ──▶ Physical Network ──▶ Weave Agent (decapsulate)
```

> 💡 This is why Weave Net requires **no manual route configuration** on routers/switches — it tunnels pod traffic transparently between nodes.

### 🔀 2.4 Two Data-Path Modes
Weave Net can move packets between nodes in two different ways:

| Mode | ⚙️ How It Works | ⚡ Performance |
|---|---|---|
| **Sleeve mode** (fallback) | Encapsulates packets in **UDP**, works over almost any network (even with restrictive firewalls/NAT) | Slower — more overhead |
| **Fast Data Path** (default when possible) | Uses the Linux kernel's **Open vSwitch Datapath (ODP)** with **VXLAN** encapsulation, bypassing userspace processing | Much faster — near-native throughput |

> 🧭 Weave automatically **falls back to Sleeve mode** if Fast Data Path can't be established (e.g., due to network restrictions), and can even do this **per node-pair**.

---

## 🗺️ 3. IP Address Management (IPAM)

- Weave Net manages **its own IP address allocation** across the cluster, without needing an external IPAM plugin.
- It divides a configured IP range among all nodes and **automatically discovers** how it's been allocated across the cluster.
- Weave ensures **no IP collisions**, even if nodes join/leave dynamically or if there's a temporary network partition — it reconciles allocation once nodes reconnect.

---

## 🔒 4. Network Policy Support

- Weave Net includes **built-in support for Kubernetes NetworkPolicy** resources (unlike some simpler CNI plugins that require Weave/Calico combos).
- This means you can define **ingress/egress rules** restricting which pods can talk to which — Weave enforces these rules directly at the node level using iptables rules it manages.

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-only
spec:
  podSelector:
    matchLabels:
      app: backend
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
```

➡️ With Weave installed, this policy is automatically enforced without needing any additional plugin.

---

## 🧰 5. Installing Weave Net

Weave Net is typically installed as a single manifest applied to the cluster:

```bash
kubectl apply -f "https://cloud.weave.works/k8s/net?k8s-version=$(kubectl version | base64 | tr -d '\n')"
```

> ⚠️ This URL-based install method was Weave's classic approach; always check the **current official Weaveworks documentation** for the up-to-date install command/manifest, as hosted install URLs can change or be deprecated over time.

After installation, verify:

```bash
kubectl get pods -n kube-system | grep weave
```
➡️ You should see one `weave-net-xxxxx` pod **per node**, all in `Running` state.

---

## 🩺 6. Basic Troubleshooting Commands

| Command | 🔍 Purpose |
|---|---|
| `kubectl get pods -n kube-system -o wide \| grep weave` | Confirm a Weave pod is running healthy on every node |
| `kubectl logs -n kube-system <weave-pod-name> -c weave` | Check Weave agent logs for connectivity errors |
| `kubectl exec -n kube-system <weave-pod-name> -c weave -- /home/weave/weave --local status` | View Weave's internal status, peers, and connections |
| `kubectl exec -n kube-system <weave-pod-name> -c weave -- /home/weave/weave --local status connections` | List connections to other node's Weave agents (and whether Fast Data Path or Sleeve mode is used) |

---

## ⚖️ 7. Weave Net vs Other CNI Plugins (Quick Comparison)

| CNI Plugin | 🔗 Networking Approach | 🔒 NetworkPolicy Support | 🧭 Notable Trait |
|---|---|---|---|
| **Weave Net** | Overlay (VXLAN / UDP mesh) | ✅ Built-in | Simple setup, resilient mesh, no external routing needed |
| **Flannel** | Overlay (VXLAN, typically) | ❌ (needs Calico for policies — "Canal") | Lightweight, simple, minimal features beyond basic connectivity |
| **Calico** | Routing-based (BGP) or overlay (IP-in-IP/VXLAN) | ✅ Advanced policies | High performance, rich policy engine, popular in production |
| **Cilium** | eBPF-based | ✅ Advanced (L3–L7) | Deep observability, high performance, modern eBPF architecture |

---

## 📚 8. Summary Cheat Sheet

| Concept | 🔑 Key Point |
|---|---|
| What it is | A CNI plugin creating a resilient mesh overlay network across nodes |
| Runs as | A DaemonSet pod (`weave-net`) on every node |
| Per-node component | Weave bridge + Weave agent |
| Cross-node transport | Overlay network — encapsulation/decapsulation of pod traffic |
| Data path modes | **Sleeve** (UDP, fallback, slower) vs **Fast Data Path** (VXLAN/ODP, faster) |
| IPAM | Self-managed, automatic, collision-free across the cluster |
| NetworkPolicy | ✅ Supported natively, enforced via iptables |
| Install | Single manifest applied via `kubectl apply` |

> 🎓 **Key takeaway:** Weave Net solves cross-node pod networking by building a **self-organizing mesh overlay** between all nodes — requiring zero manual routing configuration — while also providing built-in IPAM and NetworkPolicy enforcement, making it one of the simplest "batteries-included" CNI options to get a cluster networking correctly out of the box.
