# Kubernetes Jobs & CronJobs

## 🎯 1. Why Jobs? (Usage & Use-Cases)

Deployments, ReplicaSets, and DaemonSets are all designed to run Pods that stay **alive forever** — if a Pod dies, it's recreated, because the workload is expected to run continuously (e.g., a web server).

But many real-world tasks are meant to **run once (or a fixed number of times) and then finish** — not run forever. For example:

- Running a batch data-processing script
- Performing a database migration
- Generating a report
- Sending a one-time notification/email
- Running a backup task
- Rendering a video or processing a file

For workloads like these, Kubernetes provides the **Job** object.

**Key idea:** A Job creates one or more Pods and ensures that a specified number of them **successfully terminate**. When the required number of completions is reached, the Job itself is considered **complete** — the Pods are not restarted after that.

---

## 📦 2. Jobs

### 2.1 What is a Job?

A **Job** is a Kubernetes controller that:
- Creates one or more Pods to run a task
- Retries the Pod if it fails (based on `restartPolicy` and `backoffLimit`)
- Tracks successful completions
- Stops creating new Pods once the desired number of successful completions is reached

Unlike a Deployment, a Job's Pods use:

```yaml
spec:
  template:
    spec:
      restartPolicy: Never   # or OnFailure — NOT "Always"
```

> ⚠️ A Job's Pod template **cannot** use `restartPolicy: Always`, since that would mean the Pod never finishes.

---

### 2.2 Basic Job Example

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: math-job
spec:
  template:
    spec:
      containers:
      - name: math
        image: ubuntu
        command: ["expr", "3", "+", "2"]
      restartPolicy: Never
  backoffLimit: 4
```

```bash
kubectl apply -f math-job.yaml
kubectl get jobs
kubectl get pods                     # Pods created by the Job
kubectl logs <pod-name>              # Output of the completed task
```

---

### 2.3 Key Job Spec Fields

| Field | Purpose |
|---|---|
| `completions` | Total number of Pods that must **successfully** complete for the Job to be done |
| `parallelism` | Number of Pods that can run **at the same time** |
| `backoffLimit` | Number of retries before marking the Job as **failed** (default: 6) |
| `activeDeadlineSeconds` | Max time the Job is allowed to run before being terminated |
| `ttlSecondsAfterFinished` | Automatically clean up (delete) the Job N seconds after it finishes |
| `restartPolicy` | Must be `Never` or `OnFailure` (not `Always`) |

---

### 2.4 Running Multiple Pods — Completions & Parallelism

**Sequential (one at a time) — run 5 completions, one Pod at a time:**

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: sequential-job
spec:
  completions: 5
  template:
    spec:
      containers:
      - name: worker
        image: ubuntu
        command: ["echo", "processing item"]
      restartPolicy: Never
```

**Parallel — run 5 completions, 2 Pods running at a time:**

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: parallel-job
spec:
  completions: 5
  parallelism: 2
  template:
    spec:
      containers:
      - name: worker
        image: ubuntu
        command: ["echo", "processing item"]
      restartPolicy: Never
```

---

### 2.5 Job Failure Handling

- If a Pod fails and `restartPolicy: OnFailure` is set, the **same Pod** is restarted in place.
- If `restartPolicy: Never` is set, a **new Pod** is created to replace the failed one.
- The Job keeps retrying until either:
  - It reaches the required number of successful `completions`, **or**
  - It hits the `backoffLimit`, after which the Job is marked as **Failed**

```bash
kubectl describe job <job-name>     # See failure events, retries, backoff status
```

---

### 2.6 Useful Job Commands

```bash
kubectl create job my-job --image=busybox -- echo "hello"   # Imperative job creation
kubectl get jobs                                            # List all jobs
kubectl describe job my-job                                 # Detailed job status
kubectl delete job my-job                                   # Delete job (and its Pods)
kubectl logs job/my-job                                     # View logs of a job's pod
```

---

## ⏰ 3. CronJobs

### 3.1 What is a CronJob?

A **CronJob** creates **Jobs on a repeating schedule**, written in standard cron syntax. It's used for recurring, scheduled tasks such as:

- Nightly database backups
- Periodic report generation
- Sending scheduled emails/reports
- Cleaning up old data/logs on a schedule
- Periodic health checks or sync tasks

**Relationship:** `CronJob` → creates → `Job` → creates → `Pod(s)`

---

### 3.2 Basic CronJob Example

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: backup-cronjob
spec:
  schedule: "0 2 * * *"          # Every day at 2:00 AM
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: my-backup-tool
            command: ["/bin/sh", "-c", "run-backup.sh"]
          restartPolicy: OnFailure
```

