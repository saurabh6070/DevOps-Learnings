# 📘 Amazon EKS Setup (AWS Managed Kubernetes)

## 1. Introduction
Amazon Elastic Kubernetes Service (EKS) is a **managed Kubernetes service** that simplifies cluster setup and operation.  
 - AWS manages the **control plane** (API server, etcd, scheduler, controllers).  
 - You manage the **worker nodes** (EC2 instances).  
 - No control plane Pods are visible in your cluster — AWS handles them.  

---

## 2. Prerequisites
 - AWS account with IAM permissions.
 - EC2 instance for setup (Ubuntu recommended).
 - IAM Role: `AWS_ADMIN_ROLE`.
 - Installed tools: **AWS CLI**, **eksctl**, **kubectl**.

---

## 3. Install Required Tools

### 🔹 AWS CLI
```bash
aws --version
aws configure
```

### 🔹 eksctl
```bash
curl --silent --location "https://github.com/weaveworks/eksctl/latest/download/eksctl_$(uname -s)_amd.tar.gz" | tar xz -C /tmp
sudo mv /tmp/eksctl /usr/local/bin
chmod +x /usr/bin/eksctl
```

### 🔹 kubectl
```bash
curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.31.2/2024-11-15/bin/linux/amd64/kubectl
chmod +x ./kubectl
kubectl version --short --client
source <(kubectl completion bash)
mkdir -p $HOME/bin && cp ./kubectl $HOME/bin/kubectl && export PATH=$HOME/bin:$PATH
```

---

## 4. Create EKS Cluster

### 🔹 Command

```bash
eksctl create cluster \
  --name my-cluster \
  --region us-west-2 \
  --nodegroup-name my-nodegroup \
  --node-type t2.medium \
  --nodes 3 \
  --nodes-min 1 \
  --nodes-max 4 \
  --with-oidc \
  --managed
```

 - Uses CloudFormation to provision resources.
 - Creates a node group of EC2 instances.
 - Control plane is fully managed by AWS.

### 🔹 Verify Cluster

```bash
kubectl get nodes
```
---

## 5. Advantages of EKS
 - AWS manages control plane (no need to install controllers like EBS, Nginx, etc.).
 - Highly available and secure.
 - Integrates with AWS services (IAM, VPC, CloudWatch, WAF).

---

## 6. Deploy Applications

### 🔹 Create Deployment
```bash
kubectl create deployment nginx \
  --image=nginx \
  --labels="app=nginx,env=prod" \
  --replicas=3
```

### 🔹 Expose Deployment
```bash
kubectl expose deployment nginx \
  --name=nginx-lb \
  --type=LoadBalancer \
  --port=80 \
  --target-port=80 \
  --labels="app=nginx,env=prod"
```

### 🔹 Verify
```bash
kubectl get pods -l app=nginx,env=prod
kubectl get svc nginx-lb
```

---

## 7. LoadBalancer in EKS

 - When a LoadBalancer Service is created, AWS automatically provisions an ELB (Elastic Load Balancer).
 - Security groups must allow the exposed port (e.g., 80).
 - You can attach AWS WAF to secure access.

---

## 8. Ingress in EKS

 - Instead of multiple LoadBalancers for microservices, use Ingress.
 - Ingress Controller manages routing rules.
 - AWS automatically provisions the Ingress Controller in the console when created via kubectl.
