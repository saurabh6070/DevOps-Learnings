# 🐳 DevSecOps — Container & Docker Security

---

## 📑 Table of Contents

1. [Why Container Security Matters](#1-why-container-security-matters)
   - 1.1 [Container Security Threat Surface](#11-container-security-threat-surface)
   - 1.2 [Docker Security Checklist at a Glance](#12-docker-security-checklist-at-a-glance)
2. [Run as Non-Root User](#2-run-as-non-root-user)
   - 2.1 [The Problem with Root](#21-the-problem-with-root)
   - 2.2 [Creating and Using a Non-Root User](#22-creating-and-using-a-non-root-user)
3. [Multi-Stage Builds](#3-multi-stage-builds)
   - 3.1 [Why Multi-Stage Builds Matter for Security](#31-why-multi-stage-builds-matter-for-security)
   - 3.2 [How Multi-Stage Builds Work](#32-how-multi-stage-builds-work)
   - 3.3 [Dockerfile Without Multi-Stage (~400 MB)](#33-dockerfile-without-multi-stage-400-mb)
   - 3.4 [Dockerfile With Multi-Stage (~80 MB)](#34-dockerfile-with-multi-stage-80-mb)
4. [Distroless Images](#4-distroless-images)
   - 4.1 [What Are Distroless Images?](#41-what-are-distroless-images)
   - 4.2 [Dockerfile With Distroless (~75 MB)](#42-dockerfile-with-distroless-75-mb)
   - 4.3 [Image Size and Security Comparison](#43-image-size-and-security-comparison)
5. [.dockerignore](#5-dockerignore)
   - 5.1 [Why .dockerignore is a Security Control](#51-why-dockerignore-is-a-security-control)
   - 5.2 [Example .dockerignore](#52-example-dockerignore)
6. [Hardening Docker Runtime](#6-hardening-docker-runtime)
   - 6.1 [docker run Security Flags](#61-docker-run-security-flags)
   - 6.2 [Flags Explained](#62-flags-explained)
7. [Scanning Container Images — Trivy](#7-scanning-container-images--trivy)
   - 7.1 [What is Trivy?](#71-what-is-trivy)
   - 7.2 [Installing and Running Trivy](#72-installing-and-running-trivy)
   - 7.3 [Trivy in CI/CD Pipeline](#73-trivy-in-cicd-pipeline)
8. [Docker Security in CI/CD](#8-docker-security-in-cicd)
9. [Container Security — Defence in Depth](#9-container-security--defence-in-depth)
10. [Summary](#10-summary)

---

## 🔐 1. Why Container Security Matters

Containers have transformed how we package and deploy applications. But a container is only as secure as the image it runs from and the runtime configuration it uses. A misconfigured or bloated container image can expose your entire infrastructure to attackers.

### 🔹 1.1 Container Security Threat Surface

```
┌──────────────────────────────────────────────────────────────────────┐
│              Container Security Threat Surface                       │
├──────────────────────┬───────────────────────────────────────────────┤
│  🖼️  Image Layer      │  CVEs in OS packages, outdated base images    │
│  👤  User Context     │  Running as root → container breakout risk    │
│  📦  Package Bloat    │  Unnecessary packages = larger attack surface │
│  🔑  Secrets in Image │  Hardcoded keys, tokens baked into layers     │
│  📁  Build Context    │  .env, .git, .tfstate copied into image       │
│  🔌  Runtime Flags    │  No resource limits, writable filesystem      │
│  🌐  Network          │  Unnecessary ports exposed                    │
│  🏗️  Base Image       │  Full OS images with hundreds of packages     │
└──────────────────────┴───────────────────────────────────────────────┘
```

---

### 🔹 1.2 Docker Security Checklist at a Glance

| ✅ Control | 📖 Why It Matters |
|---|---|
| Run as non-root user | Prevents privilege escalation and container breakout |
| Multi-stage builds | Reduces image size and package count → fewer CVEs |
| Distroless base images | Minimal OS footprint → smallest possible attack surface |
| `.dockerignore` | Prevents secrets and sensitive files from entering the image |
| Hardened `docker run` flags | Restricts runtime capabilities, memory, and filesystem access |
| Trivy image scanning | Detects CVEs in installed packages before deployment |
| No hardcoded secrets | Never bake credentials into image layers |

---

## 👤 2. Run as Non-Root User

### 🔹 2.1 The Problem with Root

By default, processes inside a Docker container run as **root (UID 0)**. This is a critical security risk:

- If an attacker exploits a vulnerability in your application, they gain **root access inside the container**
- Container escapes (breaking out of the container namespace) become far more dangerous when the process is already root
- Root inside a container maps to root on the host in poorly configured environments
- Compliance frameworks (PCI-DSS, CIS Docker Benchmark) explicitly require non-root container execution

```bash
# ❌ Default behaviour — process runs as root
docker run node:25 whoami
# Output: root   ← dangerous
```

---

### 🔹 2.2 Creating and Using a Non-Root User

Always create a dedicated application user and switch to it **before** the `CMD` or `ENTRYPOINT` instruction:

```dockerfile
FROM node:25
WORKDIR /app

# ── Create a non-root group and user ──────────────────────────
RUN groupadd -r appuser && useradd -r -g appuser appuser

COPY . .
RUN npm install

# ── Switch to non-root user before running the app ────────────
USER appuser

EXPOSE 3000
CMD ["npm", "start"]
```

**Verify the user at runtime:**

```bash
docker build -t secure-app .
docker run secure-app whoami
# Output: appuser   ← correct ✅
```

> ⚠️ **Important:** Switch to the non-root user **after** installing packages. Many package managers require root to install system-level dependencies. Once installation is complete, drop to the non-root user for the final running state.

---

## 🏗️ 3. Multi-Stage Builds

### 🔹 3.1 Why Multi-Stage Builds Matter for Security

Multi-stage builds are one of the **most impactful security practices** in Docker image construction. Here is why:

```
Image Size  ──────►  Package Count  ──────►  CVE Count
   ↑                      ↑                     ↑
Larger image           More packages          More vulnerabilities
= more packages        = more CVEs            = higher risk
```

> 💡 **Core principle:** Every package installed in a Docker image is a potential vulnerability. Multi-stage builds let you strip out everything that was needed only to *build* the application — keeping only what is needed to *run* it.

---

### 🔹 3.2 How Multi-Stage Builds Work

Docker image package requirements fall into two distinct categories:

```
┌────────────────────────────────────────────────────────────────────┐
│                  Build Stage vs Run Stage                          │
├────────────────────────────┬───────────────────────────────────────┤
│  🔨 Build Stage            │  🚀 Run / Execute Stage               │
├────────────────────────────┼───────────────────────────────────────┤
│  Compilers (gcc, javac)    │  Application binary / artefact        │
│  Build tools (make, cmake) │  Runtime (JRE, Node, Python)          │
│  Package managers (npm ci) │  Required runtime libraries only      │
│  Test frameworks           │  Config files                         │
│  Dev dependencies          │  ❌ No build tools needed             │
│  Source files              │  ❌ No source files needed            │
└────────────────────────────┴───────────────────────────────────────┘
```

**The main objective is to run the application.** Everything used only at build time — compilers, dev dependencies, source files, test tools — can be discarded. Only the compiled artefacts and the minimum runtime environment are carried forward into the final image.

---

### 🔹 3.3 Dockerfile Without Multi-Stage (~400 MB)

```dockerfile
# ── Single stage — everything bundled together ────────────────
FROM node:25
WORKDIR /app

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

COPY . .
RUN npm install

# Switch to non-root user
USER appuser

EXPOSE 3000
CMD ["npm", "start"]

# ⚠️ Final image includes: full Node.js, ALL npm packages
#    (including devDependencies), source files, build tools
#    Image size: ~400 MB
#    CVE exposure: HIGH (hundreds of packages present)
```

---

### 🔹 3.4 Dockerfile With Multi-Stage (~80 MB)

```dockerfile
# ────────────────────────────────────────────────────────────
# Stage 1: BUILD — install everything needed to build the app
# ────────────────────────────────────────────────────────────
FROM node:25 AS builder
WORKDIR /build

COPY package.json ./
RUN npm install          # installs all dependencies including devDeps

COPY . .                 # copy source files into build stage only

# ────────────────────────────────────────────────────────────
# Stage 2: RUNTIME — copy only the artefacts we need to run
# ────────────────────────────────────────────────────────────
FROM node:25-slim        # slim = stripped-down base image
WORKDIR /app

# Copy only the compiled output and production dependencies
COPY --from=builder /build/app.js       ./app.js
COPY --from=builder /build/node_modules ./node_modules

EXPOSE 3000
CMD ["node", "app.js"]

# ✅ Final image: node:25-slim + app.js + node_modules only
#    No build tools, no devDependencies, no source files
#    Image size: ~80 MB  (80% reduction)
#    CVE exposure: SIGNIFICANTLY LOWER
```

> 💡 **Result:** The final image goes from ~400 MB to ~80 MB — an **80% size reduction**. Fewer packages means fewer CVEs means a smaller attack surface. Build tools, dev dependencies, and source files never reach the production image.

---

## 🪶 4. Distroless Images

### 🔹 4.1 What Are Distroless Images?

**Distroless images**, maintained by Google, take the multi-stage principle even further. They contain **only the application runtime** — no shell (`bash`/`sh`), no package manager (`apt`/`yum`), no standard UNIX utilities.

**Why this matters for security:**
- No shell = attacker cannot get an interactive shell inside the container even if they compromise it
- No package manager = attacker cannot install additional tools inside the container
- Minimal OS footprint = only the libraries the runtime absolutely needs
- Passes most CIS Docker Benchmark checks by default

**Available distroless base images:**

| 🖼️ Image | 🔧 Runtime | 📦 Registry |
|---|---|---|
| `gcr.io/distroless/nodejs20-debian12` | Node.js 20 | Google Container Registry |
| `gcr.io/distroless/java21-debian12` | Java 21 JRE | Google Container Registry |
| `gcr.io/distroless/python3-debian12` | Python 3 | Google Container Registry |
| `gcr.io/distroless/base-debian12` | C/C++ glibc | Google Container Registry |
| `gcr.io/distroless/static-debian12` | Static binaries (Go) | Google Container Registry |

---

### 🔹 4.2 Dockerfile With Distroless (~75 MB)

```dockerfile
# ────────────────────────────────────────────────────────────
# Stage 1: BUILD — full Node.js environment to build the app
# ────────────────────────────────────────────────────────────
FROM node:25 AS builder
WORKDIR /build

COPY package.json ./
RUN npm install

COPY . .

# ────────────────────────────────────────────────────────────
# Stage 2: RUNTIME — distroless image (no shell, no apt, no OS)
# ────────────────────────────────────────────────────────────
FROM gcr.io/distroless/nodejs20-debian12
WORKDIR /app

# Copy only the artefacts needed at runtime
COPY --from=builder /build/app.js       ./app.js
COPY --from=builder /build/node_modules ./node_modules

EXPOSE 3000
CMD ["app.js"]         # Note: no "node" prefix needed in distroless

# ✅ Final image: distroless Node.js runtime + app only
#    No bash, no apt, no curl, no shell utilities
#    Image size: ~75 MB
#    CVE exposure: MINIMAL
```

> ⚠️ **Debugging note:** Because distroless images have no shell, you cannot `docker exec -it container bash` into them. For debugging, use a debug variant: `gcr.io/distroless/nodejs20-debian12:debug` which adds BusyBox shell temporarily.

---

### 🔹 4.3 Image Size and Security Comparison

| 🖼️ Approach | 📦 Approx. Size | 🔒 Security Level | 🛠️ Has Shell |
|---|---|---|---|
| Standard `node:25` (no multi-stage) | ~400 MB | 🔴 Low | ✅ Yes |
| `node:25-slim` with multi-stage | ~80 MB | 🟡 Medium | ✅ Yes |
| `gcr.io/distroless` with multi-stage | ~75 MB | 🟢 High | ❌ No |
| `scratch` (static binaries only) | ~10 MB | 🟢 Highest | ❌ No |

> 💡 **Rule of thumb:** Use **distroless** for production workloads wherever possible. Use **slim** variants when you need occasional debugging capability. Never use full base images in production.

---

## 🙈 5. .dockerignore

### 🔹 5.1 Why .dockerignore is a Security Control

The `COPY . .` instruction in a Dockerfile copies **everything** from the current directory into the image build context — including secrets, credentials, state files, and Git history — unless explicitly excluded.

```dockerfile
COPY . .    # ← copies EVERYTHING from source directory into the image
            #   including .env, .git, *.pem, *.tfstate if not excluded
```

A good DevSecOps engineer always creates a **`.dockerignore`** file alongside the Dockerfile. This is functionally equivalent to `.gitignore` — it tells the Docker build engine which files and directories to **exclude from the build context entirely**.

**What can go wrong without `.dockerignore`:**
- `.env` file with `DB_PASSWORD`, `API_KEY` baked into the image layer
- `.git/` directory with full commit history (including previously removed secrets) inside the image
- `*.pem`, `id_rsa` private keys shipped inside the container
- `.tfstate` files with full infrastructure details inside the image
- Development config files with staging/prod credentials included

---

### 🔹 5.2 Example .dockerignore

```bash
vi .dockerignore
```

```dockerignore
# ── Git ───────────────────────────────────────────────────────
.git
.gitignore
.github

# ── Secrets & Credentials ─────────────────────────────────────
.env
.env.*
*.pem
*.key
id_rsa
id_rsa.pub
credentials
.aws
.gcp

# ── Terraform ─────────────────────────────────────────────────
*.tfstate
*.tfstate.backup
*.tfvars
.terraform

# ── Docker itself ─────────────────────────────────────────────
Dockerfile
Dockerfile.*
.dockerignore

# ── Logs & Temp files ─────────────────────────────────────────
*.log
*.tmp
/tmp

# ── Dev & Test artifacts ──────────────────────────────────────
node_modules        # Will be installed fresh in the build stage
__pycache__
*.pyc
.pytest_cache
coverage
.nyc_output

# ── IDE & OS files ────────────────────────────────────────────
.DS_Store
.vscode
.idea
Thumbs.db
```

> ✅ **Benefit:** `.dockerignore` reduces the build context size (faster builds), prevents secrets from being baked into image layers, and ensures sensitive files never ship with your container image.

---

## 🔒 6. Hardening Docker Runtime

### 🔹 6.1 docker run Security Flags

Building a secure image is only half the story — you also need to **harden the container at runtime**. Docker provides several flags to restrict what a running container can do:

```bash
docker run \
  --read-only \                        # Filesystem is read-only
  --tmpfs /tmp \                       # Only /tmp is writable (in memory)
  --cap-drop ALL \                     # Drop ALL Linux capabilities
  --security-opt no-new-privileges \   # Prevent privilege escalation
  --pids-limit 100 \                   # Max 100 processes (prevents fork bombs)
  --memory 256m \                      # Max 256 MB RAM
  --cpus 0.5 \                         # Max 0.5 CPU cores
  -p 3000:3000 \                       # Expose only required port
  secure-app
```

---

### 🔹 6.2 Flags Explained

| 🚩 Flag | 🎯 What It Does | 🛡️ Security Benefit |
|---|---|---|
| `--read-only` | Makes the root filesystem read-only | Prevents attackers writing malware or modifying binaries |
| `--tmpfs /tmp` | Mounts `/tmp` as in-memory writable space | App can still write temp files without a writable disk |
| `--cap-drop ALL` | Drops all Linux kernel capabilities | Prevents privilege escalation, raw socket access, kernel module loading |
| `--security-opt no-new-privileges` | Prevents gaining new privileges via setuid/setgid | Blocks privilege escalation even via SUID binaries |
| `--pids-limit 100` | Limits the number of processes inside the container | Prevents fork bomb attacks and runaway processes |
| `--memory 256m` | Hard memory limit of 256 MB | Prevents container from consuming all host memory (DoS) |
| `--cpus 0.5` | Limits to 0.5 CPU cores | Prevents container from starving other workloads |
| `-p 3000:3000` | Exposes only port 3000 | Attack surface reduced to only required ports |

> 💡 **In Kubernetes:** These runtime constraints are defined in the Pod's `securityContext` and `resources` fields — same principles, declarative YAML syntax instead of `docker run` flags.

```yaml
# Kubernetes equivalent of the above docker run flags
securityContext:
  runAsNonRoot: true
  readOnlyRootFilesystem: true
  allowPrivilegeEscalation: false
  capabilities:
    drop: ["ALL"]
resources:
  limits:
    memory: "256Mi"
    cpu: "500m"
```

---

## 🔍 7. Scanning Container Images — Trivy

### 🔹 7.1 What is Trivy?

**Trivy** (by Aqua Security) is an open-source, comprehensive vulnerability scanner for container images, filesystems, Git repositories, and IaC files. It is the **industry-standard tool** for container CVE scanning in DevSecOps pipelines.

**What Trivy scans:**
- OS packages (Alpine, Ubuntu, Debian, RHEL, CentOS)
- Language-specific packages (npm, pip, gem, go modules, Maven, Cargo)
- Container image layers
- Dockerfiles (for misconfigurations)
- Kubernetes manifests
- Terraform and CloudFormation files

---

### 🔹 7.2 Installing and Running Trivy

**Install:**

```bash
# macOS
brew install trivy

# Linux (Ubuntu/Debian)
sudo apt install wget apt-transport-https gnupg
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
echo "deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/trivy.list
sudo apt update && sudo apt install trivy
```

**Scan a local Docker image:**

```bash
# Build the image first
docker build -t secure-app .

# Scan for CVEs
trivy image secure-app

# Show only HIGH and CRITICAL vulnerabilities
trivy image --severity HIGH,CRITICAL secure-app

# Scan before pushing to registry
trivy image --exit-code 1 --severity CRITICAL secure-app
# exit-code 1 = fail the pipeline if CRITICAL CVEs found
```

**Example Trivy output:**

```
secure-app (debian 12.5)
========================
Total: 12 (HIGH: 3, CRITICAL: 1, MEDIUM: 6, LOW: 2)

┌─────────────────┬────────────────┬──────────┬───────────────────┬──────────────────┐
│    Library      │ Vulnerability  │ Severity │ Installed Version │  Fixed Version   │
├─────────────────┼────────────────┼──────────┼───────────────────┼──────────────────┤
│ libssl3         │ CVE-2024-XXXX  │ CRITICAL │ 3.0.11            │ 3.0.13           │
│ zlib1g          │ CVE-2023-XXXX  │ HIGH     │ 1:1.2.13          │ 1:1.2.13.1       │
└─────────────────┴────────────────┴──────────┴───────────────────┴──────────────────┘
```

---

### 🔹 7.3 Trivy in CI/CD Pipeline

Add Trivy as a mandatory gate in your Docker build pipeline — **block deployment if CRITICAL CVEs are found**:

```yaml
name: Docker Build and Security Scan

on: [push, pull_request]

jobs:
  docker-security:
    name: Build and Scan Container Image
    runs-on: ubuntu-latest

    steps:
      # ── Step 1: Checkout code ─────────────────────────────────
      - uses: actions/checkout@v4

      # ── Step 2: Build Docker image ────────────────────────────
      - name: Build Docker Image
        run: docker build -t secure-app:${{ github.sha }} .

      # ── Step 3: Run Trivy vulnerability scan ──────────────────
      - name: Trivy Image Scan
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: secure-app:${{ github.sha }}
          format: table
          exit-code: 1                      # Fail pipeline on findings
          severity: CRITICAL,HIGH           # Only fail on HIGH and CRITICAL

      # ── Step 4: Upload scan results as artifact ───────────────
      - name: Upload Trivy Results
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: trivy-scan-results
          path: trivy-results.sarif
```

> ⚠️ **Remove `exit-code: 0` (soft fail)** once your team has a baseline scan passing. In a mature DevSecOps pipeline, any CRITICAL Trivy finding should **block the PR from merging**.

---

## ⚙️ 8. Docker Security in CI/CD

A complete, secure Docker CI/CD pipeline combines all controls in sequence:

```yaml
name: Secure Docker Pipeline

on: [push, pull_request]

jobs:
  secure-build:
    runs-on: ubuntu-latest
    steps:

      # ── 1. Checkout ───────────────────────────────────────────
      - uses: actions/checkout@v4

      # ── 2. GitLeaks — scan for secrets ────────────────────────
      - uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      # ── 3. Hadolint — lint the Dockerfile ─────────────────────
      - name: Lint Dockerfile
        uses: hadolint/hadolint-action@v3.1.0
        with:
          dockerfile: Dockerfile

      # ── 4. Build the image ────────────────────────────────────
      - name: Build Docker Image
        run: docker build -t secure-app:${{ github.sha }} .

      # ── 5. Trivy — scan image for CVEs ────────────────────────
      - name: Trivy Image Scan
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: secure-app:${{ github.sha }}
          severity: CRITICAL,HIGH
          exit-code: 1

      # ── 6. Push to registry (only if all checks pass) ─────────
      - name: Push to Registry
        run: |
          docker tag secure-app:${{ github.sha }} your-registry/secure-app:latest
          docker push your-registry/secure-app:latest
```

> 💡 **Pipeline security order:** Secrets scan → Dockerfile lint → Build → CVE scan → Push. Never push an unscanned image to a registry.

---

## 🔒 9. Container Security — Defence in Depth

A secure container posture requires multiple overlapping layers. If one layer is missed, another catches it:

```
┌──────────────────────────────────────────────────────────────────────┐
│          CONTAINER SECURITY — DEFENCE IN DEPTH                       │
├────────┬─────────────────────────────────────────────────────────────┤
│ Layer  │ Control                                                      │
├────────┼─────────────────────────────────────────────────────────────┤
│   1    │ 👤  Non-root USER       → No root access inside container   │
│   2    │ 🏗️  Multi-stage Build   → Remove build tools from image     │
│   3    │ 🪶  Distroless Image    → No shell, no OS utils, minimal    │
│   4    │ 🙈  .dockerignore       → Secrets never enter build context │
│   5    │ 🔍  Trivy Scan          → CVE gate before image is pushed   │
│   6    │ 🔒  Runtime Hardening   → read-only, cap-drop, pids-limit   │
│   7    │ 🪝  GitLeaks Hook       → No secrets in Dockerfile or code  │
│   8    │ 📋  Hadolint            → Dockerfile best-practice linting  │
│   9    │ ⚙️  CI/CD Pipeline      → All above run automatically        │
│  10    │ 🔄  Dependabot          → Auto-update base image versions   │
└────────┴─────────────────────────────────────────────────────────────┘
```

| 🔢 Layer | 🛠️ Control | 🎯 What It Prevents |
|---|---|---|
| 1 | Non-root `USER` | Privilege escalation, container breakout as root |
| 2 | Multi-stage builds | Build tool CVEs, dev dependencies in production image |
| 3 | Distroless images | Shell access, package manager abuse post-compromise |
| 4 | `.dockerignore` | `.env`, `.pem`, `.tfstate` baked into image layers |
| 5 | Trivy scan | Known CVEs in OS packages and language dependencies |
| 6 | Runtime hardening | Fork bombs, memory exhaustion, filesystem modification |
| 7 | GitLeaks | Hardcoded secrets in Dockerfiles committed to Git |
| 8 | Hadolint | Dockerfile anti-patterns and insecure instructions |
| 9 | CI/CD pipeline | Human error — all controls enforced automatically |
| 10 | Dependabot | Outdated base images with unpatched vulnerabilities |

---

## ✅ 10. Summary

| 🏷️ Topic | 💡 Key Takeaway |
|---|---|
| 🔐 **Container Security** | Every package in an image is a potential CVE — minimise aggressively |
| 👤 **Non-root User** | Always run containers as a non-root user — create one explicitly in the Dockerfile |
| 🏗️ **Multi-Stage Builds** | Split build vs runtime — discard build tools, dev deps, source files from the final image |
| 📉 **Size = Risk** | Smaller image → fewer packages → fewer CVEs → smaller attack surface |
| 🪶 **Distroless Images** | No shell, no package manager — minimal OS footprint; use for production workloads |
| 🙈 **.dockerignore** | Prevents `.env`, `.git`, `.pem`, `.tfstate` from being copied into the image |
| 🔒 **Runtime Hardening** | `--read-only`, `--cap-drop ALL`, `--pids-limit`, `--memory` limit the blast radius at runtime |
| 🔍 **Trivy** | Scan every image for CVEs before pushing — fail pipeline on CRITICAL findings |
| ⚙️ **CI/CD Pipeline** | Automate all controls: GitLeaks → Hadolint → Build → Trivy → Push |
| 📊 **Image Size Comparison** | Standard ~400 MB → Multi-stage ~80 MB → Distroless ~75 MB |

---
