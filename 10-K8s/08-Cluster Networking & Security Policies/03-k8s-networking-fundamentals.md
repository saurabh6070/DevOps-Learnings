# ☸️ Kubernetes Networking Fundamentals: Pod-to-Pod & Pod-to-Service

Kubernetes networking builds directly on the Linux networking primitives (namespaces, veth pairs, bridges, iptables) and the CNI standard covered earlier. This guide covers the **core principles** that make cluster-wide networking work — how pods talk to each other, and how they talk via Services.

> 📌 **Scope note:** This document focuses on the *fundamental model* of Kubernetes networking. The various **CNI plugin implementations** (Calico, Flannel, Weave, Cilium, etc.) and **Service types** (ClusterIP, NodePort, LoadBalancer) are covered in separate topics.

---

## 📜 1. The Kubernetes Networking Model — Core Rules

Kubernetes imposes a strict, simple networking model that every CNI plugin must satisfy. There are **three fundamental requirements**:

| # | 📏 Rule | 💬 Meaning |
|---|---|---|
| 1️⃣ | Every **pod gets its own unique IP address** | No NAT needed between pods |
| 2️⃣ | **All pods can communicate with all other pods** without NAT | Pod IP as seen by itself = Pod IP as seen by others |
| 3️⃣ | **All nodes can communicate with all pods** without NAT | And vice versa |

