# 🤖 30-Day AI DevOps Learning Plan

## 📅 Day 1 — AI Basics for DevOps

---

## 🎯 Goal for Day 1

By the end of Day 1, you should be able to:

- ✅ Understand what LLMs are and how they work at a high level
- ✅ Know where AI fits across the DevOps lifecycle
- ✅ Use ChatGPT confidently as a daily DevOps assistant

---

## 🧠 Learn

### 1️⃣ What Are LLMs?

**LLMs (Large Language Models)** are AI models trained on massive text datasets that can:

- Understand and generate natural language
- Write, explain, and debug code
- Summarize, reason, and solve problems in context

#### 🔖 Popular LLMs Used by DevOps Engineers

| Model | Strengths |
|---|---|
| **ChatGPT** (OpenAI) | Code generation, explanations, DevOps workflows |
| **Claude** (Anthropic) | Large context windows, log analysis, safe reasoning |
| **LLaMA** (Meta) | Open-source, self-hosted, privacy-friendly |

> 💡 **Key Concept:** LLMs do *pattern prediction*, not "thinking." They predict the next best token based on the context you provide — which is why **prompt quality matters enormously.**

---

### 2️⃣ Where AI Fits in DevOps

AI enhances automation, intelligence, and speed across the entire DevOps lifecycle:

---

#### 🔁 CI/CD Pipelines

- Generate pipeline configs (YAML, Groovy, etc.)
- Validate and review pull requests
- Auto-diagnose and suggest fixes for pipeline failures
- Explain cryptic build errors in plain language

```
💬 Example prompt: "Why did my GitHub Actions pipeline fail? Here's the error log: ..."
```

---

#### 📊 Monitoring & Observability

- Summarize thousands of log lines instantly
- Detect anomalies and surface patterns
- Correlate metrics, logs, and traces
- Reduce alert fatigue by filtering noise

```
💬 Example prompt: "Summarize these 10,000 lines of application logs and highlight critical errors."
```

---

#### 🔐 Security (DevSecOps)

- Identify secrets and credentials leaked in code
- Analyze vulnerability scan reports
- Explain CVEs in plain English with remediation steps
- Assist with threat modeling

```
💬 Example prompt: "Explain CVE-2024-XXXX in simple terms and suggest mitigation steps."
```

---

#### 🔍 Root Cause Analysis (RCA)

- Correlate logs, traces, and alerts from multiple sources
- Suggest probable root causes for incidents
- Dramatically reduce **MTTR** (Mean Time To Repair)

```
💬 Example prompt: "Given this nginx error log and pod crash report, what likely caused the failure?"
```

---

## 🧪 Hands-On Tasks

> **🔧 Tool Required:** ChatGPT (Free or Paid) — *Optional: GitHub Copilot, Claude*

---

### 🛠️ Task 1 — Explain a CI/CD Pipeline

**Prompt to use:**

```
Explain a CI/CD pipeline for a microservices application using Docker and Kubernetes.
Include build, test, security scan, and deploy stages with examples.
```

**✅ What to observe:**
- How clearly the AI explains complex DevOps concepts
- Whether it understands and uses correct DevOps terminology
- How well it breaks down multi-stage workflows into digestible steps

---

### 🛠️ Task 2 — Convert Bash → Python

**Bash Script:**

```bash
#!/bin/bash
for file in *.log
do
  echo "Processing $file"
done
```

**Prompt to use:**

```
Convert this bash script into Python and explain each part of the converted code.
```

**✅ Why this matters:**
- Common in migration and cross-platform scripting tasks
- Helps refactor legacy automation scripts
- Great way to learn both languages side by side

---

### 🛠️ Task 3 — Log Summarization

**Sample Log:**

```
ERROR nginx: connection refused to upstream
WARN  retrying request
INFO  service restarted
ERROR database timeout
```

**Prompt to use:**

```
Summarize these logs and identify possible root causes for each error.
```

**✅ Real-world value:**
- Faster incident diagnosis during on-call shifts
- Cuts through log noise to surface what actually matters
- Improves team response times significantly

---

## 📒 Key Concepts to Remember

| Concept | Why It Matters |
|---|---|
| **Prompt clarity** | Better prompts consistently produce better AI output |
| **Context window size** | Very long logs may need to be split into chunks |
| **AI ≠ Replacement** | AI augments DevOps engineers — it doesn't replace them |
| **Always verify output** | AI can hallucinate; critical outputs need human review |

---

## ✅ End-of-Day Checklist

You've completed Day 1 if you can:

- [ ] Explain what an LLM is in simple, non-technical terms
- [ ] Name 3 DevOps areas where AI provides real value
- [ ] Use ChatGPT to generate a pipeline explanation, convert a script, and summarize logs
- [ ] Identify situations where AI output requires human validation before use

---

---

## 📅 Day 2 — Prompt Engineering Basics

### 🎯 Goal for Day 2

By the end of Day 2, you should be able to:

- ✅ Understand the four-part anatomy of a strong prompt
- ✅ Write zero-shot prompts that produce clear, repeatable outputs
- ✅ Apply structured prompting to real DevOps tasks

---

### 🧠 Learn

#### 1️⃣ Prompt Anatomy

A well-structured prompt has four parts that work together to eliminate ambiguity:

| Part | Purpose | Example |
|---|---|---|
| **Role** | Who the AI should act as | `"Act as a DevOps engineer…"` |
| **Task** | What you want done | `"Explain CrashLoopBackOff"` |
| **Context** | Background or target audience | `"For a beginner with basic Docker knowledge"` |
| **Constraints** | Format, depth, tone, limits | `"Simple language, no jargon, under 5 sentences"` |

> 💡 **Key Insight:** Using all four parts consistently produces outputs that are clear, repeatable, and deterministic — critical for DevOps automation.

---

#### 2️⃣ Zero-Shot Prompting

**Zero-shot** means providing no examples — the model relies entirely on prompt clarity.

```
"Explain Kubernetes CrashLoopBackOff in simple terms."
```

