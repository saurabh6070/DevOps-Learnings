# 📂 Externalizing Log File from Docker Container

## 🔍 Problem

The log file is currently baked into the Docker image via `COPY . .` in the Dockerfile. This means every time the log file changes, the image has to be rebuilt — which is not practical for a real log analyzer.

## ✅ Solution

Store the log file on the Docker host and mount it into the container at runtime using a **Docker volume bind mount**. The image stays unchanged; only the mounted file changes.

---

## 🛠️ Steps

### Step 1 — Update the Dockerfile

Remove `COPY . .` and only copy the application code — not the log file:

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY analyzer.py .
CMD ["python", "analyzer.py"]
```

---

### Step 2 — Rebuild the Image

```bash
docker build -t log-analyzer .
```

---

### Step 3 — Run with the Log File Mounted from Host

```bash
docker run --network=host \
  -v /home/ubuntu/Logs_Analyser/logs.txt:/app/logs.txt \
  log-analyzer
```

> `-v host_path:container_path` — the container reads `logs.txt` from your host directory at runtime, not from inside the image.

---

## 🔄 How to Use Going Forward

The image stays the same — just swap in any log file from the host:

```bash
docker run --network=host \
  -v /var/log/syslog:/app/logs.txt \
  log-analyzer
```

```bash
docker run --network=host \
  -v /home/ubuntu/app/production.log:/app/logs.txt \
  log-analyzer
```

---

## 📊 Before vs After

| | Before | After |
|---|---|---|
| Log file location | Baked into Docker image | Lives on Docker host |
| To change log file | Rebuild the image | Just change the `-v` path |
| Image size | Larger (includes logs) | Smaller (app code only) |
| Flexibility | ❌ Low | ✅ High |
