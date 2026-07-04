# 🏗️ DevSecOps — IaC Security with Terraform

---

## 📑 Table of Contents

1. [What is IaC Security?](#1-what-is-iac-security)
   - 1.1 [Why IaC Security Matters](#11-why-iac-security-matters)
   - 1.2 [IaC Security Threat Surface](#12-iac-security-threat-surface)
2. [Terraform Basics and Security Posture](#2-terraform-basics-and-security-posture)
   - 2.1 [Best Practices — No Hardcoded Credentials](#21-best-practices--no-hardcoded-credentials)
   - 2.2 [Files to Always Exclude via .gitignore](#22-files-to-always-exclude-via-gitignore)
3. [Securing Terraform in Git](#3-securing-terraform-in-git)
   - 3.1 [Pre-Commit Hook — GitLeaks](#31-pre-commit-hook--gitleaks)
   - 3.2 [GitHub Actions — GitLeaks Workflow](#32-github-actions--gitleaks-workflow)
4. [Checkov — IaC Misconfiguration Scanner](#4-checkov--iac-misconfiguration-scanner)
   - 4.1 [What is Checkov?](#41-what-is-checkov)
   - 4.2 [Why Checkov is Needed](#42-why-checkov-is-needed)
   - 4.3 [Installing and Running Checkov](#43-installing-and-running-checkov)
   - 4.4 [Checkov in CI/CD Pipeline](#44-checkov-in-cicd-pipeline)
5. [Advantages of Storing Terraform in GitHub](#5-advantages-of-storing-terraform-in-github)
6. [HashiCorp Vault — Dynamic Secret Management](#6-hashicorp-vault--dynamic-secret-management)
   - 6.1 [What is Vault?](#61-what-is-vault)
   - 6.2 [GitHub Secrets vs Vault — Why Vault Wins](#62-github-secrets-vs-vault--why-vault-wins)
   - 6.3 [How Vault Works with GitHub Actions via OIDC](#63-how-vault-works-with-github-actions-via-oidc)
   - 6.4 [Installing Vault](#64-installing-vault)
   - 6.5 [Vault Configuration — Step by Step](#65-vault-configuration--step-by-step)
7. [End-to-End Demo — Terraform + Vault + GitHub Actions](#7-end-to-end-demo--terraform--vault--github-actions)
   - 7.1 [Terraform Config — S3 Bucket](#71-terraform-config--s3-bucket)
   - 7.2 [GitHub Actions Workflow — infra-set.yml](#72-github-actions-workflow--infra-setyml)
   - 7.3 [How the Full Flow Works](#73-how-the-full-flow-works)
8. [IaC Security — Defence in Depth](#8-iac-security--defence-in-depth)
9. [Summary](#9-summary)

---

## 🔐 1. What is IaC Security?

Infrastructure as Code (IaC) means your cloud infrastructure — VPCs, EC2 instances, S3 buckets, IAM roles, databases — is defined and managed through **code files** (e.g., Terraform `.tf` files). This brings all the benefits of software development to infrastructure: version control, peer review, automated testing, and repeatability.

However, it also brings **software security risks directly into your infrastructure layer**.

---

### 🔹 1.1 Why IaC Security Matters

| ⚠️ Risk | 💥 Impact |
|---|---|
| Hardcoded AWS credentials in `.tf` files | Full cloud account compromise |
| Public S3 buckets misconfigured in Terraform | Sensitive data exposed to the internet |
| `.tfstate` file committed to public repo | All infrastructure secrets leaked in plaintext |
| No peer review on Terraform PRs | Silent misconfigurations reach production |
| Long-lived CI/CD credentials in GitHub Secrets | Persistent attack vector if secrets are leaked |

> 💡 **Key mindset:** A misconfiguration in a Terraform file is not just a bug — it is a **security vulnerability** that can expose cloud accounts, databases, storage, and customer data at infrastructure scale.

---

### 🔹 1.2 IaC Security Threat Surface

```
┌─────────────────────────────────────────────────────────────────────┐
│                    IaC Security Threat Surface                      │
├──────────────────────┬──────────────────────────────────────────────┤
│  🗂️  Source Code      │  Hardcoded credentials, insecure configs     │
│  📦  Dependencies     │  Outdated provider versions with CVEs        │
│  🪣  S3 / Storage     │  Public buckets, missing encryption          │
│  🔑  Secrets          │  .tfstate, .tfvars, .env exposed in Git      │
│  🤖  CI/CD Pipeline   │  Long-lived credentials in GitHub Secrets    │
│  🌐  Network          │  Open security groups, no VPC isolation      │
│  👤  IAM              │  Over-permissive roles, wildcard policies     │
└──────────────────────┴──────────────────────────────────────────────┘
```

---

## ⚙️ 2. Terraform Basics and Security Posture

### 🔹 2.1 Best Practices — No Hardcoded Credentials

The most common — and most dangerous — IaC security mistake is hardcoding cloud credentials directly in Terraform files.

```hcl
# ❌ NEVER DO THIS — hardcoded credentials
provider "aws" {
  region     = "us-east-1"
  access_key = "AKIAIOSFODNN7EXAMPLE"       # ← hardcoded! instant compromise if pushed
  secret_key = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
}

# ✅ CORRECT — use environment variables or dynamic credentials (Vault)
provider "aws" {
  region = "us-east-1"
  # Credentials injected via environment variables:
  # AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
}
```

**Approved patterns for credential injection:**
- ✅ Environment variables in CI/CD (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`)
- ✅ **HashiCorp Vault** with short-lived dynamic credentials *(recommended — see Section 6)*
- ✅ IAM Instance Profiles / IRSA (for EKS) — no credentials at all
- ✅ AWS SSO / OIDC-based federation
- ❌ Hardcoded in `.tf` files
- ❌ Stored in `.env` files committed to Git

---

### 🔹 2.2 Files to Always Exclude via .gitignore

Terraform generates several files that **must never be committed** to a Git repository:

```gitignore
# ── Terraform State ────────────────────────────────
# Contains all infrastructure details + secrets in plaintext
*.tfstate
*.tfstate.backup

# ── Terraform Variable Files ───────────────────────
# May contain cloud credentials, DB passwords, API keys
*.tfvars
*.tfvars.json

# ── Terraform Working Directory ────────────────────
.terraform/
.terraform.lock.hcl

# ── Sensitive Environment Files ────────────────────
.env
.env.*

# ── SSH & TLS Keys ─────────────────────────────────
*.pem
*.key
id_rsa
id_rsa.pub
```

> ⚠️ **Critical:** The `.tfstate` file contains **every resource's current configuration in plaintext** — including passwords, connection strings, and IAM credentials. Even on a private repository, `.tfstate` should be stored in a **remote backend** (e.g., S3 + DynamoDB for locking), not committed to Git.

---

## 🐙 3. Securing Terraform in Git

### 🔹 3.1 Pre-Commit Hook — GitLeaks

Use **GitLeaks** as a pre-commit hook to prevent accidental commits of Terraform credentials in GitHub repositories. This is identical to the Git security setup covered in Section 01 and applies equally to Terraform repositories.

```bash
# Install pre-commit framework
brew install pre-commit          # macOS
pip install pre-commit           # Linux

# Create .pre-commit-config.yaml at repo root
vi .pre-commit-config.yaml
```

```yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.24.2
    hooks:
      - id: gitleaks
```

```bash
# Activate the hooks
pre-commit install
```

Any attempt to commit Terraform files containing AWS keys, secret keys, or tokens will be **automatically blocked** before the commit is finalised.

---

### 🔹 3.2 GitHub Actions — GitLeaks Workflow

For team-wide enforcement, add GitLeaks as a mandatory CI/CD check in `.github/workflows/gitleaks.yaml`. This acts as the **last automated safety net** — catches anything that bypasses local hooks.

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
          fetch-depth: 0
      - uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

> 💡 See **Section 01 — Git Security** for full GitLeaks setup details and all available options.

---

## 🔍 4. Checkov — IaC Misconfiguration Scanner

### 🔹 4.1 What is Checkov?

**Checkov** is an open-source static analysis tool specifically designed to scan **Infrastructure as Code files** for security misconfigurations and compliance violations — before they are ever deployed.

- Supports: **Terraform, CloudFormation, Kubernetes, Helm, Dockerfile, Bicep, ARM**
- Checks against: **CIS Benchmarks, SOC2, PCI-DSS, HIPAA, GDPR, NIST**
- Runs: locally in CLI, as a pre-commit hook, or in CI/CD pipelines
- Output: pass/fail report with CVE references and remediation guidance

---

### 🔹 4.2 Why Checkov is Needed

**Real-world scenario:**

> A junior DevOps engineer creates a Terraform config to provision an S3 bucket. They focus on getting it working and inadvertently leave the bucket publicly accessible. During code review, this misconfiguration is missed — reviewers are checking logic, not security settings. The bucket is deployed and contains sensitive data. It is discovered and scraped within hours.

**This is exactly the scenario Checkov prevents.**

Checkov catches issues like:
- 🪣 S3 bucket is publicly accessible
- 🔓 S3 bucket versioning disabled
- 🔐 S3 bucket encryption not enabled
- 🌐 Security group allows `0.0.0.0/0` on port 22 (SSH open to internet)
- 📝 CloudTrail logging disabled
- 🔑 IAM policies with wildcard `*` actions
- 🗄️ RDS instance publicly accessible
- 🔒 No MFA delete on S3 bucket

---

### 🔹 4.3 Installing and Running Checkov

**Install:**

```bash
# Install via pip
pip install checkov

# Verify installation
checkov --version
```

**Scan a Terraform directory:**

```bash
# Scan the current directory
checkov -d .

# Scan a specific Terraform file
checkov -f main.tf

# Scan and output as JUnit XML (for CI/CD integration)
checkov -d . -o junitxml > checkov-report.xml

# Scan and output as JSON
checkov -d . -o json > checkov-report.json
```

**Example — Checkov report output:**

```
Passed checks: 4, Failed checks: 3, Skipped checks: 0

Check: CKV_AWS_20: "Ensure the S3 bucket has access control list (ACL) applied"
  FAILED for resource: aws_s3_bucket.vault_test_bucket
  File: /terraform/main.tf:10-25

Check: CKV_AWS_18: "Ensure the S3 bucket has access logging enabled"
  FAILED for resource: aws_s3_bucket.vault_test_bucket
  File: /terraform/main.tf:10-25

Check: CKV_AWS_145: "Ensure that S3 buckets are encrypted with KMS by default"
  FAILED for resource: aws_s3_bucket.vault_test_bucket
  File: /terraform/main.tf:10-25
```

---

### 🔹 4.4 Checkov in CI/CD Pipeline

Add Checkov as a mandatory stage in your GitHub Actions pipeline — block deployment if any **HIGH** or **CRITICAL** misconfigurations are detected:

```yaml
name: Terraform Security Scan

on: [pull_request, push]

jobs:
  checkov:
    name: Checkov IaC Scan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'

      - name: Install Checkov
        run: pip install checkov

      - name: Run Checkov Scan
        run: |
          checkov -d ./terraform \
            --output cli \
            --output junitxml \
            --output-file-path checkov-results.xml \
            --soft-fail   # Remove this flag to fail the pipeline on any issue

      - name: Upload Checkov Results
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: checkov-results
          path: checkov-results.xml
```

> 💡 **Remove `--soft-fail`** once your team has addressed existing findings. In a mature DevSecOps pipeline, any Checkov failure should **block the PR from merging**.

---

## 📦 5. Advantages of Storing Terraform in GitHub

Keeping Terraform configuration files in a GitHub repository provides multiple benefits beyond basic version control:

| ✅ Benefit | 📖 Description |
|---|---|
| 👀 **Code Review** | Every infrastructure change goes through a PR — peers spot misconfigs before deployment |
| 🔒 **Security Scanning** | GitLeaks + Checkov run automatically on every PR via GitHub Actions |
| 💾 **Backup** | Git history is a complete, versioned backup of every infrastructure definition |
| 🕵️ **Auditing** | Full audit trail — who changed what, when, and why (via commit messages and PR descriptions) |
| 🔄 **State Auditing** | Any change to `.tfstate` (stored in remote backend) can be tracked and reviewed |
| 🤝 **Collaboration** | Multiple engineers can work on infrastructure simultaneously using branches and PRs |
| ↩️ **Rollback** | Any infrastructure change can be reverted by reverting the Git commit and re-running the pipeline |
| 📋 **Compliance** | Provides documented evidence of change management for compliance audits (SOC2, ISO 27001) |

> ⚠️ **Important:** Only Terraform **configuration files** (`.tf`) go in GitHub. Never commit `.tfstate` files — use a remote backend (S3 + DynamoDB on AWS, GCS on GCP, or Terraform Cloud).

---

## 🔑 6. HashiCorp Vault — Dynamic Secret Management

### 🔹 6.1 What is Vault?

**HashiCorp Vault** is a **secret management system** that provides short-lived, dynamically generated credentials for applications, CI/CD pipelines, and infrastructure tools — eliminating the need for long-lived static credentials entirely.

Instead of storing a permanent AWS access key in GitHub Secrets, Vault **creates a temporary IAM user on demand** (e.g., valid for 10–30 minutes), uses it for the task, and then automatically revokes it.

```
Traditional approach:              Vault approach:
GitHub Secrets:                    Vault:
  AWS_KEY = AKIA... (permanent)      → Creates IAM user (valid 30 min)
                                     → Returns key to pipeline
  Never expires ❌                   → Key auto-expires ✅
  Must be manually rotated ❌        → Zero manual rotation ✅
  Leaked = permanent access ❌       → Leaked = useless in 30 min ✅
```

---

### 🔹 6.2 GitHub Secrets vs Vault — Why Vault Wins

| 🔍 Aspect | 🔴 GitHub Secrets | 🟢 HashiCorp Vault |
|---|---|---|
| **Credential lifetime** | Long-lived (months/years) | Short-lived (minutes) |
| **Rotation** | Manual — easy to forget | Automatic — zero effort |
| **Audit trail** | Basic GitHub audit log | Full Vault audit log with request metadata |
| **Leaked credential risk** | High — key is valid until manually rotated | Minimal — key expires automatically |
| **Fine-grained access** | Limited to repo-level | Policy-based per role, per path |
| **Cloud-native integration** | Static credentials only | Dynamic IAM users, roles, tokens |
| **Compliance** | Harder to prove zero-standing-privilege | Designed for zero-standing-privilege |

> 💡 **Common assumption:** Vault is only for storing credentials (like a more secure GitHub Secrets). In reality, its core value is **generating short-lived credentials on demand** — so no long-lived credentials ever exist to be stolen.

---

### 🔹 6.3 How Vault Works with GitHub Actions via OIDC

The full end-to-end flow using **OIDC (OpenID Connect / JWT)**:

```
┌─────────────────────────────────────────────────────────────────────────┐
│              GitHub Actions + Vault + AWS — Full OIDC Flow              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  1. Developer pushes Terraform code to GitHub                           │
│         ↓                                                               │
│  2. GitHub Actions pipeline triggers                                    │
│         ↓                                                               │
│  3. Pipeline sends OIDC JWT token to Vault                              │
│         ↓                                                               │
│  4. Vault validates JWT (checks repo, branch, audience)                 │
│         ↓                                                               │
│  5. Vault requests AWS to create a short-lived IAM user                 │
│         ↓                                                               │
│  6. AWS creates temporary IAM user (valid 10–60 min)                    │
│         ↓                                                               │
│  7. Vault returns AWS_ACCESS_KEY + AWS_SECRET_KEY to pipeline           │
│         ↓                                                               │
│  8. Terraform uses credentials to create/update infrastructure          │
│         ↓                                                               │
│  9. Credentials auto-expire → IAM user auto-deleted                     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Key security properties:**
- ✅ No long-lived credentials stored anywhere in the pipeline
- ✅ Credentials scoped to the exact permissions defined in the Vault policy
- ✅ Every credential request is logged in Vault's audit log
- ✅ Leaked credentials are useless after TTL expires (10 min–1 hr)
- ✅ GitHub repository identity is cryptographically verified via OIDC

---

### 🔹 6.4 Installing Vault

Vault can be installed in two ways depending on your infrastructure:

**Option 1 — On an EC2 Instance (as a service):**

```bash
# Install Vault on Ubuntu EC2
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install vault

# Start Vault in dev mode (for testing only)
vault server -dev

# For production — configure a proper storage backend (Raft, Consul, S3)
```

**Option 2 — On Kubernetes (as a Pod/Helm chart):**

```bash
# Install Vault via Helm on Kubernetes
helm repo add hashicorp https://helm.releases.hashicorp.com
helm repo update
helm install vault hashicorp/vault \
  --namespace vault \
  --create-namespace \
  --set "server.dev.enabled=true"    # dev mode only; use HA mode for production
```

> 💡 **Practical Note:** For detailed production installation steps on both EC2 and Kubernetes, refer to HashiCorp's official documentation or use AI tools to generate environment-specific setup commands.

---

### 🔹 6.5 Vault Configuration — Step by Step

Once Vault is running, configure it to issue short-lived AWS credentials for GitHub Actions pipelines.

**Step 1 — Login to Vault:**

```bash
export VAULT_ADDR='http://127.0.0.1:8200'
vault login root
# Output: Token, accessor, policies, lease duration
```

**Step 2 — Enable the AWS Secrets Engine:**

```bash
vault secrets enable aws
# This creates the path: secrets/aws in Vault console
```

**Step 3 — Configure Vault with your AWS root credentials:**

```bash
vault write aws/config/root \
  access_key="ACCESS_KEY" \
  secret_key="SECRET_KEY" \
  region="us-east-1"
```

**Step 4 — Create an AWS IAM Role in Vault (for S3 access):**

```bash
vault write aws/roles/terraform-role \
  credential_type=iam_user \
  policy_document=-<<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:*",
      "Resource": "*"
    }
  ]
}
EOF
```

> 💡 **Scope down permissions** in production — replace `"s3:*"` and `"*"` with the exact actions and specific resource ARNs your pipeline needs. Least privilege applies here too.

**Step 5 — Enable JWT/OIDC Authentication:**

```bash
vault auth enable jwt

vault write auth/jwt/config \
  oidc_discovery_url="https://token.actions.githubusercontent.com" \
  bound_issuer="https://token.actions.githubusercontent.com"
```

**Step 6 — Create a Vault Policy:**

```bash
vault policy write terraform-policy - <<EOF
path "aws/creds/terraform-role" {
  capabilities = ["read"]
}
EOF
```

**Step 7 — Create a JWT Role for GitHub Actions:**

```bash
vault write auth/jwt/role/gh-actions-role - <<EOF
{
  "role_type": "jwt",
  "bound_audiences": ["https://github.com/iam-veeramalla"],
  "user_claim": "sub",
  "bound_claims_type": "glob",
  "bound_claims": {
    "sub": "iam-veeramalla/DevSecOps-Zero-to-Hero:*"
  },
  "token_policies": ["terraform-policy"],
  "token_ttl": "1h"
}
EOF
```

> ✅ **Vault configuration is now complete.** The pipeline is now authorised to request short-lived AWS credentials using its GitHub OIDC identity.

---

## 🚀 7. End-to-End Demo — Terraform + Vault + GitHub Actions

### 🔹 7.1 Terraform Config — S3 Bucket

Create the Terraform configuration to provision an S3 bucket:

```bash
mkdir terraform
vi terraform/main.tf
```

**`terraform/main.tf`:**

```hcl
# ── 1. Define the AWS Provider ────────────────────────────────
provider "aws" {
  region = "us-east-1"
  # Credentials injected via environment variables from Vault
}

# ── 2. Create a Random ID for unique bucket naming ────────────
resource "random_id" "bucket_suffix" {
  byte_length = 4
}

# ── 3. Create the S3 Bucket ───────────────────────────────────
resource "aws_s3_bucket" "vault_test_bucket" {
  bucket = "devsecops-vault-demo-${random_id.bucket_suffix.hex}"

  tags = {
    Name        = "Vault Dynamic Secret Test"
    Environment = "Dev"
    ManagedBy   = "Terraform"
  }
}

# ── 4. Output the bucket name (visible in GitHub Actions logs) ─
output "bucket_name" {
  value = aws_s3_bucket.vault_test_bucket.id
}
```

---

### 🔹 7.2 GitHub Actions Workflow — infra-set.yml

Create the CI/CD workflow that fetches short-lived credentials from Vault and applies the Terraform config:

```bash
mkdir -p .github/workflows/
vi .github/workflows/infra-set.yml
```

**`.github/workflows/infra-set.yml`:**

```yaml
name: Terraform Deployment

on: [push]

permissions:
  id-token: write      # Required for OIDC JWT token generation
  contents: read       # Required for actions/checkout

jobs:
  deploy:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: ./terraform

    steps:
      # ── Step 1: Checkout the repository ──────────────────────
      - uses: actions/checkout@v4

      # ── Step 2: Fetch short-lived AWS credentials from Vault ──
      - name: Fetch Keys from Vault
        uses: hashicorp/vault-action@v3
        with:
          url: http://<YOUR_EC2_IP>:8200
          role: gh-actions-role
          method: jwt
          secrets: |
            aws/creds/terraform-role access_key | AWS_ACCESS_KEY_ID ;
            aws/creds/terraform-role secret_key | AWS_SECRET_ACCESS_KEY

      # ── Step 3: Setup Terraform ───────────────────────────────
      - uses: hashicorp/setup-terraform@v3

      # ── Step 4: Initialise Terraform ──────────────────────────
      - run: terraform init

      # ── Step 5: Preview the planned changes ───────────────────
      - run: terraform plan

      # ── Step 6: Apply infrastructure changes ──────────────────
      - run: terraform apply -auto-approve
```

---

### 🔹 7.3 How the Full Flow Works

Once this workflow file is committed and pushed, here is exactly what happens:

```
1. 📤  Developer pushes code to GitHub
        ↓
2. ⚙️  GitHub Actions pipeline triggers automatically
        ↓
3. 🔐  Pipeline sends OIDC JWT token to Vault (vault-action step)
        ↓
4. ✅  Vault validates JWT — confirms the request comes from
        the correct GitHub repo and branch
        ↓
5. 🏭  Vault requests AWS to create a temporary IAM user
        with s3:* permissions (as defined in terraform-role)
        ↓
6. 🔑  AWS creates the IAM user — valid for 10–15 minutes
        ↓
7. 📬  Vault returns AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
        to the GitHub Actions environment
        ↓
8. 🏗️  Terraform init → plan → apply runs using those credentials
        ↓
9. 🪣  S3 bucket is created in AWS
        ↓
10. ⏱️  Credentials TTL expires → IAM user is automatically deleted
```

> ✅ **The main purpose of Vault here:** Provide **short-lived, zero-standing-privilege AWS credentials** to GitHub Actions via OIDC JWT — so no permanent credentials ever exist anywhere in the pipeline or codebase.

---

## 🔒 8. IaC Security — Defence in Depth

A secure IaC pipeline uses multiple overlapping controls — if one layer is missed, another catches it:

```
┌──────────────────────────────────────────────────────────────────────┐
│              IaC SECURITY — DEFENCE IN DEPTH                         │
├────────┬─────────────────────────────────────────────────────────────┤
│ Layer  │ Control                                                      │
├────────┼─────────────────────────────────────────────────────────────┤
│   1    │ 📄  .gitignore         → Block .tfstate, .tfvars, .env      │
│   2    │ 🪝  GitLeaks Hook      → Block hardcoded credentials        │
│   3    │ 🔍  Checkov (local)    → Scan .tf files before committing   │
│   4    │ 🔍  Checkov (CI/CD)    → Mandatory misconfiguration gate    │
│   5    │ ⚙️  GitLeaks Actions   → Repo-wide secret scan on every PR  │
│   6    │ 🛡️  Branch Protection  → PR + 2 approvals before merge      │
│   7    │ 🔑  Vault + OIDC       → Short-lived dynamic credentials    │
│   8    │ 📋  CODEOWNERS         → Infra changes reviewed by platform │
│   9    │ 🔒  Remote Backend     → .tfstate in S3, never in Git       │
│  10    │ 🤖  Dependabot         → Auto-update provider versions      │
└────────┴─────────────────────────────────────────────────────────────┘
```

| 🔢 Layer | 🛠️ Control | 🎯 What It Prevents |
|---|---|---|
| 1 | `.gitignore` | `.tfstate`, `.tfvars`, `.env` pushed to Git |
| 2 | GitLeaks pre-commit hook | Hardcoded AWS keys, secrets in `.tf` files |
| 3 | Checkov (local CLI) | Misconfigs caught before commit |
| 4 | Checkov (CI/CD) | Misconfigs block PR merge entirely |
| 5 | GitLeaks GitHub Actions | Secrets in any push or PR — last automated net |
| 6 | Branch Protection | Unreviewed infra changes reaching main |
| 7 | Vault + OIDC | Long-lived credentials — replaced with dynamic |
| 8 | CODEOWNERS | Terraform changes merged without platform review |
| 9 | Remote Backend | State file secrets exposed in Git history |
| 10 | Dependabot | Outdated Terraform provider versions with CVEs |

---

## ✅ 9. Summary

| 🏷️ Topic | 💡 Key Takeaway |
|---|---|
| 🏗️ **IaC Security** | Infrastructure code carries the same security risks as application code — treat it accordingly |
| 🚫 **No Hardcoded Creds** | Never hardcode AWS keys in `.tf` files — use env vars, Vault, or IAM Instance Profiles |
| 📄 **.gitignore** | Always exclude `.tfstate`, `.tfvars`, `.env`, `.pem` — state files contain plaintext secrets |
| 🪝 **GitLeaks Hook** | Block accidental credential commits in Terraform repos before they reach GitHub |
| 🔍 **Checkov** | Static IaC scanner — catches public buckets, open ports, missing encryption before deployment |
| ⚙️ **Checkov in CI/CD** | Make Checkov a mandatory PR gate — misconfigs block merge until fixed |
| 📦 **Terraform in GitHub** | Enables review, backup, auditing, rollback, and automated security scanning |
| 🔑 **HashiCorp Vault** | Dynamic secret management — generates short-lived credentials on demand via OIDC |
| 🆚 **Vault vs GitHub Secrets** | GitHub Secrets = long-lived, manual rotation; Vault = short-lived, automatic, audited |
| 🤝 **OIDC JWT Flow** | GitHub Actions authenticates to Vault via OIDC → Vault creates temp IAM user → pipeline runs → creds expire |
| ⏱️ **Short-lived Creds** | Vault creates a temporary IAM user for 10–60 min — expired and deleted automatically after use |
| 🏭 **End-to-End Flow** | Push code → Actions triggers → Vault issues creds → Terraform applies → creds auto-expire |
| 🔒 **Remote Backend** | Store `.tfstate` in S3 + DynamoDB — never in Git, never local |

---