**When to use zero-shot in DevOps:**
- Generating scripts quickly
- Explaining errors or concepts
- Creating config templates on the fly

---

### 🧪 Hands-On Tasks

#### 🛠️ Task 1 — Explain Kubernetes CrashLoopBackOff

**Prompt:**

```
Role: You are a DevOps engineer
Task: Explain CrashLoopBackOff
Context: To a beginner
Constraints: Simple language, no Kubernetes jargon, under 5 sentences
```

**✅ Example Output:**

> CrashLoopBackOff means a container in Kubernetes keeps starting and crashing repeatedly. Kubernetes tries to restart it, but since the application fails each time, it waits progressively longer between retries. This usually happens due to configuration errors, missing environment variables, or the app crashing at startup. Fixing the root cause stops the loop.

- ✅ Clear, short, beginner-friendly
- ✅ Zero-shot — no examples needed
- ✅ Deterministic and repeatable

---

#### 🛠️ Task 2 — Generate a Dockerfile for a Python Flask App

**Prompt:**

```
Role: Act as a DevOps engineer
Task: Generate a Dockerfile
Context: Python Flask application
Constraints: Lightweight, production-ready, expose port 5000
```

**✅ Resulting Dockerfile:**

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

- ✅ Lightweight and production-ready
- ✅ Deterministic output
- ✅ Easily pluggable into CI/CD pipelines

---

### ✅ End-of-Day Checklist

- [ ] Understand the four components of a strong prompt
- [ ] Write a zero-shot prompt for a DevOps concept explanation
- [ ] Use structured prompts to generate a working Dockerfile
- [ ] Recognize when zero-shot is sufficient vs when examples are needed

---
---

## 📅 Day 3 — One-Shot & Few-Shot Prompting

### 🎯 Goal for Day 3

Learn how to embed examples directly in prompts to get structured, consistent, and reliable outputs — especially for logs, alerts, and automation pipelines.

---

### 🧠 Learn

#### 1️⃣ One-Shot vs Few-Shot Prompting

| Type | Meaning | When to Use |
|---|---|---|
| **Zero-Shot** | No examples provided | Task is simple or widely understood |
| **One-Shot** | One example provided | Output format needs to be matched exactly |
| **Few-Shot (n-shot)** | 2–5 examples provided | Pattern recognition or consistency is required |

> 💡 **Key Insight:** Examples reduce ambiguity. They're extremely useful in DevOps automation when working with logs, JSON, YAML, and CI reports.

---

#### 2️⃣ When to Use Examples

Reach for one-shot or few-shot prompting when:

- You need structured output: JSON, YAML, tables
- Log formats are inconsistent or noisy
- You want the AI to match your exact output format
- Previous zero-shot outputs were too variable

---

### 🧪 Hands-On Tasks

#### 🛠️ Task 1 — One-Shot Log Analysis

**Prompt:**

```
Role: Act as a DevOps incident analyst
Task: Analyze application logs
Context: Production Kubernetes environment

Example:
  Input:
  ERROR [2026-04-14 10:21:30] Connection timeout while connecting to database
  
  Output:
  Root cause: Database unreachable.
  Suggested action: Check network policy and database service status.

Now analyze the following log:
ERROR [2026-04-15 09:11:02] Authentication failed for service account
```

**✅ Expected Output:**

```
Root cause: Invalid or expired service account credentials.
Suggested action: Verify credentials and rotate secrets if needed.
```

- ✅ Output structure matches the example exactly
- ✅ One example was sufficient — classic one-shot

---

#### 🛠️ Task 2 — Few-Shot Log Severity Classification

**Prompt:**

```
Role: Act as a DevOps log classification system
Task: Classify logs into severity levels

Examples:
  Log: INFO Server started successfully
  Severity: LOW

  Log: WARN Disk usage above 80%
  Severity: MEDIUM

  Log: ERROR Pod OOMKilled
  Severity: HIGH

Now classify:
ERROR Image pull failed due to unauthorized access
```

**✅ Expected Output:**

```
Severity: HIGH
```

- ✅ Few examples teach pattern recognition effectively
- ✅ Classification is consistent and predictable

---

#### 🛠️ Task 3 — Force JSON-Structured Output

**Prompt:**

```
Role: Act as a DevOps automation assistant
Task: Analyze the following log entry
Constraints: Return output ONLY in JSON format — no additional text

Log: ERROR Container restarted 5 times due to CrashLoopBackOff
```

**✅ Expected Output:**

```json
{
  "severity": "HIGH",
  "issue": "CrashLoopBackOff",
  "possible_cause": "Application crashing on startup",
  "recommended_action": "Check application logs and configuration"
}
```

- ✅ Machine-readable and CI/CD-friendly
- ✅ Directly usable in Slack bots, Jenkins pipelines, or auto-ticketing systems

---

### ✅ End-of-Day Checklist

- [ ] Explain the difference between zero-shot, one-shot, and few-shot prompting
- [ ] Use a one-shot prompt to get consistently structured log analysis
- [ ] Apply few-shot prompting for log severity classification
- [ ] Force JSON output from a log analysis prompt

---
---

## 📅 Day 4 — Advanced Prompting Techniques

### 🎯 Goal for Day 4

Design production-grade prompts that:

- Enforce appropriate roles for context-aware reasoning
- Control reasoning depth and structure
- Produce consistent, automation-ready outputs

---

### 🧠 Learn

#### 1️⃣ Role Prompting

Role prompting tells the AI who it is, so it applies the right mental model, vocabulary, and priorities.

**Examples:**
- `"Act as a Kubernetes SRE"`
- `"Act as a production incident commander"`
- `"Act as a CI/CD reliability engineer"`

This improves:
- Correctness of technical vocabulary
- Prioritization of recommendations
- Actionability of suggested fixes

---

#### 2️⃣ Chain-of-Thought (Controlled Reasoning)

Chain-of-thought means asking the AI to reason step by step. In DevOps contexts, you want this reasoning to be:

