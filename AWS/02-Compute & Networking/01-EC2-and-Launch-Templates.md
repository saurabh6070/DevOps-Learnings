# 🖥️ EC2 and Launch Templates

## 💡 What is Amazon EC2?
Amazon Elastic Compute Cloud (EC2) is AWS’s core compute service that provides resizable virtual servers in the cloud. It allows users to launch virtual machines on demand without buying physical hardware.

EC2 is commonly used for:
- hosting web applications
- running enterprise workloads
- deploying application servers
- supporting development and testing environments
- acting as a backend for databases or middleware services

Unlike traditional servers, EC2 gives flexibility to choose instance size, operating system, storage, networking, and scaling behavior based on workload requirements.

---

## 🧱 EC2 Core Concepts

### 1. Instance Types
EC2 instance types are categorized by workload characteristics such as:
- General purpose: balanced CPU and memory
- Compute optimized: high CPU performance
- Memory optimized: large memory workloads
- Storage optimized: high disk throughput
- Accelerated computing: GPU-based workloads

Choosing the correct instance family is important for cost and performance.

### 2. AMI (Amazon Machine Image)
An AMI is a template used to create an EC2 instance. It contains:
- OS image
- application preconfiguration
- software packages
- launch permissions

Common AMI choices include Amazon Linux, Ubuntu, Windows Server, and custom images.

### 3. Security Groups
Security Groups act as virtual firewalls for EC2 instances.
- They control inbound and outbound traffic
- They are stateful
- They can allow or deny traffic based on port, protocol, and source IP

### 4. Key Pairs
Key pairs are used for secure SSH access to Linux instances and RDP access to Windows instances.

### 5. Elastic IPs
An Elastic IP is a static public IPv4 address assigned to an EC2 instance. It is useful when you need a predictable public IP.

---

## 🗂️ Storage Options for EC2
EC2 instances can use different kinds of storage depending on the workload.

### 💾 Instance Store
- Temporary storage attached to the host machine
- Best suited for cache or temporary data
- Data is lost if the instance stops or terminates

### 🧊 Amazon EBS
Amazon Elastic Block Store (EBS) provides persistent block storage for EC2.
- Used for operating systems, databases, and application data
- Survives instance stop/start
- Supports snapshots for backup and recovery

### 🔄 EBS vs Instance Store
```text
EC2 Instance
├── Root Volume (EBS or Instance Store)
├── Additional EBS Volumes
└── Temporary Instance Store
```

This diagram shows that EC2 can have persistent EBS storage and temporary instance-store storage depending on configuration.

---

## 🚀 Launch Templates
Launch Templates are used to standardize EC2 instance launches. They define settings such as:
- AMI ID
- instance type
- subnet
- security groups
- key pair
- user data scripts
- IAM instance profile

They help teams create consistent and repeatable infrastructure deployments.

### Why Launch Templates are Useful
- reduce manual configuration errors
- simplify Auto Scaling configurations
- standardize deployment practices
- make infrastructure automation easier

---

## 📈 EC2 and High Availability
EC2 can be part of highly available systems when used with:
- multiple instances across different Availability Zones
- Elastic Load Balancing
- Auto Scaling Groups
- EBS snapshots and backups

This improves fault tolerance and protects applications from single-instance failure.

---

## 🛡️ Best Practices for EC2
- Use IAM roles instead of embedding long-term credentials in instances
- Prefer EBS for persistent data storage
- Use Security Groups to restrict access to only required ports
- Place instances in private subnets when they should not be directly exposed to the internet
- Use Auto Scaling for workload fluctuations
- Monitor CPU, memory, disk, and network metrics regularly

---

## 🔍 EC2 vs Other AWS Services
- EC2 is compute
- S3 is object storage
- EBS is block storage
- Lambda is serverless compute
- ECS/EKS are container orchestration services

This distinction is very important in AWS exams and interviews.

---

## 📝 Exam Notes
- EC2 provides virtual servers in the cloud.
- Instance type selection depends on CPU, memory, storage, and networking needs.
- AMIs define the starting image of the instance.
- Security Groups are stateful firewalls.
- Launch Templates simplify repeated EC2 deployments.
- EBS is persistent storage; instance store is temporary.
