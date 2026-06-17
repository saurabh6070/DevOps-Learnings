# Manual Setting Up K8s Cluster

---

## 1. 📘 Kubernetes Cluster Setup on AWS (Ubuntu Master Node)

---

### 1.1. Prerequisites
- Ubuntu 24.04 LTS EC2 instance (Master node).
- Security groups allowing required ports (6443, 10250, 10255, 30000–32767).
- IAM role or key pair for access.

---

### 1.2. Kernel Modules & Networking
```bash
sudo modprobe overlay
sudo modprobe br_netfilter

cat <<EOF | sudo tee /etc/modules-load.d/containerd.conf
overlay
br_netfilter
EOF

cat <<EOF | sudo tee /etc/sysctl.d/kubernetes.conf
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
net.ipv4.ip_forward = 1
EOF

sudo sysctl --system
```

---

### 1.3. Install Container Runtime (containerd)
```bash
sudo apt install -y curl gnupg2 software-properties-common apt-transport-https ca-certificates
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmour -o /etc/apt/trusted.gpg.d/docker.gpg
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt update
sudo apt install -y containerd.io

containerd config default | sudo tee /etc/containerd/config.toml >/dev/null 2>&1
sudo sed -i 's/SystemdCgroup \= false/SystemdCgroup \= true/g' /etc/containerd/config.toml
sudo systemctl restart containerd
sudo systemctl enable containerd
```

---

### 1.4. Install Kubernetes Components

```bash
echo "deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.30/deb/ /" | sudo tee /etc/apt/sources.list.d/kubernetes.list
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.30/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
sudo apt update
sudo apt install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl
```

---

### 1.5. Initialize Master Node
```bash
sudo kubeadm init --apiserver-advertise-address=<MASTER_PRIVATE_IP> --pod-network-cidr=10.244.0.0/16 --v=5 --ignore-preflight-errors=all

mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

---

### 1.6. Verify Cluster Status
```bash
kubectl get pods -n kube-system
kubectl get nodes
curl http://127.0.0.1:10248/healthz
```

---

### 1.7. Install Calico CNI
```bash
kubectl apply -f https://raw.githubusercontent.com/projectcalico/calico/v3.25.0/manifests/calico.yaml
```

Edit configmap if required:

```yaml
apiVersion: v1
data:
  CALICO_IPV4POOL_CIDR: "10.244.0.0/16"
```

---

### 1.8. Post-Setup Checks

```bash
kubectl get pods -n kube-system
kubectl get nodes
netstat -anp | grep kubelet | grep -iv stream
```



---

---

## 2. 📘 Kubernetes Worker Node Setup (AWS Ubuntu)

### 2.1. Prerequisites
Ubuntu 24.04 LTS EC2 instances (Workers).

Same VPC and subnet as Master.

Security groups allowing required ports (10250, 30000–32767).

### 2.2. Kernel Modules & Networking
bash
sudo modprobe overlay
sudo modprobe br_netfilter

cat <<EOF | sudo tee /etc/modules-load.d/containerd.conf
overlay
br_netfilter
EOF

cat <<EOF | sudo tee /etc/sysctl.d/kubernetes.conf
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
net.ipv4.ip_forward = 1
EOF

sudo sysctl --system

### 2.3. Install Container Runtime
bash
sudo apt install -y curl gnupg2 software-properties-common apt-transport-https ca-certificates
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmour -o /etc/apt/trusted.gpg.d/docker.gpg
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt update
sudo apt install -y containerd.io

containerd config default | sudo tee /etc/containerd/config.toml >/dev/null 2>&1
sudo sed -i 's/SystemdCgroup \= false/SystemdCgroup \= true/g' /etc/containerd/config.toml
sudo systemctl restart containerd
sudo systemctl enable containerd

### 2.4. Install Kubernetes Components
bash
echo "deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.30/deb/ /" | sudo tee /etc/apt/sources.list.d/kubernetes.list
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.30/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
sudo apt update
sudo apt install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl

### 2.5. Join Worker Node to Cluster
On the Master node, after kubeadm init, you’ll see a kubeadm join command. Run it on each Worker:

bash
sudo kubeadm join <MASTER_PRIVATE_IP>:6443 --token <TOKEN> \
    --discovery-token-ca-cert-hash sha256:<HASH>
Verify:

bash
kubectl get nodes

## 3. 📘 Pod Interfaces with Calico CNI

Calico is a Container Network Interface (CNI) plugin that provides networking and network policy enforcement.

### 🔹 How Pod Interfaces Are Created

#### Pod scheduled → kubelet requests CNI plugin to set up networking.

#### Calico CNI plugin runs:
Creates a veth pair (virtual Ethernet).
One end inside the Pod’s network namespace (eth0).
Other end in the host namespace, connected to Calico-managed bridge.

#### IP assignment:
Calico IPAM allocates Pod IP from the CIDR (10.244.0.0/16).
IP is written to Pod’s network namespace.

#### Routing:
Calico programs routes using BGP or VXLAN.
Ensures Pod-to-Pod communication across nodes.

#### Policies:
NetworkPolicies applied via Calico enforce ingress/egress rules.

### 🔹 Verification

```bash
kubectl get pods -o wide
ip a   # check Pod IPs assigned
```

Inside Pod:

```bash
kubectl exec -it <pod> -- ip addr show eth0
```

You’ll see the Pod interface (eth0) with an IP from the Calico pool.