- Structured and predictable
- Concise and operational
- Safe for production environments

> 💡 **Best Practice:** Ask for explicit sections rather than free-form reasoning.

```
"Provide analysis in clear steps: Symptoms → Root Cause → Impact → Fix"
```

---

#### 3️⃣ Constraints & Formatting

Constraints are what transform AI into a reliable automation tool.

**Common DevOps constraints:**
- Output as JSON or YAML
- Limit verbosity — no padding or filler
- No assumptions about missing information
- Use production-safe, operational language

> 💡 **Constraints = Deterministic outputs.** Treat them as required parameters, not optional polish.

---

### 🧪 Hands-On Tasks

#### 🛠️ Task 1 — Kubernetes Log Analysis (Production-Grade)

**Prompt:**

```
Role: You are a Kubernetes Site Reliability Engineer
Task: Analyze the following application logs
Context: Production Kubernetes cluster
Instructions:
  - Analyze step by step
  - Separate output into: Symptoms, Root Cause, Impact, Remediation
  - Do not assume missing information
  - Keep output concise and operational

Logs:
ERROR Pod my-app-7f9c8b restarted multiple times
Warning BackOff restarting failed container
```

**✅ Expected Output:**

```
Symptoms
- Pod is restarting repeatedly
- Kubernetes is reporting BackOff for container restarts

Likely Root Cause
- Application is failing during startup
- Possible causes: misconfiguration, missing environment variables, or application crash

Impact
- Application is unavailable or degraded
- Active requests may be failing or dropped

Recommended Remediation
- Inspect container logs: kubectl logs <pod-name>
- Validate environment variables and ConfigMaps
- Check resource limits and application startup dependencies
```

- ✅ Matches SRE reasoning patterns
- ✅ Structured, readable, and actionable
- ✅ Safe for production incident documentation

---

#### 🛠️ Task 2 — Same Prompt, JSON Output (Automation-Ready)

Add this constraint to the prompt above:

```
Constraints: Output JSON only — no additional text, no explanation.
```

**✅ Expected Output:**

```json
{
  "symptoms": [
    "Pod restarting repeatedly",
    "BackOff warning from Kubernetes"
  ],
  "likely_root_cause": "Application crashing during startup",
  "impact": "Service instability or downtime",
  "recommended_actions": [
    "Check container logs with kubectl logs",
    "Verify configuration and environment variables",
    "Validate resource limits and startup dependencies"
  ]
}
```

**✅ Perfect for:**
- CI/CD pipeline integrations
- Slack or Webex alert bots
- Automated ticket creation
- Monitoring system webhooks

---

### ✅ End-of-Day Checklist

- [ ] Write a role prompt appropriate for an SRE or incident response scenario
- [ ] Use chain-of-thought structure in a log analysis prompt
- [ ] Apply constraints to produce JSON output from a Kubernetes log
- [ ] Combine role + structured reasoning + constraints in a single production-grade prompt

---
---

## 📅 Day 5 — Prompt Testing & Refinement

### 🎯 Goal for Day 5

Develop prompt debugging skills so your prompts remain stable, repeatable, and safe for production use and automation pipelines.

---

### 🧠 Learn

#### 1️⃣ Why Prompts Break

Prompts fail for predictable, fixable reasons:

**a) Ambiguity**
- Vague verbs: *analyze*, *explain*, *fix* — without scope
- No definition of expected output format or depth

**b) Missing Constraints**
- No format specified → inconsistent, unpredictable outputs
- No scope defined → model fills gaps with hallucinations

**c) Context Drift**
- AI assumes details you didn't provide
- Environment not specified (prod vs staging vs dev)

**d) Overloaded Prompts**
- Too many tasks bundled into one prompt
- No prioritization — model picks what to focus on

> 💡 **Mental Model:** Treat prompts like API calls. Unclear inputs reliably produce unreliable outputs.

---

#### 2️⃣ Prompt Versioning

Treat prompts like code — version them, track changes, and change one thing at a time.

**Best practices:**
- Name versions clearly: `prompt-analyze-logs-v1`, `v2`, `v3`
- Change one variable per iteration
- Document *why* each version was updated

**Example changelog:**
```
prompt-analyze-logs-v3
- Added JSON output constraint
- Removed ambiguous verb "check"
- Added explicit instruction: do not assume missing information
```

> ✅ Especially important for CI/CD pipelines, alerting bots, and automated workflows.

---

#### 3️⃣ Reducing Hallucinations

Hallucinations occur when the AI fills knowledge gaps with plausible-sounding guesses.

**Techniques to reduce them:**
- Explicitly state: `"Do not assume missing information"`
- Instruct the model to flag unknowns: `"If data is missing, state 'insufficient data'"`
- Narrow the scope and specify the environment clearly

---

### 🧪 Hands-On Tasks

#### 🛠️ Task 1 — Compare Three Prompts, Measure Quality

**🔴 Prompt A — Weak**

```
Analyze this Kubernetes error and suggest a fix.
```

❌ Problems: No role, no context, no format, high hallucination risk

---

**🟡 Prompt B — Better**

```
Act as a DevOps engineer. Analyze this Kubernetes error and suggest a fix.
```

✅ Role added — but still vague, unstructured, and open-ended

---

**🟢 Prompt C — Production-Grade**

```
Role: Act as a Kubernetes SRE
Task: Analyze the following error
Context: Production Kubernetes cluster
Constraints:
  - Do not assume missing information
  - Separate output into: Symptoms, Root Cause, Remediation
  - Keep output concise and operational

Error: BackOff restarting failed container
```

✅ Clear scope, structured output, low hallucination risk, fully reusable

---

#### 📊 Output Quality Comparison

| Prompt | Consistency | Structure | Hallucination Safety |
|---|---|---|---|
| **Prompt A** | ❌ Low | ❌ None | ❌ Risky |
| **Prompt B** | ⚠️ Medium | ❌ Weak | ⚠️ Medium |
| **Prompt C** | ✅ High | ✅ Strong | ✅ Safe |

---

