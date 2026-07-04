# 📘 Minikube Setup on AWS Ubuntu VM

## 🔧 1. Introduction
Minikube is a lightweight Kubernetes implementation that runs a single-node cluster on your local machine.  
It’s ideal for **testing and learning Kubernetes** before moving to production-grade clusters like EKS.  

⚠️ Note: Minikube stops whenever the VM is stopped/restarted. You must restart Minikube manually or configure a **startup script**.

---

## 🖥️ 2. Prerequisites
- AWS EC2 Ubuntu VM (t2.medium or larger recommended).
- Security group allowing SSH (port 22).
- At least 2 CPUs and 4GB RAM for smooth operation.

---

## 📦 3. Install Dependencies

```bash
sudo apt update -y
sudo apt install -y curl wget apt-transport-https ca-certificates software-properties-common
sudo apt install -y docker.io
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker $USER && newgrp docker
```

## 🚀 4. Install Minikube

```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

Verify:

```bash
minikube version
```

## 🛠️ 5. Install kubectl

```bash
curl -LO "https://dl.k8s.io/release/$(curl -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/
kubectl version --client --short
```

## ⚡ 6. Start Minikube

```bash
minikube start --driver=docker
```

Check cluster:

```bash
kubectl get nodes
kubectl get pods -n kube-system
```

## 🎛️ 7. Enable Addons
```bash
minikube addons enable dashboard
minikube addons enable ingress
```

Access dashboard:

```bash
minikube dashboard
```

## 🔄 8. Auto-Start Script (Optional)

Create a startup script so Minikube starts automatically after VM reboot:

```bash
sudo tee /etc/systemd/system/minikube.service <<EOF
[Unit]
Description=Minikube Kubernetes Cluster
After=docker.service
Requires=docker.service

[Service]
ExecStart=/usr/local/bin/minikube start --driver=docker
ExecStop=/usr/local/bin/minikube stop
Restart=always
User=ubuntu

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable minikube
sudo systemctl start minikube
```
