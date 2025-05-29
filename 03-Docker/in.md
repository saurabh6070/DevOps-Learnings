📘 Introduction to Virtualization and Containerization
1. Virtualization Overview
Virtualization allows multiple virtual machines (VMs) or containers to run on a single physical server. When designing such systems, three key factors must be considered:

Cost Efficiency
Security
Resource Allocation
🔐 Security Considerations
Virtual machines are isolated from the host system by a hypervisor, ensuring strong security boundaries.
VMs are considered as secure as dedicated physical servers due to this isolation.
⚙️ Resource Allocation
The hypervisor is responsible for allocating dedicated hardware resources (CPU, memory, etc.) to each VM.
🧱 Types of Virtualization
Type 1 (Bare Metal):
Hardware → Hypervisor → Virtual Machines
Type 2 (Hosted):
Hardware → Host OS → Hypervisor → Virtual Machines
(Commonly used by cloud providers)
⚠️ Challenges of Virtual Machines
Increased OS Overhead: Each VM runs its own OS, increasing licensing, patching, and maintenance costs.
Resource Inefficiency: VMs may consume more resources than necessary.
Slow Boot Times: Full OS boot is required.
Bloat: VMs often include unnecessary binaries not required by the application.
✅ Benefits of Virtualization
Scalability: Easily scale up or down based on demand.
Security: Strong isolation between environments.
🧠 Role of the Operating System
The OS acts as a bridge between applications and hardware, enabling task execution and resource management.

2. Containerization Overview
Containerization is a lightweight alternative to virtualization. It allows applications to run in isolated environments using shared OS resources.

📦 What is a Container?
A container is an OS-level process that behaves like a VM but is more efficient.
It includes only the application code and its dependencies, not a full OS.
Containers are portable, lightweight, and fast to start.
🏗️ Container Architecture
Hardware 
  ↓
Operating System (Linux Kernel)
  ↓
Container Runtime (e.g., runc)
  ↓
[Container 1: App-1 + Dependencies]
[Container 2: App-2 + Dependencies]
🧰 Types of Containers
LXC (Linux Containers)
CRI-O
Podman
Rkt (Rocket)
Apache Mesos (supports Windows containers)
Docker (most widely adopted)
🐳 Installing Docker
Docker is a popular container platform that uses runc as its default runtime. It simplifies container creation, management, and deployment.

3. Linux Process Execution Flow
In a Linux system:

Process → System Call → Kernel → Hardware
Example: If Process1 needs Python 2 and Process2 needs Python 3, running both on the same system can cause conflicts.
Containers solve this using Namespaces.
4. Linux Kernel Features for Containers
🧩 Namespaces
Isolate system resources (e.g., process IDs, network, file systems).
Each container sees only its own set of resources.
📊 cgroups (Control Groups)
Limit and monitor resource usage (CPU, memory, disk I/O) for a group of processes.
5. Container Lifecycle with Docker
Developer → Writes Code → Adds to Dockerfile → Builds Docker Image → Runs Container
The Dockerfile defines the environment and dependencies required to run the application.
6. Docker Architecture
Docker CLI: Interface to run Docker commands.
Docker Daemon: Converts CLI commands into HTTPS API calls and manages containers.
Docker Hub: Cloud-based registry for storing and sharing Docker images.