#### 🛠️ Task 2 — Rewrite a Weak Prompt

**❌ Original Prompt:**

```
Check this CI failure and explain what went wrong.
```

**✅ Refined Prompt (v2):**

```
Role: Act as a CI/CD reliability engineer
Task: Analyze the following CI pipeline failure
Context: Jenkins build on the production branch
Constraints:
  - Identify the stage where the failure occurred
  - Provide the most likely cause
  - Suggest the next concrete debugging step
  - Do not assume missing log data

Failure Log: <paste log here>
```

- ✅ Clear inputs → predictable outputs
- ✅ Minimal hallucination risk
- ✅ Directly reusable across pipeline failures

---

### ✅ End-of-Day Checklist

- [ ] Identify the four common reasons a prompt breaks
- [ ] Compare a weak, medium, and production-grade prompt for the same task
- [ ] Rewrite a vague prompt using role, task, context, and constraints
- [ ] Apply at least one hallucination-reduction technique
- [ ] Adopt a versioning habit for prompts used in automation

---

---

## 📅 Day 6 — AI for Real DevOps Tasks

### 🎯 Goal for Day 6

Apply AI to four high-value, everyday DevOps workflows:

- RCA generation after incidents
- YAML explanation and review
- Helm values pre-deployment checks
- Security scan summarization

> By the end of today, AI should feel like a natural part of your daily DevOps toolkit.

---

### 🧪 Practice Use Cases

#### 🛠️ Use Case 1 — RCA (Root Cause Analysis) Generation

**Scenario:** A production incident occurred — service down, latency spike, pod crash, or pipeline failure.

**Prompt:**

```
Generate an RCA for the following incident:

- Date: 23 Apr 2026
- Impact: Checkout service unavailable for 15 minutes
- Symptoms:
    - Pods restarted repeatedly
    - Error: "OOMKilled"
- Environment: Kubernetes, 3 replicas
- Recent change: New release deployed 10 minutes before incident

Provide:
- Summary
- Root cause
- Contributing factors
- Resolution
- Preventive actions
```

**✅ Expected Output Structure:**

| Section | Example Content |
|---|---|
| **Incident Summary** | Service outage for 15 min, checkout impacted |
| **Root Cause** | Memory limit too low / memory leak introduced in release |
| **Contributing Factors** | No HPA, missing memory requests, no pre-deploy load test |
| **Resolution** | Rollback deployment, increase memory limits |
| **Preventive Actions** | Load testing in staging, alerting on OOM events, LimitRange policies |

> 💡 **Daily Use Tip:** Run this prompt after every Sev-2 or Sev-3 incident to standardize RCAs and save hours of post-incident writing.

---

#### 🛠️ Use Case 2 — YAML Explanation

**Sample YAML:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: checkout
spec:
  replicas: 3
  selector:
    matchLabels:
      app: checkout
  template:
    metadata:
      labels:
        app: checkout
    spec:
      containers:
      - name: checkout
        image: checkout:v2
        resources:
          limits:
            memory: "512Mi"
            cpu: "500m"
```

**Prompt:**

```
Explain this Kubernetes YAML line by line.
Highlight potential issues and suggest best practices.
```

**✅ What AI Should Catch:**
- What each field does and why it matters
- Missing `resources.requests` (only `limits` defined)
- No `readinessProbe` or `livenessProbe`
- No `imagePullPolicy` defined
- No annotations for monitoring or alerting

> 💡 **Daily Use Tip:** Any YAML you don't fully understand → paste it into AI before deploying.

---

#### 🛠️ Use Case 3 — Helm Values Review

**Sample `values.yaml`:**

```yaml
replicaCount: 1
resources:
  limits:
    cpu: 100m
    memory: 128Mi
autoscaling:
  enabled: false
service:
  type: LoadBalancer
```

**Prompt:**

```
Review this Helm values.yaml from a production readiness perspective.
Suggest improvements and flag risks.
```

**✅ Expected Feedback:**

| Flag | Issue |
|---|---|
| 🚩 | Single replica — no high availability |
| ⚠️ | Memory limit of 128Mi is likely too low for production |
| ⚠️ | HPA disabled — no auto-scaling under load |
| 🚩 | `LoadBalancer` type exposes service publicly |
| ✅ | Suggest separate prod vs non-prod values files |

> 💡 **Daily Use Tip:** Make AI your Helm reviewer before every release PR.

---

#### 🛠️ Use Case 4 — Security Scan Summary

**Sample Input (Trivy / Snyk / Prisma output):**

```
CRITICAL: openssl 1.1.1 vulnerable to CVE-2023-0286
HIGH:     curl <7.87.0 vulnerable to CVE-2023-23916
LOW:      bash informational issue
```

**Prompt:**

```
Summarize this security scan for engineering leadership.
Include risk level, impact, and remediation priority for each finding.
```

**✅ Expected Output:**
- Executive-friendly summary with plain-language impact
- Clear split: what needs an immediate fix vs what goes to backlog
- Specific upgrade recommendations per package
- Deployment risk assessment for the current build

> 💡 **Daily Use Tip:** AI turns raw security scan output into actionable decisions — not just noise.

---

### ✅ End-of-Day Checklist

- [ ] Generate a structured RCA using AI from a sample incident
- [ ] Paste a Kubernetes YAML and identify AI-flagged issues
- [ ] Review a Helm `values.yaml` for production readiness gaps
- [ ] Convert a raw security scan output into a leadership-ready summary

---
---

## 📅 Day 7 — DevOps Prompt Library

### 🎯 Goal for Day 7

Build a personal, reusable prompt library for high-impact day-to-day DevOps work — so you spend less time writing prompts and more time using them.

---

### 📌 How to Use This Library

1. Copy the prompt
2. Replace placeholders (`< >`) with your actual data
3. Paste into ChatGPT, Claude, or GitHub Copilot
4. Iterate with follow-up questions as needed

---

### 🔧 Kubernetes Troubleshooting Prompts

#### 1️⃣ Pod Crash / Restart Loop

```
You are a Kubernetes expert.
Analyze the following issue and provide:
- Root cause
- Evidence from logs and events
- Immediate fix
- Long-term prevention