> 💡 This is often summarized as: **"IP-per-pod"** — every pod behaves like a full-fledged VM or host on the network, each with its own IP, own port range, and no port-conflict issues between pods (unlike Docker's default bridge networking limitations).

### 🚫 What Kubernetes Does NOT Define
Kubernetes **does not dictate how** this model is implemented — that's left entirely to the **CNI plugin**. It only defines the *contract* — the plugin decides the underlying mechanism (overlay network, routing, VXLAN, BGP, etc.).

---

## 🧱 2. Networking Building Blocks Recap

Before pod-to-pod communication happens, a few things are already in place on every node (as covered in earlier Linux networking / CNI topics):

- 🧪 Each **pod runs in its own network namespace**.
- 🔗 A **veth pair** connects the pod's namespace to the node's root namespace.
- 🌉 The node-side end of each veth pair attaches to a **bridge** (or equivalent construct, depending on the CNI plugin).
- 🏷️ The **CNI plugin** assigns an IP address to each pod when it's created.

---

## 🔁 3. Pod-to-Pod Communication

### 🏠 3.1 Same Node Communication

When two pods are scheduled on the **same node**:

1. Each pod has its own network namespace with a **veth pair** connecting it to the node's bridge.
2. Both veth pairs attach to the **same bridge** on that node.
3. The bridge acts as a **virtual switch** — traffic between the two pods simply flows through the bridge, like two devices plugged into the same physical switch.

```
Pod A (10.244.1.2) ── veth ──┐
                              ├── bridge (cbr0 / docker0-like) ── Node
Pod B (10.244.1.3) ── veth ──┘
```

➡️ No routing between nodes is needed — it's purely local, layer-2 style communication via the bridge.

---

### 🌍 3.2 Cross-Node Communication

When two pods are on **different nodes**, things get more interesting — because each node typically has its **own private bridge subnet** (e.g., Node1's pods = `10.244.1.0/24`, Node2's pods = `10.244.2.0/24`).

For Pod A (on Node 1) to reach Pod B (on Node 2), the traffic must:

1. Leave Pod A's namespace via its veth pair → reach Node 1's bridge.
2. Get **routed out of Node 1** toward Node 2 (since the destination subnet isn't local to Node 1).
3. Travel across the **underlying physical/network infrastructure** connecting the nodes.
4. Arrive at Node 2, get routed into Node 2's bridge.
5. Reach Pod B via its veth pair.

🗺️ **This is exactly where the CNI plugin's real value comes in** — it's responsible for making sure every node knows how to route to every other node's pod subnet. Common approaches (implementation details, covered separately):
- 📡 Maintaining **routing tables** across nodes (all nodes aware of all pod subnets).
- 🎁 Using an **overlay network** that encapsulates pod traffic to tunnel it between nodes.
- 🔀 Using **BGP** or similar protocols to advertise pod-subnet routes across the network.

> ✅ Regardless of the underlying mechanism, the **result must obey Rule #2** from the core model above: Pod A can reach Pod B directly by its IP, with **no NAT** in between.

---

## 🔀 4. The Problem Pod-to-Pod Alone Doesn't Solve

Pod IPs are **not stable** — pods are ephemeral:
- 🔄 Pods get **recreated** on failure, restarts, or rescheduling.
- 🆕 Each time a pod is recreated, it typically gets a **new IP address**.
- 📈 With **ReplicaSets/Deployments**, there are often **multiple pod replicas** — a client shouldn't need to know each individual pod IP.

➡️ If applications relied purely on direct pod IPs, connections would constantly break, and there'd be no way to **load balance** across replicas. This is the exact gap that **Services** are designed to fill.

---

## 🧭 5. Pod-to-Service Communication

### 🎯 5.1 What a Service Provides

A **Service** is a **stable networking abstraction** in front of a dynamic set of pods. It provides:

- 🏷️ A **fixed virtual IP** (ClusterIP) that never changes, regardless of which/how many pods are behind it.
- 🎛️ **Load balancing** across all matching pod replicas.
- 🔍 **Service discovery** — other pods can reach it by a **stable DNS name** instead of an IP.

```
Client Pod ──▶ Service (stable VIP: 10.96.0.15) ──▶ Pod A / Pod B / Pod C (rotating)
```

---

### 🧩 5.2 How Kubernetes Tracks Which Pods Belong to a Service

- A Service selects pods using **label selectors** (matching pod labels, e.g., `app: web`).
- Kubernetes continuously maintains an up-to-date list of matching pod IPs — this list is exposed internally via an object called an **Endpoints** (or **EndpointSlice**) object.
- As pods come and go (scale up/down, crash/restart), the Endpoints list is **automatically updated** — the Service's virtual IP itself **never changes**.

---

### ⚙️ 5.3 How Traffic Actually Gets Routed: kube-proxy

The **Service's virtual IP (ClusterIP) doesn't belong to any real interface** — it's a purely virtual construct. So how does traffic sent to it actually reach a real pod?

This is handled by **`kube-proxy`**, a component running on **every node**, which:

1. 👀 **Watches** the Kubernetes API for Services and Endpoints changes.
2. 🧾 Programs the node's **`iptables`** (or **IPVS**, depending on mode) rules to intercept traffic destined for the Service's ClusterIP.
3. 🔀 **Redirects (DNATs)** that traffic to one of the **actual pod IPs** backing the service — selecting among them for basic load balancing.

> 🔗 Conceptually, this is the **same DNAT mechanism** used earlier for manual port-forwarding (`iptables -t nat ... -j DNAT`) — Kubernetes automates and scales that exact pattern across the whole cluster.

---

### 🌐 5.4 Service Discovery via DNS

Rather than hardcoding a Service's ClusterIP, pods typically reach Services by **name**, thanks to Kubernetes' internal DNS (usually **CoreDNS**):

- Every Service automatically gets a DNS entry, e.g.:
  ```
  my-service.my-namespace.svc.cluster.local
  ```
- A pod can simply resolve `my-service` (within the same namespace) or the fully qualified name (across namespaces), and DNS returns the Service's stable ClusterIP.

➡️ This means application code never needs to know real pod IPs **or** even the Service's IP — just its **name**.

---

## 🔄 6. Putting It All Together — Full Request Flow

```
1. Client Pod wants to talk to "backend-service"
2. DNS lookup (CoreDNS) → resolves to Service's ClusterIP
3. Packet sent to ClusterIP
4. kube-proxy's iptables/IPVS rules intercept the packet on the node
5. Packet is DNATed to one of the healthy backend Pod IPs (load-balanced)
6. Pod-to-Pod networking rules (same-node bridge OR cross-node routing) deliver
   the packet to the actual destination Pod
7. Response follows the reverse path back to the Client Pod
```

---

## 📚 7. Summary Cheat Sheet

| Concept | 🔑 Key Point |
|---|---|
| Core Model Rule 1 | Every pod gets its own unique IP |
| Core Model Rule 2 | All pods can reach all pods, no NAT |
| Core Model Rule 3 | Nodes can reach all pods, no NAT |
| Same-node Pod-to-Pod | Via shared node bridge (veth pairs) |
| Cross-node Pod-to-Pod | Routed/tunneled across nodes by the CNI plugin |
| Why Services exist | Pod IPs are ephemeral; Services give a stable VIP + load balancing |
| Endpoints / EndpointSlice | Tracks the live set of pod IPs behind a Service |
| kube-proxy | Programs iptables/IPVS to DNAT ClusterIP traffic to real pod IPs |
| CoreDNS | Provides name-based discovery for Services (and pods) |

> 🎓 **Key takeaway:** Kubernetes networking guarantees a flat, NAT-free network where every pod can reach every other pod directly by IP — but because pod IPs are ephemeral, **Services** sit on top to provide a stable virtual IP, automatic load balancing, and DNS-based discovery, all implemented under the hood using the same iptables/DNAT and bridging concepts from core Linux networking.
