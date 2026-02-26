# 🐳 Docker — Complete Notes (Beginner to Advanced)

> 🚀 A comprehensive guide to Docker — covering virtualization fundamentals, containerization, Docker architecture, images, containers, networking, volumes, Docker Compose, and production best practices.

---

## 📌 Table of Contents

| # | Section |
|---|---------|
| 1 | [🖥️ Introduction to Virtualization](#1-%EF%B8%8F-introduction-to-virtualization) |
| 2 | [📦 Introduction to Containerization](#2--introduction-to-containerization) |
| 3 | [🐳 What is Docker?](#3--what-is-docker) |
| 4 | [⚙️ Docker Architecture](#4-%EF%B8%8F-docker-architecture) |
| 5 | [📥 Installing Docker](#5--installing-docker) |
| 6 | [📄 Dockerfile](#6--dockerfile) |
| 7 | [🖼️ Docker Images](#7-%EF%B8%8F-docker-images) |
| 8 | [📦 Docker Containers](#8--docker-containers) — Lifecycle, OS-process proof, commit, rename, attach, history, cleanup |
| 9 | [🗂️ Docker Volumes](#9-%EF%B8%8F-docker-volumes) — Types, commands, practical workflow, backup/restore |
| 10 | [🌐 Docker Networking](#10--docker-networking) — docker0 bridge, user-defined bridge, DNS |
| 11 | [🗃️ Docker Registry & Docker Hub](#11-%EF%B8%8F-docker-registry--docker-hub) — Push walkthrough, layers, storage paths, daemon logs |
| 12 | [🧩 Docker Compose](#12--docker-compose) |
| 13 | [🔐 Docker Security](#13--docker-security) |
| 14 | [📊 Docker Resource Management](#14--docker-resource-management) |
| 15 | [🔍 Docker Logging & Monitoring](#15--docker-logging--monitoring) |
| 16 | [🏗️ Multi-Stage Builds](#16-%EF%B8%8F-multi-stage-builds) |
| 17 | [🚀 Docker in CI/CD](#17--docker-in-cicd) |
| 18 | [🌊 Docker Swarm](#18--docker-swarm) |
| 19 | [✅ Docker Best Practices](#19--docker-best-practices) |
| 20 | [⚡ Quick Reference Cheat Sheet](#20--quick-reference-cheat-sheet) |

---

## 1. 🖥️ Introduction to Virtualization

**Virtualization** is the process of creating virtual instances of computing resources — servers, operating systems, storage, or networks. It is the foundation of modern cloud computing and IT infrastructure.

When implementing virtualization, three key factors must be considered:

| Factor | Description |
|--------|-------------|
| 💰 **Cost Efficiency** | Share physical hardware across multiple virtual machines to reduce hardware costs |
| 🔐 **Security** | Isolated environments limit the blast radius of security breaches |
| ⚙️ **Resource Allocation** | Hypervisors distribute CPU, RAM, and storage efficiently among VMs |

### 1.1 🔐 Security in Virtualization

Virtual machines operate in **isolated environments** and do not have direct access to the host system. This isolation is enforced by the **hypervisor**, which acts as a security boundary between the host and the VMs — giving VMs a security level comparable to dedicated physical servers.

### 1.2 ⚙️ Resource Allocation

Hypervisors manage and allocate physical hardware resources — CPU, memory, disk, and network — to each virtual machine. This ensures:
- Efficient hardware utilization
- Performance isolation between VMs
- No single VM can starve others of resources

### 1.3 🧱 Types of Hypervisor-Based Virtualization

#### Type 1 — Bare-Metal Hypervisor

```
Physical Hardware
      ↓
  Hypervisor          ← Runs DIRECTLY on hardware
      ↓
Virtual Machines
```

- Runs directly on physical hardware — no underlying OS
- High performance and security
- Used in enterprise environments
- **Examples:** VMware ESXi, Microsoft Hyper-V, Xen

#### Type 2 — Hosted Hypervisor

```
Physical Hardware
      ↓
Host Operating System
      ↓
  Hypervisor          ← Runs ON TOP of host OS
      ↓
Virtual Machines
```

- Runs on top of an existing operating system
- Easier to set up; used for development and testing
- Preferred by many cloud providers for flexibility
- **Examples:** VirtualBox, VMware Workstation, KVM

### 1.4 ⚠️ Challenges in Virtual Machine Deployment

| Challenge | Description |
|-----------|-------------|
| 🐘 **OS Overhead** | Each VM needs its own OS → higher licensing, patching, and maintenance cost |
| ⚙️ **Resource Management** | Efficient allocation is critical to avoid bottlenecks |
| 🐢 **Slow Boot Times** | VMs take minutes to boot compared to seconds for containers |
| 🗑️ **Bloated OS** | Guest OS includes many binaries and services the application doesn't need |
| 💰 **Cost** | More OS instances = more cost at scale |

### 1.5 ✅ Benefits of Virtualization

- **Scalability** — Resources scale up or down based on demand
- **Security** — Strong isolation between virtual environments
- **Hardware utilization** — Multiple workloads on a single physical machine
- **Disaster recovery** — VMs can be snapshotted, cloned, and migrated

### 1.6 🧠 Role of the Operating System

```
Applications
     ↓
Operating System     ← Bridge between apps and hardware
     ↓
Hardware
```

The OS manages hardware resources and provides the necessary environment for applications to run. This is the layer that containers share with the host — making them far more lightweight than VMs.

---

## 2. 📦 Introduction to Containerization

### 2.1 🧾 What is a Container?

A **container** is an isolated operating system process that:

- Behaves similarly to a VM but is **much more lightweight**
- Includes only the **application code + its dependencies** — not a full OS
- Shares the host OS kernel (unlike VMs which have their own kernel)
- Starts in **seconds** instead of minutes

```
Virtual Machine:                Container:
┌─────────────┐                 ┌─────────────┐
│  App + Deps │                 │  App + Deps │
├─────────────┤                 ├─────────────┤
│  Guest OS   │  ← Heavy        │  (no OS)    │  ← Lightweight
├─────────────┤                 └─────────────┘
│  Hypervisor │                        ↓
├─────────────┤                  Shared Host OS
│  Hardware   │                        ↓
└─────────────┘                   Hardware
```

### 2.2 🆚 VMs vs Containers — Comparison

| Feature | Virtual Machines | Containers |
|---------|:---------------:|:---------:|
| **OS** | Full OS per VM | Shared host OS kernel |
| **Size** | GBs | MBs |
| **Boot Time** | Minutes | Seconds |
| **Isolation** | Strong (hypervisor) | Process-level (namespaces) |
| **Performance** | Lower (OS overhead) | Near-native |
| **Portability** | Moderate | ✅ High |
| **Use case** | Full OS isolation | App packaging & delivery |

### 2.3 🏗️ Container Architecture

```
Physical Hardware
       ↓
Host Operating System (Linux Kernel)
       ↓
Container Runtime (e.g., runc, containerd)
       ↓
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│  Container 1     │  │  Container 2     │  │  Container 3     │
│  App-1 + Deps    │  │  App-2 + Deps    │  │  App-3 + Deps    │
└──────────────────┘  └──────────────────┘  └──────────────────┘
```

### 2.4 🧰 Types of Container Runtimes

| Runtime | Description |
|---------|-------------|
| 🐳 **Docker** | Most widely used; developer-friendly; uses `runc` under the hood |
| **containerd** | Industry-standard runtime used by Docker and Kubernetes |
| **runc** | Low-level OCI-compliant runtime; used by Docker/containerd |
| **LXC** | Linux Containers — system containers (closer to VMs) |
| **Podman** | Daemonless, rootless alternative to Docker |
| **CRI-O** | Lightweight runtime designed specifically for Kubernetes |
| **Rkt (Rocket)** | CoreOS's container runtime (now deprecated) |
| **Apache Mesos** | Supports both Linux and Windows containers at scale |

### 2.5 🧩 Linux Kernel Features Behind Containers

Containers work because of two core Linux kernel features:

#### 🧱 Namespaces — Isolation

Namespaces give each container its **own isolated view** of system resources:

| Namespace | What It Isolates |
|-----------|-----------------|
| `pid` | Process IDs — container sees its own process tree |
| `net` | Network interfaces, IP addresses, routing tables |
| `mnt` | File system mount points |
| `uts` | Hostname and domain name |
| `ipc` | Inter-process communication |
| `user` | User and group IDs |

#### 📊 cgroups (Control Groups) — Resource Limits

cgroups **limit and monitor** resource usage for a group of processes:

```bash
# Example: Limit a container to 512MB RAM and 50% CPU:
docker run -m 512m --cpus="0.5" nginx
```

| Resource | Controlled By cgroups |
|----------|----------------------|
| CPU | Limit CPU time per container |
| Memory | Set max RAM usage |
| Disk I/O | Throttle read/write speeds |
| Network | Bandwidth control |

#### 🤔 Why This Matters — Real Example

```
Problem: Process 1 needs Python 2, Process 2 needs Python 3
         → Running both on the same OS causes conflicts

Solution: Containers isolate each process with its own namespace
         → Process 1 sees Python 2 in its container
         → Process 2 sees Python 3 in its container
         → Both run simultaneously on the same host — no conflicts!
```

---

## 3. 🐳 What is Docker?

**Docker** is an open-source platform that makes it easy to **build, ship, and run** applications in containers. It was released in **2013** by Solomon Hykes / dotCloud and became the de facto standard for containerization.

### Docker Workflow

```
Developer
    ↓
Writes Application Code
    ↓
Creates a Dockerfile (environment definition)
    ↓
Builds a Docker Image (immutable snapshot)
    ↓
Runs a Docker Container (running instance of image)
    ↓
Pushes Image to Docker Hub / Registry (share & deploy)
```

### Why Docker?

| Without Docker | With Docker |
|----------------|------------|
| "Works on my machine" | ✅ Runs identically everywhere |
| Manual dependency installation | ✅ Dependencies bundled in image |
| Slow environment setup | ✅ `docker run` = instant environment |
| OS conflicts between apps | ✅ Isolated containers per app |
| Hard to scale | ✅ Spin up multiple containers instantly |

---

## 4. ⚙️ Docker Architecture

Docker uses a **client-server architecture** with three main components:

```
┌─────────────────────────────────────────────────────────────────┐
│                        Docker Host                              │
│                                                                 │
│  ┌──────────────┐    REST API    ┌────────────────────────────┐ │
│  │  Docker CLI  │ ◄────────────► │      Docker Daemon         │ │
│  │  (Client)    │                │      (dockerd)             │ │
│  └──────────────┘                │                            │ │
│                                  │  ┌──────┐  ┌──────┐       │ │
│                                  │  │Image │  │Image │       │ │
│                                  │  └──────┘  └──────┘       │ │
│                                  │  ┌──────────────────────┐  │ │
│                                  │  │ Container 1          │  │ │
│                                  │  │ Container 2          │  │ │
│                                  │  └──────────────────────┘  │ │
│                                  └────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                              ↕  HTTPS
                                    ┌─────────────────────┐
                                    │    Docker Hub /     │
                                    │    Registry         │
                                    └─────────────────────┘
```

### 4.1 Core Components

| Component | Description |
|-----------|-------------|
| 🖥️ **Docker CLI** | Command-line interface — sends commands to Docker Daemon via REST API |
| ⚙️ **Docker Daemon (`dockerd`)** | Background service that receives CLI commands, manages images, containers, networks, and volumes |
| 🖼️ **Docker Images** | Read-only, immutable blueprint of a container (built from Dockerfile) |
| 📦 **Docker Containers** | Running instance of a Docker image |
| 🌐 **Docker Registry** | Storage for Docker images (e.g., Docker Hub, ECR, GCR) |
| 🔧 **containerd** | Container runtime used by Docker daemon to actually run containers |
| 🔩 **runc** | Low-level OCI runtime that creates and runs containers from OCI bundles |

### 4.2 How a `docker run` Works Internally

```
1. User runs:     docker run nginx
2. Docker CLI     → sends request to Docker Daemon (via UNIX socket)
3. Docker Daemon  → checks if 'nginx' image exists locally
4. If not found   → pulls from Docker Hub (registry)
5. containerd     → unpacks the image layers
6. runc           → creates the container using namespaces + cgroups
7. Container      → starts running!
```

---

## 5. 📥 Installing Docker

### 5.1 Ubuntu / Debian

```bash
# Update package index:
sudo apt update

# Install prerequisites:
sudo apt install -y apt-transport-https ca-certificates curl gnupg lsb-release

# Add Docker's official GPG key:
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker repository:
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] \
  https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine:
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Verify installation:
docker --version
docker run hello-world
```

### 5.2 CentOS / RHEL

```bash
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install -y docker-ce docker-ce-cli containerd.io
sudo systemctl start docker
sudo systemctl enable docker
```

### 5.3 Post-Installation (Run Docker Without sudo)

```bash
# Add your user to the docker group:
sudo usermod -aG docker $USER

# Reload group (or log out and back in):
newgrp docker

# Verify:
docker ps
```

### 5.4 Key Docker Paths

| Path | Purpose |
|------|---------|
| `/var/lib/docker/` | Docker data directory (images, containers, volumes) |
| `/etc/docker/daemon.json` | Docker daemon configuration |
| `/var/run/docker.sock` | Docker UNIX socket (CLI ↔ Daemon communication) |

---

## 6. 📄 Dockerfile

A **Dockerfile** is a plain-text file with instructions to build a Docker image. Each instruction creates a new **layer** in the image.

### 6.1 Basic Dockerfile Structure

```dockerfile
# Base image:
FROM ubuntu:22.04

# Maintainer info (optional):
LABEL maintainer="devops@company.com"

# Set environment variables:
ENV APP_HOME=/app \
    APP_PORT=8080 \
    PYTHONDONTWRITEBYTECODE=1

# Set working directory:
WORKDIR /app

# Copy files into the image:
COPY requirements.txt .
COPY . .

# Run commands during build:
RUN apt-get update && apt-get install -y python3 pip \
    && pip install -r requirements.txt \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Expose a port (documentation only — doesn't publish):
EXPOSE 8080

# Define a volume mount point:
VOLUME ["/app/data"]

# Switch to non-root user (security best practice):
RUN useradd -m appuser
USER appuser

# Default command when container starts:
CMD ["python3", "app.py"]
```

### 6.2 Dockerfile Instructions Reference

| Instruction | Purpose | Example |
|-------------|---------|---------|
| `FROM` | Base image (must be first) | `FROM python:3.11-slim` |
| `RUN` | Execute command during build | `RUN apt-get install -y curl` |
| `CMD` | Default command at container start (overridable) | `CMD ["nginx", "-g", "daemon off;"]` |
| `ENTRYPOINT` | Fixed command (CMD appended as args) | `ENTRYPOINT ["python3"]` |
| `COPY` | Copy files from host to image | `COPY app.py /app/` |
| `ADD` | Like COPY + supports URLs + auto-extracts tar | `ADD app.tar.gz /app/` |
| `WORKDIR` | Set working directory | `WORKDIR /app` |
| `ENV` | Set environment variables | `ENV PORT=8080` |
| `EXPOSE` | Document which port the app uses | `EXPOSE 8080` |
| `VOLUME` | Create a mount point for persistent data | `VOLUME ["/data"]` |
| `USER` | Set user for subsequent instructions | `USER appuser` |
| `ARG` | Build-time variable (not available at runtime) | `ARG VERSION=1.0` |
| `LABEL` | Add metadata | `LABEL version="1.0"` |
| `HEALTHCHECK` | Check container health | `HEALTHCHECK CMD curl -f http://localhost/` |
| `ONBUILD` | Trigger instruction in child image | `ONBUILD COPY . /app` |

### 6.3 CMD vs ENTRYPOINT

| | `CMD` | `ENTRYPOINT` |
|--|-------|-------------|
| **Purpose** | Default command (can be overridden) | Fixed executable (always runs) |
| **Override** | `docker run image <new-cmd>` replaces CMD | `docker run image <args>` appends to ENTRYPOINT |
| **Use together** | `ENTRYPOINT` = executable; `CMD` = default args | Flexible and powerful |

```dockerfile
# CMD only:
CMD ["python3", "app.py"]               # Can be overridden: docker run img bash

# ENTRYPOINT + CMD:
ENTRYPOINT ["python3"]
CMD ["app.py"]                          # docker run img → runs python3 app.py
                                        # docker run img test.py → runs python3 test.py
```

### 6.4 Docker Image Layers

Every `RUN`, `COPY`, `ADD` instruction creates a new **read-only layer**:

```
Layer 5: COPY app.py /app/           ← Top layer (latest change)
Layer 4: RUN pip install flask
Layer 3: COPY requirements.txt .
Layer 2: RUN apt-get install python3
Layer 1: FROM ubuntu:22.04           ← Base layer
```

> 💡 **Layer caching:** Docker caches layers. If a layer hasn't changed, it's reused → faster builds.
> Always copy `requirements.txt` BEFORE copying the rest of your code so the dependency layer is cached.

### 6.5 .dockerignore File

Like `.gitignore` — prevents unnecessary files from being sent to the Docker build context:

```dockerignore
.git
.gitignore
*.md
*.log
node_modules/
__pycache__/
.env
tests/
docs/
```

---

## 7. 🖼️ Docker Images

A Docker **image** is a **read-only, immutable blueprint** used to create containers. It contains:
- Application code
- Runtime (Python, Node.js, Java, etc.)
- System libraries and dependencies
- Configuration files

### 7.1 Image Commands

```bash
# Pull an image from Docker Hub:
docker pull nginx
docker pull python:3.11-slim
docker pull ubuntu:22.04

# List local images:
docker images
docker image ls

# Build an image from Dockerfile:
docker build -t myapp:1.0 .
docker build -t myapp:latest -f Dockerfile.prod .

# Tag an image:
docker tag myapp:1.0 myrepo/myapp:1.0

# Push an image to registry:
docker push myrepo/myapp:1.0

# Remove an image:
docker rmi nginx
docker image rm myapp:1.0

# Remove all unused images:
docker image prune
docker image prune -a           # Remove ALL unused images

# Inspect image details:
docker inspect nginx
docker image inspect python:3.11

# Show image layers:
docker history nginx

# Save image to tar file:
docker save -o myapp.tar myapp:1.0

# Load image from tar file:
docker load -i myapp.tar
```

### 7.2 Image Naming Convention

```
[registry/][username/]image-name[:tag]

Examples:
nginx                          ← Official image, latest tag
nginx:1.25                     ← Specific version
python:3.11-slim               ← Slim variant
ubuntu:22.04
myuser/myapp:v1.0              ← User image on Docker Hub
gcr.io/myproject/myapp:prod    ← Google Container Registry
123456789.dkr.ecr.us-east-1.amazonaws.com/myapp:latest  ← AWS ECR
```

### 7.3 Official Image Variants

| Variant | Description | Size |
|---------|-------------|------|
| `ubuntu` / `debian` | Full OS base | ~70–100 MB |
| `slim` | Minimal packages removed | ~50–70 MB |
| `alpine` | Ultra-minimal Linux (musl libc) | ~5 MB |
| `scratch` | Empty base — for static binaries | 0 MB |
| `distroless` | No shell, no package manager — just runtime | ~20 MB |

> ✅ **Use `alpine` or `slim` variants** in production to minimize image size and attack surface.

---

## 8. 📦 Docker Containers

A **container** is a **running instance of a Docker image**. You can have many containers from the same image.

### 8.1 Container Lifecycle

```
Created → Running → Paused → Running → Stopped → Removed
                     ↑                   ↑
              docker pause          docker stop
```

### 8.2 Container Commands

```bash
# Run a container:
docker run nginx                              # Runs in foreground
docker run -d nginx                           # Detached (background)
docker run -d -p 8080:80 nginx               # Map host:container port
docker run -d --name webserver nginx         # Named container
docker run -it ubuntu bash                   # Interactive terminal
docker run --rm ubuntu echo "hello"          # Auto-remove after exit

# Run with environment variables:
docker run -d -e DB_HOST=localhost -e DB_PORT=5432 myapp

# Run with resource limits:
docker run -d --memory="512m" --cpus="0.5" nginx

# List containers:
docker ps                    # Running containers
docker ps -a                 # All containers (including stopped)

# Stop / Start / Restart:
docker stop webserver
docker start webserver
docker restart webserver

# Pause / Unpause:
docker pause webserver
docker unpause webserver

# Remove container:
docker rm webserver           # Must be stopped first
docker rm -f webserver        # Force remove (even if running)

# Remove all stopped containers:
docker container prune

# Execute command in running container:
docker exec -it webserver bash         # Open shell
docker exec webserver cat /etc/nginx/nginx.conf

# View container logs:
docker logs webserver
docker logs -f webserver               # Follow (tail) logs
docker logs --tail 100 webserver       # Last 100 lines

# View container resource usage:
docker stats
docker stats webserver

# Inspect container:
docker inspect webserver

# Copy files between host and container:
docker cp webserver:/etc/nginx/nginx.conf ./nginx.conf   # From container
docker cp ./index.html webserver:/var/www/html/          # To container

# View running processes inside container:
docker top webserver

# View port mappings:
docker port webserver
```

### 8.3 Port Mapping

```bash
# -p <host_port>:<container_port>
docker run -d -p 8080:80 nginx     # Access nginx via localhost:8080

# Map all ports automatically:
docker run -d -P nginx             # Docker assigns random host ports

# Map to specific host IP:
docker run -d -p 127.0.0.1:8080:80 nginx   # Only accessible from localhost
```

### 8.4 Container States Explained

| State | Description |
|-------|-------------|
| `created` | Container created but not started |
| `running` | Container is actively running |
| `paused` | Container processes are paused (frozen in memory) |
| `stopped` | Container has exited (filesystem preserved) |
| `dead` | Container failed to stop properly |
| `restarting` | Container is being restarted |

### 8.5 🧠 Containers ARE OS-Level Processes — Proof

This is a fundamental concept: **a Docker container is simply an isolated Linux process running on the host**.

```bash
# Step 1: Run an nginx container in the background
docker run -d nginx

# Step 2: Check running containers
docker ps
# Output: container ID, image=nginx, STATUS=Up ...

# Step 3: Check the same process from Linux's perspective on the HOST
ps -aux
ps -aux | grep -i nginx
# Output: shows nginx master and worker processes running on the host OS!

# Step 4: Kill the nginx process directly using its Linux PID (requires root)
sudo su -
ps -aux | grep nginx
kill -9 <pid>

# Step 5: Check Docker again
docker ps
# ❌ Container is GONE — because the underlying OS process was killed!
```

> ✅ **This proves that containers are OS-level processes. They behave like lightweight standalone environments thanks to Linux Namespaces (isolation) and cgroups (resource limits) — but to the kernel, they are just processes.**

### 8.6 🔄 Complete Container Lifecycle — Practical Walkthrough

```bash
# Best practice: run as root for Docker operations
sudo su -

# 1. Start a new nginx container (detached/background):
docker run -d nginx

# 2. List running containers (Docker processes):
docker ps

# 3. Force-stop a container immediately:
docker kill <CONTAINER_ID>

# 4. Container is stopped but NOT removed — still in docker ps -a:
docker ps -a

# Show last N containers (e.g., last 5):
docker ps -n 5

# 5. Restart a stopped container:
docker start <CONTAINER_ID>

# 6. Confirm it's running again:
docker ps

# 7. Enter the container shell interactively:
docker exec -it <CONTAINER_ID> bash

# Inside the container — install tools:
apt update -y && apt install -y vim python3

# Write and run a Python script inside the container:
vim hello.py        # Add: print("Hello World")
python3 hello.py    # Output: Hello World

# Detach WITHOUT stopping the container:  Ctrl + P + Q
# Exit and stop container:                exit  or  Ctrl + D
```

### 8.6a 🗑️ Stop and Delete Commands — Full Reference

```bash
docker ps                         # Show running containers (processes)
docker ps -a                      # Show ALL containers including stopped
docker ps -n 5                    # Show last 5 containers

docker stop <CONTAINER_NAME>      # Gracefully stop a container
docker rm   <CONTAINER_NAME>      # Delete stopped container (removes context)
docker rm -f <CONTAINER_NAME>     # Force: STOP + DELETE in one command (running container)

docker images                     # List all local Docker images
docker rmi <IMAGE_ID>             # Remove an image from local storage
```

> 💡 **`docker rm -f`** is the same as `docker stop` followed by `docker rm` — it stops and deletes a running container in a single command.

> 🔑 **Important:** Any command starting with `docker` runs **on the Host only** (outside the container). Commands inside a container are run after `docker exec -it <id> bash` or `docker attach`.

### 8.6b 🔄 Re-Run a Previously Removed Container's Image

If a container was removed with `docker rm`, its **image still exists**. You can re-create a fresh container from that image:

```bash
# List available images:
docker images

# Run a fresh container from the image (same environment):
docker run -it <IMAGE_NAME> bash

# Example:
docker run -it myapp-backup:v1 bash
ls    # ← same files/environment as before!
```

> 📝 The container is gone, but the **image** (snapshot) persists until you run `docker rmi`.

### 8.7 💾 `docker commit` — Save Container State as Image (Backup)

When you make changes inside a container (install packages, edit configs, write code), those changes live only in the running container and are **lost when the container is removed**. `docker commit` saves the container's current state as a **new Docker image** — a portable, shareable backup.

```bash
# Commit the container — creates a new image from it:
docker commit <CONTAINER_NAME_OR_ID>
# Output: sha256:abc123def456...  (the new image ID)

# View the new image:
docker images

# Give the image a meaningful name and tag:
docker tag <IMAGE_ID> myapp-backup:v1

# Or commit with name directly in one step:
docker commit <CONTAINER_ID> myapp-backup:v1

# Run the saved image anytime (same environment restored):
docker run -it myapp-backup:v1 bash
ls    # ← you'll see the same files you created inside the container
```

**The image stores the changes as additional layers on top of the base image:**

```bash
# Inspect layers of a committed image:
docker inspect myapp-backup:v1
# Scroll to "Layers" at the bottom →
# You'll see the base image layers + your new layer on top

# View layer history:
docker history myapp-backup:v1
```

> 💡 **What gets committed:** All filesystem changes (installed packages, new/edited files). The image stores a **diff** — only your changes, not the entire base image again.

> ⚠️ **Sharing images:** The committed image can be pushed to Docker Hub and shared with anyone. It contains your changes layered on top of the base image.

> ✅ **Best practice:** Use `docker commit` for quick backups and exploration. For reproducible production builds, always encode changes in a `Dockerfile` instead.

### 8.8 🏷️ `docker rename` — Rename a Container

```bash
# Rename an existing container:
docker rename <OLD_NAME> <NEW_NAME>

# Example:
docker rename festive_newton mywebserver
docker ps   # Now shows 'mywebserver'
```

> 📝 Renaming a container does **not** affect images previously committed from it, and doesn't interrupt the running process.

### 8.9 📋 `docker attach` — Attach to a Running Container

```bash
# Attach your terminal to a running container's STDIN/STDOUT:
docker attach <CONTAINER_NAME_OR_ID>

# ⚠️ IMPORTANT: Pressing Ctrl+C will STOP the container!
# To safely DETACH without stopping: Ctrl + P + Q
```

> 💡 Prefer `docker exec -it <container> bash` over `attach` — it opens a **new** shell session and exiting it won't stop the container.

### 8.10 📜 `docker history` — View Command History

```bash
# View the layer history of an image (commands run during build):
docker history nginx
docker history myapp-backup:v1

# Output shows each layer: size, created date, and the command that created it
```

> 📝 `docker history` shows the **image build history**, not the commands run inside the container.

### 8.11 🧹 System-Wide Cleanup

```bash
# Stop a specific container:
docker stop <CONTAINER_ID>

# Remove a stopped container:
docker rm <CONTAINER_ID>

# Force-remove a running container (stop + remove in one):
docker rm -f <CONTAINER_ID>

# Remove all stopped containers:
docker container prune

# Nuclear option — clean EVERYTHING unused
# (stopped containers, dangling images, unused networks, build cache):
docker system prune

# Include ALL unused images (not just dangling):
docker system prune --all

# Check disk usage before cleaning:
docker system df
docker system df -v      # Verbose breakdown per image/container/volume
```

---

## 9. 🗂️ Docker Volumes

Containers are **ephemeral** — data inside them is lost when the container is removed. **Volumes** provide **persistent storage** that survives container restarts and deletions.

### 9.1 Types of Storage in Docker

| Type | Description | Use Case |
|------|-------------|---------|
| 🗂️ **Volume** | Managed by Docker, stored in `/var/lib/docker/volumes/` | Databases, persistent app data |
| 📁 **Bind Mount** | Mount a host directory into the container | Development (live code editing) |
| 💾 **tmpfs Mount** | Stored in host memory only (not on disk) | Sensitive/temporary data |

```
Docker Volume:    /var/lib/docker/volumes/myvolume/_data ↔ /app/data (in container)
Bind Mount:       /home/user/project/ ↔ /app/ (in container)
tmpfs:            RAM ↔ /tmp/ (in container)
```

### 9.2 Volume Commands

```bash
# Create a named volume:
docker volume create mydata
docker volume create myvol

# List volumes:
docker volume ls

# Inspect a volume (shows mount path, driver, creation date):
docker volume inspect mydata
docker volume inspect myvol
# Output shows: Mountpoint → /var/lib/docker/volumes/myvol/_data

# Remove a volume:
docker volume rm mydata

# Remove all unused volumes:
docker volume prune
```

### 9.3 Using Volumes with Containers

```bash
# Named volume:
docker run -d -v mydata:/var/lib/mysql mysql:8.0

# Bind mount (host path):
docker run -d -v /home/user/app:/app myapp
docker run -d -v $(pwd):/app myapp         # Current directory

# Read-only bind mount:
docker run -d -v $(pwd)/config:/app/config:ro myapp

# tmpfs mount:
docker run -d --tmpfs /tmp myapp

# Multiple volumes:
docker run -d \
  -v mydata:/var/lib/mysql \
  -v myconfig:/etc/mysql/conf.d:ro \
  mysql:8.0
```

### 9.4 🔌 Practical Volume Workflow — Attach and Inspect

```bash
# Create a volume and attach it to a container:
docker volume create myvol
docker run -d --name conZ -v myvol:/app nginx

# Attach to the running container:
docker attach conZ
# Inside container:
df -kh             # 💽 Shows disk space — myvol is mounted at /app

# Detach safely (without stopping): Ctrl + P + Q

# Inspect the volume on the HOST:
docker volume inspect myvol
# Shows: Mountpoint → /var/lib/docker/volumes/myvol/_data
# You can also access this path directly on the host as root

# Cleanup:
docker kill conZ
docker rm conZ
docker volume inspect myvol   # Volume still exists even after container removal!
docker volume rm myvol        # Now explicitly remove the volume
```

> 💡 **Key insight:** Volumes persist **independently** of containers. Removing a container does **NOT** remove its associated named volume — you must explicitly run `docker volume rm` or `docker volume prune`.

### 9.5 Volume Backup and Restore

```bash
# Backup a volume:
docker run --rm -v mydata:/data -v $(pwd):/backup ubuntu \
  tar czf /backup/mydata_backup.tar.gz /data

# Restore a volume:
docker run --rm -v mydata:/data -v $(pwd):/backup ubuntu \
  tar xzf /backup/mydata_backup.tar.gz -C /
```

---

## 10. 🌐 Docker Networking

Docker networking allows containers to communicate with each other, the host, and the outside world.

### 10.1 Default Network Drivers

| Driver | Description | Use Case |
|--------|-------------|---------|
| `bridge` | Default. Creates isolated network; NAT for external access | Single host, most apps |
| `host` | Container shares host's network stack; no isolation | High-performance networking |
| `none` | No networking — completely isolated | Batch jobs, security testing |
| `overlay` | Multi-host networking for Docker Swarm | Distributed/multi-host apps |
| `macvlan` | Container gets its own MAC/IP on physical network | Legacy apps, direct LAN access |

### 10.2 Network Commands

```bash
# List networks:
docker network ls

# Create a custom network:
docker network create mynetwork
docker network create --driver bridge --subnet 172.20.0.0/16 mynetwork

# Inspect a network:
docker network inspect mynetwork

# Connect/disconnect container from network:
docker network connect mynetwork webserver
docker network disconnect mynetwork webserver

# Remove a network:
docker network rm mynetwork

# Remove all unused networks:
docker network prune
```

### 10.3 🌉 Default Bridge Network (`docker0`) — Deep Dive

Docker automatically creates the **`docker0`** bridge network during installation. All containers that don't specify a network are attached to it by default.

**Check the docker0 interface on your host:**

```bash
ip addr show
# Look for: docker0: inet 172.17.0.1/16
# docker0 is the virtual bridge interface on the host

docker network ls
# Shows: bridge, host, none (default networks)

docker inspect bridge | grep Subnet
# Output: "Subnet": "172.17.0.0/16"
```

**Communication flows on the default bridge:**

```
Container → Internet:
  Container A (172.17.0.2) → docker0 (172.17.0.1) → eth0 → Internet

Container A → Container B (same bridge):
  Container A (172.17.0.2) → docker0 → Container B (172.17.0.3)
```

**Running containers on the default bridge:**

```bash
# Start two containers on the default bridge:
docker run -td --name contA alpine
docker run -td --name contB alpine

# Check contA's IP:
docker attach contA
ip addr show eth0   # Likely: 172.17.0.2
# Detach: Ctrl + P + Q

# Check contB's IP:
docker attach contB
ip addr show eth0   # Likely: 172.17.0.3

# ❌ Ping contB from contA by NAME fails:
ping contB
# ping: bad address 'contB' — DNS is NOT supported on the default bridge!

# ✅ Ping by IP works:
ping 172.17.0.3
```

> ⚠️ **Limitation of default bridge:** Containers **cannot resolve each other by name**. You must use IP addresses — which can change between restarts.

### 10.4 🔗 User-Defined Bridge Network — DNS Support

Custom bridge networks solve the DNS problem. Containers on the same user-defined network can **communicate by container name**.

```bash
# Create a user-defined bridge network:
docker network create my-bridge

# Inspect the new network:
docker network inspect my-bridge
# Shows subnet, gateway, and connected containers

# Run containers on the custom network:
docker run -td --name contA --network my-bridge alpine
docker run -td --name contB --network my-bridge alpine

# ✅ Now ping by NAME works!
docker attach contA
ping contB      # ✅ Works! Docker's built-in DNS resolves container names
# Detach: Ctrl + P + Q
```

**Why user-defined bridges are better:**

| Feature | Default Bridge | User-Defined Bridge |
|---------|:--------------:|:------------------:|
| DNS / name resolution | ❌ No | ✅ Yes |
| Container isolation | Shared with all | ✅ Network-scoped |
| Connect/disconnect live | ❌ No | ✅ Yes |
| Custom subnet/gateway | ❌ No | ✅ Yes |

### 10.5 Container Communication

```bash
# Containers on the SAME custom network can communicate by name:
docker network create app-network

docker run -d --name database --network app-network mysql:8.0
docker run -d --name webserver --network app-network myapp

# webserver can now reach database by hostname "database":
# mysql -h database -u root -p
```

### 10.6 Network Architecture Diagram

```
┌──────────────────────────────────────────────────────┐
│                    Docker Host                       │
│                                                      │
│  ┌──────────────────────────────────────────────┐   │
│  │           bridge network (docker0)           │   │
│  │                                              │   │
│  │  ┌────────────┐         ┌────────────┐       │   │
│  │  │ Container1 │         │ Container2 │       │   │
│  │  │ 172.17.0.2 │         │ 172.17.0.3 │       │   │
│  │  └────────────┘         └────────────┘       │   │
│  └──────────────────────────────────────────────┘   │
│                      ↕ NAT                           │
│               Host: 192.168.1.100                    │
└──────────────────────────────────────────────────────┘
                         ↕
                   External Network
```

---

## 11. 🗃️ Docker Registry & Docker Hub

A **Docker Registry** is a storage and distribution system for Docker images.

### 11.1 Docker Hub — Full Push Walkthrough

🔗 https://hub.docker.com — The default public registry.

**Setup (one-time):**
1. Sign up at https://hub.docker.com using your email
2. Confirm your email address
3. Choose a unique Docker ID (username) — **must be all lowercase**
4. ⚠️ Do **not** download Docker Desktop — use CLI only

**Image naming rule for Docker Hub:**

```
ImageName format:  username/image-name:tag
                   ↑ must be lowercase   ↑ also lowercase
```

```bash
# Login to Docker Hub from terminal:
docker login
# Prompts for username and password

# Tag your local image with the correct Docker Hub format:
docker tag <IMAGE_ID> yourusername/myapp:v1
# Example:
docker tag abc123def456 hpsaurabh2022/samplewebimage:latest

# Push the image to Docker Hub:
docker push hpsaurabh2022/samplewebimage:latest

# View the pushed image at: hub.docker.com/r/hpsaurabh2022/samplewebimage

# Pull the image (public repo — no login needed):
docker pull hpsaurabh2022/samplewebimage:latest

# Pull from private repo (login required first):
docker login
docker pull hpsaurabh2022/private-repo:latest

# Run someone else's public image:
docker run -it hpsaurabh2022/samplewebimage bash

# Logout:
docker logout
```

> ⚠️ **NEVER push company code or secrets to Docker Hub.** Public repositories are visible to everyone on the internet. Use a **private registry** (ECR, GCR, ACR) for production workloads.

### 11.2 🧱 Understanding Docker Image Layers

Every Docker image is built from **multiple read-only layers**. When you push an image, Docker only pushes the **layers that don't already exist** in the registry — saving time and bandwidth.

```bash
# Build an image:
docker build -t hpsaurabh2022/samplewebimage .

# During build, you'll see multiple intermediate image IDs — one per layer
# Example output:
# Step 1/4 : FROM ubuntu:22.04         → pulls/uses base layer
# Step 2/4 : RUN apt-get install ...   → new layer created
# Step 3/4 : COPY app.py /app/         → new layer created
# Step 4/4 : CMD ["python3", "app.py"] → metadata only

# View all layers of an image:
docker history hpsaurabh2022/samplewebimage

# Inspect layers (SHA256 hashes):
docker inspect hpsaurabh2022/samplewebimage
# Scroll to "Layers" section — each hash is one layer

# Compare base image layers vs your image:
docker inspect ubuntu:22.04         # Base layers only
docker inspect hpsaurabh2022/samplewebimage  # Base layers + YOUR new layer on top
# All base layers are IDENTICAL — only the last layer differs!
```

**What happens during `docker push`:**

```
Pushing hpsaurabh2022/samplewebimage:latest
  Layer 1 (ubuntu base):    "Layer already exists" / "Mounted from library/ubuntu"
  Layer 2 (apt install):    "Layer already exists" / "Mounted from library/ubuntu"
  Layer 3 (your changes):   PUSHED  ← only this is uploaded!
```

> 💡 **Key insight:** Docker stores images as layered diffs. Your image only adds the delta on top of the base image. This is why images are efficient to store, transfer, and share.

### 11.3 📁 Where are Images Stored on the Host?

Docker stores all image data in `/var/lib/docker/`:

```bash
# Docker's data directory:
ls /var/lib/docker/
# Directories: image/, overlay2/, containers/, volumes/, network/

# Find the location of a specific image layer:
docker inspect <IMAGE_NAME>
# Look at "Layers" section → get the layer SHA/ID (shown at the bottom)

# Find the layer directory on disk using the layer ID:
cd /var/lib/docker/
find . -name "<LAYER_ID>"
# Example: find . -name "abc123def456..."

# Navigate to the layer:
cd ./overlay2/<found_path>
# → You'll see the actual filesystem contents of that layer

# List all overlay layers (one directory per image layer):
ls /var/lib/docker/overlay2/
```

> 💡 **Key concepts about Docker storage:**
> - Container data (context + metadata) → `/var/lib/docker/containers/`
> - Image layers → `/var/lib/docker/overlay2/` (one folder per layer)
> - Volume data → `/var/lib/docker/volumes/`
> - When a container is **stopped** → like shutting down a VM; processes stop, state is saved to Container Context
> - When a container is **removed** (`docker rm`) → Container Context is permanently deleted
> - Images stay in `/var/lib/docker/image/` until explicitly removed with `docker rmi`
> - Behind every image there are **multiple layers** — each `RUN`, `COPY`, `ADD` creates one layer

### 11.3a 📋 Docker Daemon Logs

```bash
# Docker daemon logs location (system-level logs):
/var/log/messages          # CentOS / RHEL / older systems
/var/log/syslog            # Ubuntu / Debian

# View daemon logs via journald (most modern systems):
journalctl -u docker.service
journalctl -u docker.service -f       # Follow live
journalctl -u docker.service --since "1 hour ago"
```

> 💡 Daemon logs show Docker service startup, errors, and system-level events — different from `docker logs <container>` which shows application output inside the container.

### 11.4 Private Registry

```bash
# Run a local private registry:
docker run -d -p 5000:5000 --name registry registry:2

# Push to local registry:
docker tag myapp:1.0 localhost:5000/myapp:1.0
docker push localhost:5000/myapp:1.0

# Pull from local registry:
docker pull localhost:5000/myapp:1.0
```

### 11.5 Cloud Registries

| Registry | Provider | Command |
|----------|---------|---------|
| Docker Hub | Docker | `docker.io/username/image` |
| ECR | AWS | `aws ecr get-login-password \| docker login --username AWS ...` |
| GCR | Google Cloud | `gcloud auth configure-docker` |
| ACR | Azure | `az acr login --name myregistry` |
| GHCR | GitHub | `echo $TOKEN \| docker login ghcr.io` |

---

## 12. 🧩 Docker Compose

**Docker Compose** is a tool for defining and running **multi-container applications** using a single YAML file (`docker-compose.yml`).

### 12.1 Why Docker Compose?

```bash
# Without Compose — manual multi-container setup:
docker network create app-net
docker volume create db-data
docker run -d --name db --network app-net -v db-data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=secret mysql:8.0
docker run -d --name web --network app-net -p 8080:80 -e DB_HOST=db myapp

# With Compose — one command:
docker compose up -d
```

### 12.2 docker-compose.yml Structure

```yaml
version: "3.9"           # Compose file version

services:
  # Web Application:
  web:
    image: myapp:latest
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8080:80"
    environment:
      - DB_HOST=db
      - DB_PORT=3306
      - DB_NAME=appdb
    env_file:
      - .env
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - ./app:/app
    networks:
      - app-network
    restart: unless-stopped
    deploy:
      resources:
        limits:
          cpus: "0.5"
          memory: 512M

  # Database:
  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: ${DB_ROOT_PASS}
      MYSQL_DATABASE: appdb
    volumes:
      - db-data:/var/lib/mysql
    networks:
      - app-network
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  # Reverse Proxy:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./certs:/etc/ssl/certs:ro
    depends_on:
      - web
    networks:
      - app-network

volumes:
  db-data:               # Named volume for database persistence
    driver: local

networks:
  app-network:           # Custom bridge network
    driver: bridge
```

### 12.3 Docker Compose Commands

```bash
# Start all services (detached):
docker compose up -d

# Build images and start:
docker compose up -d --build

# Stop all services:
docker compose down

# Stop and remove volumes too:
docker compose down -v

# View running services:
docker compose ps

# View logs:
docker compose logs
docker compose logs -f web           # Follow web service logs

# Scale a service:
docker compose up -d --scale web=3  # Run 3 web instances

# Execute command in a service container:
docker compose exec web bash
docker compose exec db mysql -u root -p

# Rebuild a specific service:
docker compose build web

# Restart a service:
docker compose restart web

# Pull latest images:
docker compose pull
```

### 12.4 restart Policies

| Policy | Behavior |
|--------|---------|
| `no` | Never restart (default) |
| `always` | Always restart regardless of exit code |
| `on-failure` | Restart only on non-zero exit code |
| `unless-stopped` | Always restart unless manually stopped |

---

## 13. 🔐 Docker Security

### 13.1 Run as Non-Root User

```dockerfile
# ❌ Bad — running as root:
FROM python:3.11
COPY app.py .
CMD ["python3", "app.py"]

# ✅ Good — running as non-root:
FROM python:3.11
RUN useradd -m -u 1001 appuser
WORKDIR /home/appuser/app
COPY --chown=appuser:appuser . .
USER appuser
CMD ["python3", "app.py"]
```

### 13.2 Use Read-Only Filesystem

```bash
docker run --read-only --tmpfs /tmp nginx
```

### 13.3 Limit Container Capabilities

```bash
# Drop ALL capabilities and add only what's needed:
docker run --cap-drop ALL --cap-add NET_BIND_SERVICE nginx
```

### 13.4 Scan Images for Vulnerabilities

```bash
# Docker Scout (built-in):
docker scout cves nginx:latest

# Trivy (popular open-source scanner):
trivy image nginx:latest
trivy image --severity HIGH,CRITICAL myapp:1.0
```

### 13.5 Use Secrets (Not Environment Variables)

```bash
# ❌ Bad — password in environment variable (visible in docker inspect):
docker run -e DB_PASSWORD=supersecret myapp

# ✅ Good — use Docker secrets (Swarm mode):
echo "supersecret" | docker secret create db_password -
docker service create --secret db_password myapp

# ✅ Good — use secret files in Compose:
```

```yaml
# docker-compose.yml with secrets:
services:
  app:
    image: myapp
    secrets:
      - db_password

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

### 13.6 Security Best Practices Summary

| Practice | Why |
|----------|-----|
| ✅ Use non-root user | Limit damage if container is compromised |
| ✅ Use minimal base images (alpine, distroless) | Smaller attack surface |
| ✅ Scan images regularly | Catch known vulnerabilities early |
| ✅ Never store secrets in images | Secrets in environment/image history are exposed |
| ✅ Use read-only filesystem | Prevent malicious file writes |
| ✅ Drop unnecessary capabilities | Follow principle of least privilege |
| ✅ Set resource limits | Prevent DoS via resource exhaustion |
| ✅ Use trusted base images only | Avoid supply chain attacks |
| ✅ Keep images up to date | Patch known CVEs |

---

## 14. 📊 Docker Resource Management

### 14.1 Limit CPU

```bash
# Limit to 0.5 CPU cores:
docker run --cpus="0.5" nginx

# Set CPU shares (relative weight, default 1024):
docker run --cpu-shares=512 nginx

# Pin to specific CPU cores:
docker run --cpuset-cpus="0,1" nginx
```

### 14.2 Limit Memory

```bash
# Limit memory to 512MB:
docker run --memory="512m" nginx

# Limit memory + swap:
docker run --memory="512m" --memory-swap="1g" nginx

# Set memory reservation (soft limit):
docker run --memory-reservation="256m" nginx
```

### 14.3 Limit Disk I/O

```bash
# Limit read speed to 10MB/s:
docker run --device-read-bps /dev/sda:10mb nginx

# Limit write IOPS:
docker run --device-write-iops /dev/sda:100 nginx
```

### 14.4 Monitor Resource Usage

```bash
# Real-time stats for all containers:
docker stats

# Stats for specific container (no-stream):
docker stats --no-stream webserver

# Output:
# CONTAINER  CPU %   MEM USAGE / LIMIT   MEM %   NET I/O    BLOCK I/O
# webserver  0.1%    10MiB / 512MiB      1.95%   1.2kB / 0B 0B / 0B
```

---

## 15. 🔍 Docker Logging & Monitoring

### 15.1 Log Drivers

Docker supports multiple logging backends:

| Driver | Description |
|--------|-------------|
| `json-file` | Default — stores logs as JSON on the host |
| `syslog` | Sends logs to the syslog daemon |
| `journald` | Sends logs to systemd journal |
| `fluentd` | Sends logs to Fluentd |
| `awslogs` | Sends logs to AWS CloudWatch |
| `splunk` | Sends logs to Splunk |
| `none` | Disables logging |

```bash
# View container logs:
docker logs webserver
docker logs -f webserver             # Follow
docker logs --tail=50 webserver      # Last 50 lines
docker logs --since="2024-01-01" webserver

# Set log driver when running:
docker run -d --log-driver=syslog nginx

# Set max log size (prevent disk fill):
docker run -d \
  --log-opt max-size=10m \
  --log-opt max-file=3 \
  nginx
```

### 15.2 Global Logging Config (`/etc/docker/daemon.json`)

```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

### 15.3 Health Checks

```dockerfile
# In Dockerfile:
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1
```

```yaml
# In docker-compose.yml:
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
  interval: 30s
  timeout: 10s
  start_period: 40s
  retries: 3
```

```bash
# Check container health status:
docker inspect --format='{{.State.Health.Status}}' webserver
```

---

## 16. 🏗️ Multi-Stage Builds

**Multi-stage builds** produce smaller, more secure final images by using one stage to **build** and another to **run** the application.

### 16.1 Without Multi-Stage (Bad — Large Image)

```dockerfile
FROM node:18
WORKDIR /app
COPY . .
RUN npm install
RUN npm run build
# Final image includes node_modules, source code, build tools → ~1GB+
CMD ["node", "dist/server.js"]
```

### 16.2 With Multi-Stage Build (Good — Small Image)

```dockerfile
# Stage 1: Build
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci                          # Install all deps (including devDependencies)
COPY . .
RUN npm run build                   # Compile TypeScript, bundle, etc.

# Stage 2: Production
FROM node:18-alpine AS production   # Tiny base image
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production        # Only production dependencies
COPY --from=builder /app/dist ./dist   # Copy ONLY built output

USER node                           # Non-root user
EXPOSE 3000
CMD ["node", "dist/server.js"]
# Final image: ~150MB instead of 1GB+
```

### 16.3 Multi-Stage for Go (Extreme Optimization)

```dockerfile
# Stage 1: Build (needs Go compiler ~800MB)
FROM golang:1.21 AS builder
WORKDIR /app
COPY go.* ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o myapp .

# Stage 2: Run (just the binary!)
FROM scratch                        # Empty base image — 0MB!
COPY --from=builder /app/myapp /myapp
EXPOSE 8080
CMD ["/myapp"]
# Final image: ~10MB!
```

---

## 17. 🚀 Docker in CI/CD

### 17.1 Docker with GitHub Actions

```yaml
# .github/workflows/docker-build.yml
name: Build and Push Docker Image

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Build and Push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: |
            myuser/myapp:latest
            myuser/myapp:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### 17.2 Docker with Jenkins

```groovy
pipeline {
    agent any
    environment {
        IMAGE = "myuser/myapp"
        TAG   = "${env.BUILD_NUMBER}"
    }
    stages {
        stage('Build Image') {
            steps {
                sh "docker build -t ${IMAGE}:${TAG} ."
            }
        }
        stage('Test') {
            steps {
                sh "docker run --rm ${IMAGE}:${TAG} npm test"
            }
        }
        stage('Push') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub')]) {
                    sh "docker push ${IMAGE}:${TAG}"
                    sh "docker tag ${IMAGE}:${TAG} ${IMAGE}:latest"
                    sh "docker push ${IMAGE}:latest"
                }
            }
        }
        stage('Deploy') {
            steps {
                sh "docker compose -f docker-compose.prod.yml up -d --force-recreate"
            }
        }
    }
    post {
        always {
            sh "docker image prune -f"
        }
    }
}
```

---

## 18. 🌊 Docker Swarm

**Docker Swarm** is Docker's built-in container orchestration tool for managing a cluster of Docker nodes.

> 💡 For large-scale production, **Kubernetes** is generally preferred. Swarm is simpler and good for smaller teams or existing Docker setups.

### 18.1 Swarm Architecture

```
┌─────────────────────────────────────────┐
│           Docker Swarm Cluster           │
│                                         │
│  ┌──────────┐  ┌──────────┐            │
│  │ Manager  │  │ Manager  │  ← Raft    │
│  │ Node 1   │  │ Node 2   │    Consensus
│  └────┬─────┘  └──────────┘            │
│       │ Schedules tasks                  │
│  ┌────▼─────┐  ┌──────────┐            │
│  │ Worker   │  │ Worker   │            │
│  │ Node 1   │  │ Node 2   │            │
│  └──────────┘  └──────────┘            │
└─────────────────────────────────────────┘
```

### 18.2 Swarm Commands

```bash
# Initialize a swarm (on manager node):
docker swarm init --advertise-addr <MANAGER-IP>

# Get join token for workers:
docker swarm join-token worker

# Join as a worker (run on worker nodes):
docker swarm join --token <TOKEN> <MANAGER-IP>:2377

# List nodes:
docker node ls

# Deploy a stack:
docker stack deploy -c docker-compose.yml myapp

# List services:
docker service ls

# Scale a service:
docker service scale myapp_web=5

# Rolling update:
docker service update --image myapp:2.0 myapp_web

# Leave the swarm:
docker swarm leave
```

---

## 19. ✅ Docker Best Practices

### 19.1 Dockerfile Best Practices

| Practice | Why |
|----------|-----|
| ✅ Use official, minimal base images | Security, smaller size |
| ✅ Use specific image tags (not `latest`) | Reproducible builds |
| ✅ Combine `RUN` commands with `&&` | Fewer layers, smaller image |
| ✅ Put frequently changing layers LAST | Better layer caching |
| ✅ Use `.dockerignore` | Faster builds, smaller context |
| ✅ Use multi-stage builds | Tiny production images |
| ✅ Run as non-root user | Security |
| ✅ Use `HEALTHCHECK` | Container self-healing |
| ✅ Don't store secrets in Dockerfile | Security — they end up in image history |

```dockerfile
# ❌ Bad — separate RUN commands, root user, no .dockerignore:
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y vim

# ✅ Good — combined, cleaned up in same layer:
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*
```

### 19.2 Tagging Strategy

```bash
# ❌ Bad — only 'latest' tag:
docker build -t myapp:latest .

# ✅ Good — semantic versioning + git SHA:
docker build -t myapp:2.1.0 -t myapp:latest .
docker build -t myapp:${GIT_SHA} .
```

### 19.3 Production Checklist

| Item | Command / Action |
|------|-----------------|
| ✅ Set memory limits | `--memory="512m"` |
| ✅ Set CPU limits | `--cpus="0.5"` |
| ✅ Enable health checks | `HEALTHCHECK` in Dockerfile |
| ✅ Use restart policy | `--restart unless-stopped` |
| ✅ Limit log size | `--log-opt max-size=10m` |
| ✅ Use named volumes | Not anonymous volumes |
| ✅ Scan for vulnerabilities | `docker scout` / `trivy` |
| ✅ Use secrets management | Docker secrets / Vault |
| ✅ Monitor with `docker stats` | Set up alerts |
| ✅ Regular `docker system prune` | Prevent disk fill |

### 19.4 Cleaning Up Docker Resources

```bash
# Remove stopped containers:
docker container prune

# Remove unused images:
docker image prune
docker image prune -a         # All unused (not just dangling)

# Remove unused volumes:
docker volume prune

# Remove unused networks:
docker network prune

# Remove EVERYTHING unused (containers, images, networks, build cache):
docker system prune
docker system prune -a        # Include all unused images

# Check disk usage:
docker system df
docker system df -v           # Verbose breakdown
```

---

## 20. ⚡ Quick Reference Cheat Sheet

### 🏗️ Build

| Command | Description |
|---------|-------------|
| `docker build -t name:tag .` | Build image from Dockerfile |
| `docker build -f Dockerfile.prod .` | Use specific Dockerfile |
| `docker build --no-cache .` | Build without layer cache |
| `docker history image` | Show image layers |

### 🖼️ Images

| Command | Description |
|---------|-------------|
| `docker images` | List local images |
| `docker pull nginx` | Pull image from registry |
| `docker push user/image:tag` | Push image to registry |
| `docker tag src:tag dest:tag` | Tag an image |
| `docker rmi image` | Remove an image |
| `docker image prune -a` | Remove all unused images |
| `docker inspect image` | Show image details |

### 📦 Containers

| Command | Description |
|---------|-------------|
| `docker run -d -p 8080:80 nginx` | Run container (detached, port mapped) |
| `docker run -it ubuntu bash` | Run interactively |
| `docker run --rm image cmd` | Run and auto-remove |
| `docker ps` | List running containers |
| `docker ps -a` | List all containers |
| `docker stop name` | Stop a container |
| `docker rm name` | Remove a container |
| `docker rm -f name` | Force remove |
| `docker exec -it name bash` | Shell into container |
| `docker logs -f name` | Follow container logs |
| `docker stats` | Live resource usage |
| `docker inspect name` | Container details |
| `docker cp name:/path ./local` | Copy from container |

### 🗂️ Volumes

| Command | Description |
|---------|-------------|
| `docker volume create name` | Create named volume |
| `docker volume ls` | List volumes |
| `docker volume rm name` | Remove volume |
| `docker volume prune` | Remove unused volumes |
| `-v name:/path` | Mount named volume |
| `-v $(pwd):/path` | Mount bind (current dir) |

### 🌐 Networking

| Command | Description |
|---------|-------------|
| `docker network ls` | List networks |
| `docker network create name` | Create network |
| `docker network inspect name` | Network details |
| `docker network connect net container` | Connect container |
| `docker network prune` | Remove unused networks |

### 🧩 Docker Compose

| Command | Description |
|---------|-------------|
| `docker compose up -d` | Start all services |
| `docker compose down` | Stop and remove services |
| `docker compose down -v` | Remove services + volumes |
| `docker compose ps` | List services |
| `docker compose logs -f` | Follow all logs |
| `docker compose exec svc bash` | Shell into service |
| `docker compose build` | Build/rebuild images |
| `docker compose pull` | Pull latest images |

### 🧹 System

| Command | Description |
|---------|-------------|
| `docker system df` | Check disk usage |
| `docker system prune` | Clean unused resources |
| `docker system prune -a` | Clean everything unused |

---

> 💡 **Key Insight:** Containers share the host OS kernel using **Namespaces** (isolation) and **cgroups** (resource limits) — that's what makes them lightweight compared to VMs.

> 🌟 **Golden Rule:** Build images small, run containers stateless, persist data in volumes, and never store secrets in images.

---

*📘 Made with ❤️ for DevOps engineers and developers learning Docker — from fundamentals to production-ready containerization.*