kubectl describe pod output:
<PASTE HERE>

kubectl logs output:
<PASTE HERE>
```

---

#### 2️⃣ OOMKilled / Resource Issues

```
Investigate this Kubernetes pod being OOMKilled.
Provide:
- Why it happened
- Whether the current limits and requests are appropriate
- Recommended corrected values
- Monitoring and alerting improvements

Pod spec:
<PASTE POD YAML>

Metrics (if available):
<PASTE METRICS>
```

---

#### 3️⃣ Service Not Reachable

```
A Kubernetes service is not reachable from within the cluster.
Analyze:
- Service type and configuration
- Whether selectors match pod labels
- Endpoints status
- Potential network policy impact

Service YAML:
<PASTE SERVICE YAML>

Pod labels:
<PASTE LABELS>
```

---

### 🐳 Docker Optimization Prompts

#### 4️⃣ Dockerfile Optimization

```
Review the following Dockerfile.
Goals:
- Reduce final image size
- Improve build layer caching
- Follow security best practices

Dockerfile:
<PASTE DOCKERFILE>
```

---

#### 5️⃣ Slow Docker Builds

```
My Docker builds are taking too long.
Analyze this Dockerfile and suggest:
- Layer caching improvements
- Optimal instruction ordering
- Where to apply multi-stage builds

Dockerfile:
<PASTE DOCKERFILE>
```

---

#### 6️⃣ Container Security Review

```
Review this Dockerfile from a security perspective.
Check for:
- Root user usage
- Vulnerable or outdated base images
- Secrets or credentials exposure
- Runtime hardening opportunities

Dockerfile:
<PASTE DOCKERFILE>
```

---

### 🔁 CI/CD Pipeline Prompts

#### 7️⃣ Pipeline Failure Analysis

```
Analyze the following CI/CD pipeline failure.
Provide:
- Root cause of the failure
- Explanation of the failing stage
- Quick fix to unblock the build
- Preventive improvements for future runs

Pipeline logs:
<PASTE LOGS>
```

---

#### 8️⃣ CI/CD Best Practices Review

```
Review this CI/CD pipeline configuration.
Evaluate across four dimensions:
- Security
- Performance
- Maintainability
- Environment separation (dev / staging / prod)

Pipeline YAML:
<PASTE PIPELINE YAML>
```

---

#### 9️⃣ Pre-Merge Safety Check

```
Act as a senior DevOps reviewer.
Review this change before it is merged to main:
- Identify risks
- Flag missing checks or gates
- Assess rollback readiness
- Describe potential production impact

Change details:
<PASTE PR / DIFF / CONFIG>
```

---

### 🛡️ Bonus — Production Readiness Assessment

```
Assess the production readiness of the following service.
Evaluate across five pillars:
- Scalability
- Resilience and fault tolerance
- Observability (logs, metrics, traces)
- Security posture
- Cost risks

Architecture and configs:
<PASTE DETAILS>
```

---

### 📈 Suggested Next Steps

- Version this library in a Git repo
- Add real incident examples as context
- Tag prompts by severity: `P0 / P1 / P2`
- Share with your team as a shared prompt runbook

---

### ✅ End-of-Day Checklist

- [ ] Save the full prompt library to your own repo or notes
- [ ] Test at least 3 prompts with real or sample data
- [ ] Customize placeholders for your actual stack and tooling
- [ ] Identify 1–2 prompts you'll use this week in real work

---
---

## 📅 Day 8 — Local LLMs Overview

### 🎯 Goal for Day 8

Understand why local Large Language Models matter for DevOps, and get hands-on with Ollama and Hugging Face.

---

### 🧠 Learn

#### 1️⃣ Why Local Models Matter

Local LLMs run directly on your machine or internal infrastructure — no cloud API, no external data transmission.

**✅ Key Advantages:**

| Advantage | Detail |
|---|---|
| 🔐 **Privacy** | Data never leaves your system |
| 💰 **Cost Efficiency** | No per-request API cost |
| ⚡ **Low Latency** | No network round-trip |
| 📴 **Offline Capability** | Works in air-gapped or restricted environments |

**⚖️ Trade-offs vs Cloud LLMs:**

| Factor | Local Models | Cloud Models |
|---|---|---|
| Cost | Low (one-time infra) | Pay-per-use |
| Privacy | High | Depends on provider |
| Latency | Low | Network dependent |
| Setup effort | Medium | Easy |
| Scale | Limited | Highly scalable |

---

#### 2️⃣ Tool 1 — Ollama

Ollama lets you run LLMs locally with minimal setup via a simple CLI.

**Install:**

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Run a model:**

```bash
ollama run llama3
```

---

#### 3️⃣ Tool 2 — Hugging Face

Hugging Face provides a hub of 100k+ open-source models plus the `transformers` Python library.

**Basic usage:**

```python
from transformers import pipeline

pipe = pipeline("text-generation", model="gpt2")
result = pipe("Explain DevOps in simple terms")
print(result)
```

---

### 🧪 Hands-On Tasks

#### 🛠️ Task 1 — Run a Local Model with Ollama

1. Install Ollama
2. Run `llama3`
3. Ask a DevOps-related question (pipeline, YAML, error explanation)

#### 🛠️ Task 2 — Try a Hugging Face Model

1. Run basic text generation locally using the `transformers` library
2. Test with at least two different DevOps prompts

**💬 Suggested prompts to test:**

```
Explain a CI/CD pipeline in simple terms
Write a GitLab pipeline for building a Docker image
Best practices for Kubernetes resource limits
Fix this error: permission denied while running docker
Generate a bash script to clean log files older than 7 days
```

---

### ✅ End-of-Day Checklist

- [ ] Install Ollama and successfully run `llama3`
- [ ] Ask at least 3 DevOps prompts to a local model
- [ ] Run a basic Hugging Face `text-generation` pipeline locally
- [ ] Understand the key trade-offs between local and cloud LLMs

---
---

## 📅 Day 9 — Ollama Hands-On

### 🎯 Goal for Day 9

Go deeper with Ollama — run models interactively, via CLI, via HTTP API, and understand how to integrate local AI into DevOps workflows.

---

### 🔧 Step-by-Step Guide

#### Step 1 — Install Ollama

```bash
# Linux / Mac
curl -fsSL https://ollama.com/install.sh | sh