```bash
kubectl apply -f backup-cronjob.yaml
kubectl get cronjobs
kubectl get jobs                       # Jobs created by the CronJob over time
kubectl get pods
```

---

### 3.3 Cron Schedule Syntax

```
┌───────────── minute (0 - 59)
│ ┌───────────── hour (0 - 23)
│ │ ┌───────────── day of month (1 - 31)
│ │ │ ┌───────────── month (1 - 12)
│ │ │ │ ┌───────────── day of week (0 - 6) (Sunday=0)
│ │ │ │ │
* * * * *
```

| Schedule | Meaning |
|---|---|
| `* * * * *` | Every minute |
| `*/5 * * * *` | Every 5 minutes |
| `0 * * * *` | Every hour, on the hour |
| `0 2 * * *` | Every day at 2:00 AM |
| `0 0 * * 0` | Every Sunday at midnight |
| `0 9 1 * *` | 9:00 AM on the 1st of every month |

---

### 3.4 Key CronJob Spec Fields

| Field | Purpose |
|---|---|
| `schedule` | Cron expression defining when the Job runs |
| `jobTemplate` | The Job spec to run on each schedule trigger |
| `concurrencyPolicy` | Controls overlapping runs: `Allow`, `Forbid`, or `Replace` |
| `startingDeadlineSeconds` | Deadline (in seconds) to start the Job if it missed its scheduled time |
| `successfulJobsHistoryLimit` | Number of completed Jobs to keep (default: 3) |
| `failedJobsHistoryLimit` | Number of failed Jobs to keep (default: 1) |
| `suspend` | If `true`, pauses future scheduled runs without deleting the CronJob |

**Concurrency Policy behavior:**

| Value | Behavior |
|---|---|
| `Allow` (default) | Multiple Jobs can run concurrently if a previous one hasn't finished |
| `Forbid` | Skips a new run if the previous Job is still running |
| `Replace` | Cancels the currently running Job and replaces it with the new one |

```yaml
spec:
  schedule: "*/10 * * * *"
  concurrencyPolicy: Forbid
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 1
```

---

### 3.5 Useful CronJob Commands

```bash
kubectl create cronjob my-cronjob --image=busybox --schedule="*/1 * * * *" -- echo "hello"

kubectl get cronjobs                        # List all cronjobs
kubectl describe cronjob my-cronjob          # Detailed status + schedule info
kubectl get jobs --watch                     # Watch jobs get created over time

# Manually trigger a run right now (creates a one-off Job from the CronJob's template)
kubectl create job manual-run --from=cronjob/my-cronjob

# Pause / resume a CronJob
kubectl patch cronjob my-cronjob -p '{"spec":{"suspend":true}}'
kubectl patch cronjob my-cronjob -p '{"spec":{"suspend":false}}'

kubectl delete cronjob my-cronjob            # Delete cronjob (and its jobs/pods)
```

---

## 🧾 4. Summary

| Object | Purpose | Runs Until |
|---|---|---|
| **Job** | Run a task once (or a fixed number of times) to completion | Required number of successful completions is reached |
| **CronJob** | Run a Job repeatedly on a schedule | Runs indefinitely, creating a new Job on each scheduled trigger (until suspended/deleted) |

**When to use which:**
- Use a **Job** for one-off or batch tasks that need to run to completion.
- Use a **CronJob** for recurring tasks that need to happen on a fixed schedule.
