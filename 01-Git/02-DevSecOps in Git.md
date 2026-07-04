# 🔐 DevSecOps — Introduction & Git Security

---

## 📑 Table of Contents

1. [What is DevSecOps?](#1-what-is-devsecops)
   - 1.1 [DevOps vs DevSecOps](#11-devops-vs-devsecops)
   - 1.2 [Security Across DevOps Activities](#12-security-across-devops-activities)
2. [Shift Left Principle](#2-shift-left-principle)
3. [AI and Security](#3-ai-and-security)
4. [Threat Modeling](#4-threat-modeling)
   - 4.1 [OWASP Threat Dragon](#41-owasp-threat-dragon)
   - 4.2 [STRIDE Framework](#42-stride-framework)
5. [DevSecOps for Git](#5-devsecops-for-git)
   - 5.1 [.gitignore — Prevent Tracking Sensitive Files](#51-gitignore--prevent-tracking-sensitive-files)
   - 5.2 [Pre-Commit Hooks — Custom Scripts](#52-pre-commit-hooks--custom-scripts)
   - 5.3 [Pre-Commit Framework with GitLeaks](#53-pre-commit-framework-with-gitleaks)
   - 5.4 [GitLeaks Repository Scan](#54-gitleaks-repository-scan)
   - 5.5 [GitLeaks in CI/CD — GitHub Actions](#55-gitleaks-in-cicd--github-actions)
   - 5.6 [Branch Protection Rules](#56-branch-protection-rules)
   - 5.7 [RBAC — Role-Based Access Control](#57-rbac--role-based-access-control)
   - 5.8 [Mandatory PR Reviews](#58-mandatory-pr-reviews)
   - 5.9 [CODEOWNERS — Review by Specific Teams](#59-codeowners--review-by-specific-teams)
   - 5.10 [Dependabot — Automated Vulnerability Fixes](#510-dependabot--automated-vulnerability-fixes)
6. [Git Security — Defence in Depth](#6-git-security--defence-in-depth)
7. [Summary](#7-summary)

---

## 🛡️ 1. What is DevSecOps?

### 🔹 1.1 DevOps vs DevSecOps

**DevSecOps = DevOps + a Security Mindset.**

Traditionally, DevOps engineers focused mainly on CI/CD pipelines, Git workflows, containerisation, and infrastructure automation — but **security was largely an afterthought**, handled by a separate security team right before release. This approach left critical gaps:

- Vulnerabilities accumulated in infrastructure code throughout the entire development lifecycle
- Secrets and credentials were accidentally committed to repositories
- Third-party packages with known CVEs went undetected until late in the cycle
- Security fixes were expensive and disruptive when discovered post-deployment

> 💡 **DevSecOps shifts ownership of security** to every engineer in the software delivery pipeline — developers, DevOps engineers, and platform teams alike. Security is no longer a gate at the end; it is woven into every activity from day one.

---

### 🔹 1.2 Security Across DevOps Activities

The scope of DevSecOps is broad. Security can — and should — be introduced across **every common DevOps activity**, not just in application code:

| 🔧 DevOps Activity | ⚠️ Security Concern | ✅ DevSecOps Practice |
|---|---|---|
| **Git / Version Control** | Secrets hardcoded in commits | `.gitignore`, pre-commit hooks, GitLeaks, Dependabot |
| **IaC (Terraform)** | Cloud provider secrets in `.tfstate` or code | Store secrets in Vault; scan with Checkov or tfsec |
| **Scripting (Python / Bash)** | Vulnerable or outdated packages | Check vulnerability databases; use Snyk or Safety |
| **Containers (Docker)** | Running as root; bloated images with CVEs | Distroless images, multi-stage builds, non-root users |
| **Kubernetes (EKS)** | Exposed control plane, unrestricted network | VPCs, private subnets, RBAC, NetworkPolicies |
| **CI/CD Pipelines** | No security gates in pipeline stages | SAST, Trivy, Snyk, OWASP Dependency-Check |

> **Example:** Encoded passwords in config files can be eliminated using **pre-commit hooks** — commits are only pushed to Git if they pass security checks. Tools like **GitGuardian** can detect leaked credentials even after a commit has been pushed.

---

## ⬅️ 2. Shift Left Principle

The **Shift Left Principle** is the foundational philosophy of DevSecOps.

```
Development Start ◄─────────────────────────────────────────► Deployment
     [LEFT]                                                       [RIGHT]

Traditional Security:                          Security only checked here ──►
DevSecOps Security:        Security starts here ◄──
```

- **Left side** = Development start — writing code, infrastructure, and config
- **Right side** = Deployment — production release

**The principle:** Security must be enforced **from the very beginning** of the development process — not only at deployment or after a breach is discovered.

### 🔹 Why It Matters — Cost of Fixing Late

| 📍 Where Bug is Found | 💸 Relative Cost to Fix |
|---|---|
| Development (coding) | **1x** |
| Testing / Staging | **10x** |
| Production / Post-deployment | **100x** |

> 💡 **Shift Left means:** the earlier you catch a security issue, the cheaper, faster, and less disruptive it is to fix. Pre-commit hooks, SAST tools in the IDE, and IaC scanning are all examples of shifting security left.

---

## 🤖 3. AI and Security

AI-assisted development is rapidly changing the software landscape — and introducing new security risks that DevSecOps must actively address.

### 🔹 Current Reality

- In some companies, **AI writes 40–80% of production code**
- AI models are trained on large codebases — many of which contain **outdated, deprecated, or non-compliant packages**
- Vulnerabilities in AI-generated code may be subtle enough to **slip past human reviewers** who assume AI output is correct

### 🔹 The Risk

- AI does not always know which package versions are currently safe
- It may suggest libraries with **known CVEs** discovered after the AI model's training cutoff
- Developers who blindly trust and merge AI-generated code without security validation create new attack surfaces

### 🔹 The Solution

Build **strong, automated CI/CD security pipelines** that catch vulnerabilities regardless of whether the code was written by a human or AI:

| 🛠️ Tool | 🎯 Purpose |
|---|---|
| **Qwiet** | AI-powered SAST — detects vulnerabilities in AI-generated code |
| **Snyk** | Scans dependencies for known CVEs; integrates with IDEs and CI/CD |
| **Trivy** | Scans container images, filesystems, and IaC for vulnerabilities |
| **Dependabot** | Automatically raises PRs to update vulnerable package versions |

> ⚠️ **Key takeaway:** AI code generation does not eliminate the need for security pipelines — it makes them even more critical.

---

## 🗺️ 4. Threat Modeling

Threat modeling is the practice of **proactively identifying potential security threats** in your infrastructure and application design — before they are exploited in production.

Rather than reacting to incidents, threat modeling generates structured **security reports** (including CVE details) that help teams fully understand their attack surface.

---

### 🔹 4.1 OWASP Threat Dragon

**OWASP Threat Dragon** is a free, open-source tool for creating visual threat models of your infrastructure and application architecture.

**How it works:**

1. 🖊️ Draw your infrastructure as a **diagram** (e.g., a two-tier app with a load balancer, app servers, and database)
2. 🔍 The tool analyses the diagram and **automatically lists potential vulnerabilities** per component and data flow
3. 📄 A structured **PDF report** is generated detailing each identified threat
4. 💾 Architecture diagrams are saved as **JSON files** locally — version-controllable and shareable

**Use cases:**
- New service design review
- Cloud infrastructure security assessment
- Compliance and audit documentation
- Developer security awareness training

> 💡 **Practical:** Create threat models for your own infrastructure to understand both the vulnerabilities and the overall design of your system. Threat modeling is as much a design review tool as it is a security tool.

---

### 🔹 4.2 STRIDE Framework

OWASP Threat Dragon uses the **STRIDE Framework** internally to categorise and identify vulnerabilities. STRIDE is an acronym covering six categories of security threat:

| 🔡 Letter | 🚨 Threat | 📖 Description | 💥 Example |
|---|---|---|---|
| **S** | Spoofing | Impersonating another user or service | Forged JWT tokens, IP spoofing |
| **T** | Tampering | Modifying data in transit or at rest | Man-in-the-middle attack, DB record modification |
| **R** | Repudiation | Denying an action was performed | No audit logs, unverifiable transactions |
| **I** | Information Disclosure | Exposing data to unauthorised parties | Leaked secrets, verbose error messages |
| **D** | Denial of Service | Making a service unavailable | Resource exhaustion, DDoS attacks |
| **E** | Elevation of Privilege | Gaining higher access than intended | Container breakout, privilege escalation |

> 💡 **Instructor Tip:** STRIDE is also a great mental checklist to run through when reviewing any new infrastructure design or CI/CD pipeline change.

---

## 🐙 5. DevSecOps for Git

Git stores your **source code, infrastructure definitions, CI/CD configs, and secrets** — making it one of the highest-value targets for attackers. A single leaked credential in a public repository can lead to a complete cloud account compromise within minutes.

Securing Git is therefore one of the **highest-priority activities** in any DevSecOps programme.

> ⚠️ **Critical Reminder:** If a secret is committed and pushed — even for one second — treat it as **fully compromised**. Even after reverting the commit, the secret may already have been scraped by automated bots that monitor public repositories 24/7. **The only fix is to rotate the credential immediately.**

---

### 🔹 5.1 📄 .gitignore — Prevent Tracking Sensitive Files

The **first and simplest** line of defence. `.gitignore` instructs Git to never track certain files — preventing secrets stored in separate files from ever being committed.

**Common files that must always be in `.gitignore`:**

```
.env               # Environment variables and secrets
*.pem              # SSL/TLS private keys
*.key              # Private keys
id_rsa             # SSH private keys
*.tfstate          # Terraform state files (contain infrastructure secrets)
*.tfvars           # Terraform variable files (may contain cloud credentials)
*.p12              # Certificate files
credentials        # AWS credentials files
config             # Cloud config files
```

**Example `.gitignore`:**

```gitignore
# ── Environment & Secrets ──────────────────────────
.env
.env.*
*.secret

# ── SSH & TLS Keys ────────────────────────────────
*.pem
*.key
id_rsa
id_rsa.pub

# ── Terraform ─────────────────────────────────────
*.tfstate
*.tfstate.backup
*.tfvars
.terraform/

# ── Cloud Credentials ─────────────────────────────
credentials
.aws/
.gcp/
```

> ⚠️ **Limitation:** `.gitignore` only prevents tracking of **separate secret files**. It cannot help if secrets are **hardcoded directly inside source code** (e.g., a Python script, a Dockerfile, or a YAML manifest). That is where pre-commit hooks are needed.

---

### 🔹 5.2 🪝 Pre-Commit Hooks — Custom Scripts

**Pre-commit hooks** are scripts that run automatically **before every `git commit`** is finalised. If the script exits with a non-zero code, the commit is **blocked entirely**.

This protects against secrets hardcoded directly inside tracked files — situations where `.gitignore` provides no protection.

**Setup:**

```bash
# Navigate to the Git hooks directory
cd .git/hooks/

# Create the pre-commit hook file
touch pre-commit
vi pre-commit
```

**Example pre-commit hook script:**

```bash
#!/bin/bash
echo "Running native pre-commit hook..."

# Scan staged changes for common secret patterns
if git diff --cached | grep -iE "secret|password|token|api_key|aws_access|private_key"; then
  echo "----------------------------------------------------"
  echo "⚠️  Potential secret detected in staged changes!"
  echo "   Commit has been BLOCKED."
  echo "   Please remove the sensitive value and try again."
  echo "----------------------------------------------------"
  exit 1
fi

echo "✅ No secrets detected. Commit passed security checks."
exit 0
```

**Make the hook executable:**

```bash
chmod +x .git/hooks/pre-commit
```

**Test it:**

```bash
# Create a test file with a secret
echo "DB_PASSWORD=supersecret123" > test-config.py
git add test-config.py
git commit -m "test commit"
# Expected result: commit is BLOCKED with the warning message ✅
```

> ⚠️ **Limitation:** `.git/hooks/` is **local to each developer's machine** and is not committed to the repository. A developer who clones the repo fresh will not have the hook. For team-wide enforcement, use the pre-commit framework (Section 5.3) or CI/CD enforcement (Section 5.5).

---

### 🔹 5.3 🔍 Pre-Commit Framework with GitLeaks

The **pre-commit framework** solves the limitations of manual hook scripts by providing a standardised, shareable, configuration-driven approach. **GitLeaks** is a purpose-built secret detection tool that integrates with this framework.

**Advantages over custom scripts:**
- No need to write or maintain custom bash scripts
- Configuration lives in a **committed file** (`.pre-commit-config.yaml`) — every developer who clones the repo gets the same checks automatically
- GitLeaks uses a comprehensive, regularly updated ruleset covering **150+ secret patterns** (AWS keys, GitHub tokens, Stripe keys, GCP credentials, etc.)
- Faster and more accurate than simple `grep` patterns

**Installation and setup:**

```bash
# Step 1: Install the pre-commit framework
brew install pre-commit          # macOS
pip install pre-commit           # Linux / Python

# Step 2: Create the configuration file in the repo root
vi .pre-commit-config.yaml
```

**`.pre-commit-config.yaml`:**

```yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.24.2
    hooks:
      - id: gitleaks
```

```bash
# Step 3: Install the hooks into the local .git/hooks directory
pre-commit install

# Step 4: Test — try to commit a file containing a real secret pattern
echo "AWS_SECRET_ACCESS_KEY=AKFAH124141GKGAND" > secrets.env
git add secrets.env
git commit -m "adding secrets"
# Expected result: GitLeaks detects the AWS secret and BLOCKS the commit ✅
```

> 💡 **Instructor Tip:** Commit the `.pre-commit-config.yaml` file to the repository. This makes hook configuration version-controlled and automatically available to every developer who clones the repo and runs `pre-commit install`.

---

### 🔹 5.4 🕵️ GitLeaks Repository Scan

Beyond commit-time scanning, GitLeaks can perform a **full historical scan** of an entire repository — checking every commit ever made for secrets, passwords, tokens, or API keys.

**This is critical for:**
- Auditing repositories created before pre-commit hooks were in place
- Investigating a suspected credential leak
- Compliance audits requiring proof that no secrets exist in version history

**Command:**

```bash
gitleaks detect
```

**Recommended operational practice — schedule with cron:**

```bash
# Run a full repo scan every Sunday at 2am
0 2 * * 0 cd /path/to/repo && gitleaks detect >> /var/log/gitleaks-scan.log 2>&1
```

> 💡 **Plan:** Run `gitleaks detect` at minimum **once a week** via a scheduled cron job or a dedicated pipeline stage. Any detected secrets must trigger an immediate incident response to rotate the affected credentials.

---

### 🔹 5.5 ⚙️ GitLeaks in CI/CD — GitHub Actions

Even with pre-commit hooks installed locally, a developer might bypass them using `git commit --no-verify`, or join the team without setting up hooks. The **last line of defence** is enforcing GitLeaks as a mandatory GitHub Actions workflow that runs on every Pull Request and push.

> ⚠️ **Rule:** If none of the above methods are followed in your organisation, **this CI/CD workflow must never be skipped**. It is the safety net that catches anything slipping through every other layer.

**Setup:**

```bash
# Create the GitHub Actions workflow directory and file
mkdir -p .github/workflows/
vi .github/workflows/gitleaks.yaml
```

**`.github/workflows/gitleaks.yaml`:**

```yaml
name: gitleaks

on: [pull_request, push, workflow_dispatch]

jobs:
  scan:
    name: gitleaks
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0          # Scan full history, not just the latest commit
      - uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

**Behaviour:**
- ✅ Triggers on every **Pull Request**, every **push**, and manual runs (`workflow_dispatch`)
- ✅ Scans the **full commit history** (`fetch-depth: 0`) — not just the latest change
- ✅ If any secret is detected, the workflow **fails** and the PR cannot be merged
- ✅ Results are visible directly in the **GitHub Actions** tab of the repository

---

### 🔹 5.6 🛡️ Branch Protection Rules

Without branch protection, any team member can push directly to `main` or `master` — bypassing code review, CI/CD checks, and all security gates. Branch protection rules enforce a proper review and merge workflow.

**Setup in GitHub:**

```
GitHub Repository → Settings → Branches → Add Branch Ruleset
```

**Recommended settings:**

| ⚙️ Setting | ✅ Recommended Value | 📖 Why |
|---|---|---|
| Enforcement Status | **Active** | Rules take effect immediately |
| Target Branches | `main`, `master`, `feature-*` | Protects all key branches |
| Restrict Deletions | ✅ Enable | Prevent accidental or malicious branch deletion |
| Require Pull Request before merging | ✅ Enable | No direct pushes to protected branches |
| Require approvals | ✅ Enable (min. 2) | Peer review before every merge |
| Require status checks to pass | ✅ Enable | CI/CD and security scans must pass first |
| Block force pushes | ✅ Enable | Prevent history rewriting |

> ⚠️ **Without branch protection:** A developer — or an attacker with compromised credentials — can push directly to main, bypassing all security checks, code reviews, and GitLeaks scans in a single step.

---

### 🔹 5.7 🔑 RBAC — Role-Based Access Control

Not every team member needs full access to every repository. Applying the **principle of least privilege** to Git access limits the blast radius of a compromised account or insider threat.

**Setup in GitHub:**

```
GitHub Repository → Settings → Collaborators → Add People
→ Search for username → Assign permission level
```

**GitHub Permission Levels:**

| 🎭 Permission | 👁️ Read | ✏️ Write / Push | ⚙️ Settings | 👑 Admin |
|---|---|---|---|---|
| **Read** | ✅ | ❌ | ❌ | ❌ |
| **Triage** | ✅ | ❌ (issues only) | ❌ | ❌ |
| **Write** | ✅ | ✅ | ❌ | ❌ |
| **Maintain** | ✅ | ✅ | Partial | ❌ |
| **Admin** | ✅ | ✅ | ✅ | ✅ |

**Best practice assignments:**
- 🆕 New engineers → **Read** or **Triage** until onboarding is complete
- 👨‍💻 Active contributors → **Write**
- 👨‍🏫 Team leads → **Maintain**
- 🔐 Security / Platform team → **Admin** only where absolutely required

---

### 🔹 5.8 👥 Mandatory PR Reviews

Requiring a minimum number of approvals before a PR can be merged ensures that **at least two pairs of eyes** have reviewed every change — catching both bugs and security issues that automated tools might miss.

**Setup in GitHub:**

```
GitHub Repository → Settings → Branches → Branch Protection Rules
→ Require a pull request before merging  → ✅ Enable
→ Require approvals                       → Set to 2
```

**Why 2 approvals?**
- One reviewer may miss a subtle security issue
- Two approvals create shared accountability and reduce rubber-stamping
- Satisfies common compliance requirements: **SOC2, ISO 27001, PCI-DSS**

---

### 🔹 5.9 📋 CODEOWNERS — Review by Specific Teams

The **CODEOWNERS** file defines that certain files or directories can only be approved by **specific individuals or teams**. GitHub automatically requests the right reviewer when a matching file is changed — no manual tagging on every PR.

**Critical for:**
- Security-sensitive files (IAM policies, Terraform modules, Dockerfiles) requiring security team review
- Infrastructure changes requiring platform team approval
- Preventing sensitive configuration from being merged without expert sign-off

**Setup:**

```bash
# Create the CODEOWNERS file
vi .github/CODEOWNERS
```

**Example `CODEOWNERS` file:**

```
# ── Global — all files require core team review ────────
*                           @org/core-team

# ── Terraform — platform team must review ──────────────
/terraform/                 @org/platform-team

# ── Dockerfiles — security team must approve ───────────
**/Dockerfile               @org/security-team

# ── CI/CD Pipelines — DevOps team must approve ─────────
.github/workflows/          @org/devops-team

# ── Kubernetes Manifests — platform team must review ───
/k8s/                       @org/platform-team
```

> 💡 **How it works:** When a PR modifies a file matching a CODEOWNERS pattern, GitHub **automatically requests a review** from the designated owner. The PR cannot be merged without their approval (when combined with branch protection rules).

---

### 🔹 5.10 🤖 Dependabot — Automated Vulnerability Fixes

**Dependabot** is GitHub's built-in automated dependency management tool. It continuously monitors the packages declared in your repository and **automatically raises Pull Requests** to update any package with a known vulnerability.

**What Dependabot monitors:**

| 📦 File | 🔧 Ecosystem |
|---|---|
| `go.mod` / `go.sum` | Go modules |
| `pom.xml` | Java / Maven |
| `package.json` / `package-lock.json` | Node.js / npm |
| `requirements.txt` / `Pipfile` | Python / pip |
| `Gemfile` | Ruby |
| `Dockerfile` | Container base images |
| `.github/workflows/*.yaml` | GitHub Actions versions |

**How it works:**
1. Dependabot checks dependency files daily against the **GitHub Advisory Database** and **NVD**
2. When a vulnerability is detected, it **automatically opens a PR** with the updated version
3. The PR shows the CVE details, severity level, and the exact version change
4. Your CI/CD pipeline runs against the Dependabot PR — if checks pass, merge it

**Setup:**

```bash
mkdir -p .github/
vi .github/dependabot.yml
```

**Example `.github/dependabot.yml`:**

```yaml
version: 2
updates:

  # ── npm packages ───────────────────────────────────
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"

  # ── Python packages ────────────────────────────────
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"

  # ── Docker base images ─────────────────────────────
  - package-ecosystem: "docker"
    directory: "/"
    schedule:
      interval: "weekly"

  # ── GitHub Actions versions ────────────────────────
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

> 💡 **Instructor Tip:** Dependabot PRs should be treated with the same rigour as any code change. Always let CI/CD run fully, review the changelog for breaking changes, and merge security patches promptly.
>
> 📺 **Reference:** [Dependabot Deep Dive](https://www.youtube.com/watch?v=g85EpvD18Cc&list=PLdpzx0OAlWLlRR_KPzSKCJMf2gDNKrGd-) *(timestamp 1:17:40)*

---

## 🔒 6. Git Security — Defence in Depth

A single security control is never sufficient. The best Git security posture uses **multiple overlapping layers** — so if one control is missed or bypassed, another catches it.

```
┌──────────────────────────────────────────────────────────────────┐
│              GIT SECURITY — DEFENCE IN DEPTH                     │
├────────┬─────────────────────────────────────────────────────────┤
│ Layer  │ Control                                                  │
├────────┼─────────────────────────────────────────────────────────┤
│   1    │ 📄  .gitignore          → Block sensitive file tracking  │
│   2    │ 🪝  Pre-Commit Hook     → Scan staged changes locally    │
│   3    │ 🔍  GitLeaks Framework  → Team-shared 150+ pattern scan  │
│   4    │ 🕵️  GitLeaks Scan       → Full historical repo audit     │
│   5    │ ⚙️  GitHub Actions      → CI/CD gate on every PR/push    │
│   6    │ 🛡️  Branch Protection   → No direct pushes to main       │
│   7    │ 👥  Mandatory Reviews   → 2 human approvals required     │
│   8    │ 📋  CODEOWNERS          → Right reviewer per file/path   │
│   9    │ 🔑  RBAC                → Least-privilege repo access    │
│  10    │ 🤖  Dependabot          → Auto-fix vulnerable packages   │
└────────┴─────────────────────────────────────────────────────────┘
```

| 🔢 Layer | 🛠️ Method | 🎯 What It Catches |
|---|---|---|
| 1 | `.gitignore` | Separate secret files (`.env`, `.pem`, `.tfstate`) |
| 2 | Pre-commit hook | Hardcoded secrets in any staged file (custom patterns) |
| 3 | GitLeaks pre-commit | 150+ secret patterns — AWS, GCP, tokens, API keys |
| 4 | GitLeaks scan | Secrets buried in full commit history |
| 5 | GitHub Actions | Secrets in any PR or push — last automated safety net |
| 6 | Branch protection | Direct main-branch pushes, bypassed reviews |
| 7 | Mandatory reviews | Logic errors, subtle vulnerabilities, bad practices |
| 8 | CODEOWNERS | Changes to sensitive files without specialist review |
| 9 | RBAC | Over-privileged access, insider threats |
| 10 | Dependabot | Vulnerable third-party dependencies in package files |

---

## ✅ 7. Summary

| 🏷️ Topic | 💡 Key Takeaway |
|---|---|
| 🔐 **DevSecOps** | DevOps + security mindset — every engineer owns security, not just a separate team |
| ⬅️ **Shift Left** | Find and fix security issues at development time — exponentially cheaper than post-deployment |
| 🤖 **AI & Security** | AI writes code with outdated packages; automated pipelines (Snyk, Trivy, Qwiet) are essential |
| 🗺️ **Threat Modeling** | Use OWASP Threat Dragon + STRIDE to proactively identify vulnerabilities before building |
| 📄 **.gitignore** | First line of defence — prevents `.env`, `.pem`, `.tfstate` from ever being tracked |
| 🪝 **Pre-Commit Hook** | Blocks local commits containing hardcoded secrets — script-based, per-developer |
| 🔍 **GitLeaks Framework** | Team-shared, config-driven detection — stronger and more comprehensive than manual scripts |
| 🕵️ **GitLeaks Scan** | Full historical repo audit — run weekly via cron to catch past leaks |
| ⚙️ **CI/CD GitLeaks** | GitHub Actions safety net — mandatory on every PR; cannot be bypassed locally |
| 🛡️ **Branch Protection** | No direct pushes to main; all changes go through a reviewed and approved PR |
| 👥 **Mandatory Reviews** | Minimum 2 approvals before merge — human eyes on every single change |
| 📋 **CODEOWNERS** | Auto-assigns the right reviewer for security-sensitive files and directories |
| 🔑 **RBAC** | Least-privilege access — limits the blast radius of compromised or rogue accounts |
| 🤖 **Dependabot** | Auto-raises PRs to fix vulnerable dependencies — keeps the supply chain clean |

---