# Verify installation
ollama --version
```

---

#### Step 2 — Pull a Model

```bash
ollama pull llama3
```

> This downloads the model locally — AI runs fully offline from this point.

---

#### Step 3 — Run Model Interactively

```bash
ollama run llama3
```

**Try these prompts inside the interactive session:**

```
Explain DevOps in simple terms
Write a Dockerfile for a Node.js app
Generate a CI/CD pipeline YAML for GitHub Actions
```

---

#### Step 4 — One-Shot CLI Prompt

```bash
ollama run llama3 "Write a Kubernetes deployment YAML"
```

---

#### Step 5 — Pipe Input from Script

```bash
echo "Generate Terraform config for an AWS EC2 instance" | ollama run llama3
```

---

#### Step 6 — Use the HTTP API

Ollama exposes a local REST API at `http://localhost:11434`.

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "llama3",
  "prompt": "Write a GitHub Actions workflow for CI",
  "stream": false
}'
```

> This is how you integrate local AI with CI/CD pipelines, automation scripts, and internal tools.

---

#### Step 7 — Compare Ollama vs ChatGPT

| Feature | Ollama (Local) | ChatGPT (Cloud) |
|---|---|---|
| Internet required | ❌ Fully offline | ✅ Online |
| Data privacy | ✅ Stays local | ❌ Leaves your system |
| Response speed | ✅ Fast (no latency) | ✅ Fast API |
| Model capability | ⚠️ Smaller models | ✅ Stronger |
| Cost | ✅ Free | ❌ API usage cost |

---

### 🧠 Pro Tip — Try Multiple Models

```bash
ollama pull mistral
ollama run mistral
```

| Model | Characteristic |
|---|---|
| `llama3` | Better reasoning, slightly slower |
| `mistral` | Faster and lightweight |

---

### ✅ End-of-Day Checklist

- [ ] Run `llama3` locally and test 3+ DevOps prompts
- [ ] Use the one-shot CLI prompt to generate a Kubernetes YAML
- [ ] Call the Ollama HTTP API from the terminal
- [ ] Pull `mistral` and compare its output to `llama3`

---
---

## 📅 Day 10 — Ollama + Docker (Containerized AI)

### 🎯 Goal for Day 10

Run Ollama inside a Docker container and expose it as a portable, reproducible local AI API service.

---

### 🐳 Step-by-Step Guide

#### Step 1 — Pull the Ollama Docker Image

```bash
docker pull ollama/ollama
```

---

#### Step 2 — Run the Ollama Container

```bash
docker run -d \
  --name ollama \
  -p 11434:11434 \
  -v ollama_data:/root/.ollama \
  ollama/ollama
```

**What this does:**
- Runs Ollama as a background container
- Exposes the API on `localhost:11434`
- Persists downloaded models via a Docker volume

---

#### Step 3 — Download a Model Inside the Container

```bash
docker exec -it ollama ollama pull llama3
```

---

#### Step 4 — Test the Local API

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "llama3",
  "prompt": "Explain a CI/CD pipeline",
  "stream": false
}'
```

> ✅ A valid JSON response confirms your containerized AI is running correctly.

---

#### Step 5 — Interactive Mode (Optional)

```bash
docker exec -it ollama ollama run llama3
```

---

#### Step 6 — Use in a CI/CD Pipeline

**Example GitHub Actions step:**

```yaml
- name: Query Local AI
  run: |
    curl http://localhost:11434/api/generate -d '{
      "model": "llama3",
      "prompt": "Generate a Dockerfile for a Python app",
      "stream": false
    }'
```

---

#### Step 7 — Docker Compose Setup (Recommended for Teams)

**`docker-compose.yml`:**

```yaml
version: '3'
services:
  ollama:
    image: ollama/ollama
    container_name: ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    restart: unless-stopped

volumes:
  ollama_data:
```

**Start:**

```bash
docker-compose up -d
```

---

### 🏗️ Architecture Overview

```
┌──────────────────────────┐
│   DevOps Pipeline        │
│   (CI/CD / Scripts)      │
└──────────┬───────────────┘
           │  HTTP API (port 11434)
           ▼
┌──────────────────────────┐
│   Ollama Docker Container │
│   Local Model (Llama3)   │
└──────────────────────────┘
```

---

### ⚠️ Tips

- Allocate sufficient memory — models typically require 4–8 GB RAM
- Use a lighter model on constrained systems: `ollama pull mistral`
- Monitor container logs: `docker logs ollama`

---

### ✅ End-of-Day Checklist

- [ ] Run Ollama as a Docker container
- [ ] Successfully query the containerized AI via `curl`
- [ ] Set up the Docker Compose file and bring it up
- [ ] Understand how to integrate the API into a CI/CD step

---
---

## 📅 Day 11 — VS Code + GitHub Copilot

### 🎯 Goal for Day 11

Use GitHub Copilot inside VS Code to generate Kubernetes YAML, Dockerfiles, and CI/CD configs — and understand code you didn't write.

---

### ⚙️ Setup

1. Open VS Code
2. Go to Extensions (`Ctrl + Shift + X`)
3. Search and install: **GitHub Copilot** and **GitHub Copilot Chat**
4. Sign in with your GitHub account

---

### 🧪 Hands-On Tasks

#### 🛠️ Task 1 — Inline Suggestions

Start typing a YAML file and let Copilot complete it:

```yaml
apiVersion: apps/v1
kind: Deployment
```

> Copilot will auto-suggest `metadata`, `spec`, `containers`, and more. Accept with `Tab`.

