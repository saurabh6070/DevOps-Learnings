# 📘 Introduction to Virtualization and Containerization

## 1. **Virtualization Overview**

Virtualization allows multiple virtual machines (VMs) or containers to run on a single physical server. When designing such systems, three key factors must be considered:

- **Cost Efficiency**
- **Security**
- **Resource Allocation**

### 🔐 Security Considerations
- Virtual machines are isolated from the host system by a **hypervisor**, ensuring strong security boundaries.
- VMs are considered as secure as dedicated physical servers due to this isolation.

### ⚙️ Resource Allocation
- The hypervisor is responsible for allocating **dedicated hardware resources** (CPU, memory, etc.) to each VM.

### 🧱 Types of Virtualization
- **Type 1 (Bare Metal)**:  
  `Hardware → Hypervisor → Virtual Machines`
- **Type 2 (Hosted)**:  
  `Hardware → Host OS → Hypervisor → Virtual Machines`  
  *(Commonly used by cloud providers)*

### ⚠️ Challenges of Virtual Machines
- **Increased OS Overhead**: Each VM runs its own OS, increasing licensing, patching, and maintenance costs.
- **Resource Inefficiency**: VMs may consume more resources than necessary.
- **Slow Boot Times**: Full OS boot is required.
- **Bloat**: VMs often include unnecessary binaries not required by the application.

### ✅ Benefits of Virtualization
- **Scalability**: Easily scale up or down based on demand.
- **Security**: Strong isolation between environments.

### 🧠 Role of the Operating System
The OS acts as a bridge between applications and hardware, enabling task execution and resource management.

---


# 2.📦 Introduction to Containerization

## 🧾 What is a Container?
- A container is an operating system-level process that behaves similarly to a virtual machine but is more lightweight.
- Unlike a full OS, a container includes only the application code and its dependencies—not the entire operating system.
- It is a standard unit of software that packages code and all its dependencies to ensure consistent execution across environments.

## 🏗️ Container Architecture
Hardware → OS → RUNC → <br>
-    ├── Container 1: [App-1 Code + Dependencies] <br>
-    └── Container 2: [App-2 Code + Dependencies] <br>

## 🧰 Types of Containers
LXC – Linux Containers
CRI-O – Lightweight container runtime for Kubernetes
Podman – Daemonless container engine
Rkt (Rocket) – App container runtime
Apache Mesos – Also supports Windows containers
Docker – Most widely used container platform

## 🐳 Installing Docker
Docker is the most commonly used container runtime. It typically uses runc as the default container runtime under the hood.

## ⚙️ Linux Process Execution Flow
Process1 ──generates──> System Call 1 ──calls──> Kernel ──allocates──> Hardware  
Process2 ──generates──> System Call 2 ──calls──> Kernel ──allocates──> Hardware

### 🧪 Example:
If Process1 requires Python 2 and Process2 requires Python 3, running both on the same system can cause conflicts.
This is where Namespaces come into play.

## 🧩 Linux Kernel Features for Containers

### 🧱 Linux Namespace

A Namespace is a Linux kernel feature that isolates resources so that one set of processes sees one set of resources, and another set sees a different set.
Enables process-level isolation.

### 📊 Linux cgroups (Control Groups)
A cgroup limits, accounts for, and isolates the resource usage (CPU, memory, disk I/O, etc.) of a group of processes.
Ensures resource control and efficiency.

### 🛠️ Container Lifecycle & Docker Workflow
Developer ──writes──> Code  
        └──adds to──> Dockerfile  
                └──builds──> Docker Image  
                        └──runs──> Container
The Dockerfile defines all the dependencies and instructions needed to build the container image.

## 🧱 Docker Architecture
Docker CLI
Interface where users run Docker commands.

Docker Daemon
Converts CLI commands into HTTPS API calls and manages containers.

Docker Hub
A cloud-based registry for sharing and storing Docker images.