---

#### 🛠️ Task 2 — Explain Code with Copilot Chat

Open Copilot Chat (`Ctrl + Alt + I`) and ask:

```
Explain this Kubernetes deployment YAML line by line.
```

Copilot will break down every field, including what happens if values are missing.

---

#### 🛠️ Task 3 — Comment-Driven YAML Generation

Type a plain-English comment and let Copilot write the YAML:

```yaml
# Create a Kubernetes deployment for nginx with 3 replicas
```

**✅ Copilot generates:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:latest
        ports:
        - containerPort: 80
```

---

#### 🛠️ Task 4 — Generate a Service YAML

```yaml
# Expose the nginx deployment as a NodePort service
```

**✅ Copilot generates:**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  type: NodePort
  selector:
    app: nginx
  ports:
  - port: 80
    targetPort: 80
    nodePort: 30007
```

---

#### 🛠️ Task 5 — Refactor with Copilot

Highlight any YAML block → Right-click → **"Ask Copilot"**

**Try these:**

```
Convert this to ClusterIP
Add resource limits and requests
Make this production-ready
Add liveness and readiness probes
Use a rolling update strategy
```

---

### 🔥 Recommended DevOps Workflow

Instead of writing configs from scratch:

1. Write a descriptive comment:
   ```yaml
   # Kubernetes deployment for a Node.js app with 2 replicas, env variables, and resource limits
   ```
2. Let Copilot generate the full manifest
3. **Always validate before applying:**
   ```bash
   kubectl apply --dry-run=client -f file.yaml
   ```

---

### ⚖️ Copilot vs Manual Writing

| Factor | Copilot | Manual |
|---|---|---|
| Speed | ✅ Fast | ❌ Slow |
| Accuracy | ⚠️ Always review | ✅ Full control |
| Learning value | ✅ High | ✅ High |
| Boilerplate | ✅ Auto-generated | ❌ Written by hand |

> ⚠️ **Important:** Copilot can suggest incorrect configs or miss security best practices. Always review before production use.

---

### ✅ End-of-Day Checklist

- [ ] Install GitHub Copilot and Copilot Chat in VS Code
- [ ] Generate a Kubernetes Deployment YAML using inline comments
- [ ] Generate a Service YAML from a comment prompt
- [ ] Use Copilot Chat to explain an existing YAML file
- [ ] Validate a Copilot-generated manifest with `kubectl --dry-run`

---
---

## 📅 Day 12 — Hugging Face Models Deep Dive

### 🎯 Goal for Day 12

Understand Hugging Face model types, choose the right model for DevOps tasks, and run models locally.

---

### 🧠 Learn

#### 1️⃣ What Is Hugging Face?

Hugging Face is a platform for pretrained AI models, datasets, and ML tooling.

- Model hub: [https://huggingface.co/models](https://huggingface.co/models)
- 100k+ open-source models available
- Python `transformers` library for local usage

---

#### 2️⃣ Model Types

**🔹 Base Models**
- Raw pretrained LLMs, not optimized for following instructions
- Best for custom ML training and fine-tuning
- Examples: `bert`, `gpt2`

**🔹 Instruction Models**
- Fine-tuned to follow task-style prompts directly
- Best for DevOps automation (YAML, scripts, configs)
- Examples: `mistral-instruct`, `llama3-instruct`

**🔹 Chat Models**
- Designed for multi-turn conversation with context retention
- Best for interactive assistants and chatbots
- Examples: `llama3-chat`, `zephyr`

**⚖️ Quick Comparison:**

| Type | Best For | Example Use |
|---|---|---|
| Base | ML training / fine-tuning | Build your own model |
| Instruction | Tasks and automation | YAML generation, scripts |
| Chat | Conversational workflows | Internal chatbots |

---

#### 3️⃣ Running Models Locally

**Option 1 — Basic `transformers` pipeline:**

```bash
pip install transformers torch
```

```python
from transformers import pipeline

generator = pipeline("text-generation", model="gpt2")
print(generator("Explain Kubernetes", max_length=50))
```

**Option 2 — Instruction model:**

```python
from transformers import pipeline

pipe = pipeline("text-generation", model="mistralai/Mistral-7B-Instruct")
print(pipe("Write a Dockerfile for a Python Flask app"))
```

**Option 3 — Lightweight (recommended for DevOps):**

```bash
ollama run mistral
```

> For most DevOps tasks, Ollama with a quantized model is faster and simpler than raw `transformers`.

---

#### 4️⃣ Model Selection Strategy

**By task type:**

| Task | Model Type |
|---|---|
| YAML / Infra generation | Instruction model |
| Chat UI or assistant | Chat model |
| Custom ML pipeline | Base model |

**By available RAM:**

| RAM | Suitable Model Size |
|---|---|
| 8 GB | 3B – 7B parameters |
| 16 GB | 7B – 13B parameters |
| 32 GB+ | 13B+ parameters |

**Popular models to try:**

| Category | Models |
|---|---|
| Lightweight | `phi-2`, `mistral-7b` |
| Balanced | `llama3-8b` |
| Advanced | `mixtral`, `llama3-70b` |

---

### ✅ End-of-Day Checklist

- [ ] Navigate Hugging Face and find 3 DevOps-relevant models
- [ ] Run a basic `text-generation` pipeline locally
- [ ] Understand the difference between base, instruction, and chat models
- [ ] Select an appropriate model for a given task and RAM budget

---
---

## 📅 Day 13 — Prompt Testing on Local Models

### 🎯 Goal for Day 13

Build systematic model evaluation skills by comparing outputs across multiple local LLMs using the same prompts.

---

### 🔧 Setup

Pull 2–3 local models to compare:

```bash
ollama run llama3
ollama run mistral
ollama run phi3
```

| Model | Characteristic |
|---|---|
| `llama3` | Strong reasoning, more detailed |
| `mistral` | Fast and efficient |
| `phi3` | Lightweight, good for edge/dev |

---

### 🧪 Evaluation Process

#### Step 1 — Use the Same Prompt Across All Models

```
Explain how CI/CD pipelines work in DevOps.
Include real-world examples and best practices.
```

---

#### Step 2 — Capture and Compare Outputs

| Criteria | Llama 3 | Mistral | Phi-3 |
|---|---|---|---|
| Accuracy | ✅ High | ✅ Medium | ⚠️ Basic |
| Depth | ✅ Detailed | ⚠️ Moderate | ❌ Shallow |
| Clarity | ✅ Clear | ✅ Clear | ✅ Simple |
| Real-world examples | ✅ Included | ⚠️ Generic | ❌ Few |
| Hallucination risk | Low | Medium | High |

---

#### Step 3 — Evaluate Key Dimensions

Assess each output across five dimensions:

1. **Instruction following** — Did the model address all parts of the prompt?
2. **Depth vs brevity** — Is the answer appropriately detailed, or too shallow/verbose?
3. **Factual accuracy** — Are DevOps concepts correctly described?
4. **Hallucinations** — Any fabricated tools, commands, or claims?
5. **Consistency** — Run the same prompt twice; does the output vary significantly?

---

#### Step 4 — Identify Limitations

| Model | Typical Limitation |
|---|---|
| `phi3` | Lacks depth, skips edge cases |
| `mistral` | Sometimes misses nuanced details |
| `llama3` | Slower, occasionally verbose |

---

#### Step 5 — Refine Your Prompt and Re-Test

**Improved prompt (v2):**

```
Explain CI/CD pipelines in DevOps with:
1. A clear definition
2. A step-by-step workflow
3. Real-world tools (e.g., Jenkins, GitHub Actions, GitLab CI)
4. Three concrete best practices

Keep the explanation structured and under 200 words.
```

Re-run across all models and compare whether the structured prompt improves output quality.

---

#### 🚀 Bonus — Edge-Case Prompts

Test how models behave under pressure:

```
# Ambiguous prompt
Explain pipelines.

# Complex reasoning
Design a CI/CD pipeline for a microservices architecture using Kubernetes.

# Debugging task
Why is my GitHub Actions pipeline failing with a permission denied error?
```

---

### ✅ End-of-Day Checklist

- [ ] Run the same prompt across `llama3`, `mistral`, and `phi3`
- [ ] Build a comparison table with accuracy, depth, and hallucination scores
- [ ] Identify one clear limitation per model
- [ ] Refine the prompt and re-run to measure improvement
- [ ] Test at least one edge-case or ambiguous prompt

---
---

## 📅 Day 14 — Mini Project: Local AI Log Analyzer

### 🎯 Goal for Day 14

Build a working AI-powered DevOps tool that reads a log file and returns an AI-generated issue summary using a local LLM — no API cost, no external services.

---

### 🏗️ Project Architecture

```
logs.txt  →  Python Script  →  Ollama (Local LLM)  →  Summary Output
```

---

### 📁 Project Structure

```
.
├── analyzer.py
├── logs.txt
├── requirements.txt
└── Dockerfile
```

---

### 🔧 Step-by-Step Build

#### Step 1 — Create Sample Logs (`logs.txt`)

```
2026-05-20 10:12:23 ERROR Failed to connect to database
2026-05-20 10:12:25 INFO  Retrying connection...
2026-05-20 10:12:30 ERROR Connection timeout
2026-05-20 10:13:00 WARN  High memory usage detected
2026-05-20 10:14:10 ERROR Service crashed unexpectedly
```

---

#### Step 2 — Design the Prompt

```
Analyze the following system logs and provide:
1. Key issues identified
2. Possible root causes
3. Recommended remediation actions

Logs:
{logs}
```

---

#### Step 3 — Python Script (`analyzer.py`)

```python
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

def read_logs(file_path):
    with open(file_path, "r") as f:
        return f.read()

def generate_summary(logs):
    prompt = f"""
Analyze the following logs and provide:
1. Key issues
2. Root causes
3. Fix suggestions

Logs:
{logs}
"""
    response = requests.post(OLLAMA_URL, json={
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    })
    return response.json()["response"]

if __name__ == "__main__":
    logs = read_logs("logs.txt")
    summary = generate_summary(logs)
    print("\n===== AI LOG SUMMARY =====\n")
    print(summary)
```

---

#### Step 4 — Run Locally

Start Ollama:

```bash
ollama run llama3
```

Run the analyzer:

```bash
python analyzer.py
```

**✅ Expected Output:**

```
Key Issues:
- Database connection failure
- Service crash
- High memory usage

Root Causes:
- Database unreachable or misconfigured
- Resource exhaustion leading to crash
- Timeout values too low

Recommended Actions:
- Verify DB credentials and network connectivity
- Increase connection timeout limits
- Set up memory usage alerting
```

---

### 📦 Dockerize the Project

**`requirements.txt`:**

```
requests
```

**`Dockerfile`:**

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "analyzer.py"]
```

**Build and run:**

```bash
docker build -t log-analyzer .
docker run --network=host log-analyzer
```

> `--network=host` allows the container to reach Ollama running on the host machine.

---

### 💡 Improvements to Level Up

**1. Add CLI input:**

```bash
python analyzer.py logs.txt
```

**2. Multi-model comparison — run against `llama3`, `mistral`, and `phi3` and compare summaries**

**3. Force structured JSON output — update the prompt:**

```
Return output in this JSON format only:
{
  "issues": [],
  "root_causes": [],
  "actions": []
}
```

**4. Streamlit dashboard (optional)** — upload logs, display AI analysis, visualize severity

**5. CI/CD integration** — run the analyzer automatically on pipeline failure logs and alert on critical findings

---

### ✅ End-of-Day Checklist

- [ ] Create `logs.txt` with sample log entries
- [ ] Write and run `analyzer.py` successfully against a local Ollama model
- [ ] Verify the AI-generated summary is accurate and structured
- [ ] Dockerize the project and run it as a container
- [ ] Try at least one improvement: JSON output, CLI args, or multi-model comparison

---
