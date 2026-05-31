# 🔍 AI Log Analyzer

A lightweight DevOps tool that reads application logs and generates an AI-powered summary — including key issues, root causes, and fix suggestions — using a local LLM via Ollama. No API keys, no cloud, no cost.

---

## 📁 Project Structure

```
Logs_Analyser/
├── analyzer.py        # Main script — reads logs and calls local AI
├── logs.txt           # Input log file
├── requirements.txt   # Python dependencies
└── Dockerfile         # Container build definition
```

---

## ⚙️ Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed
- [Ollama](https://ollama.com) installed and running on the host
- Model pulled locally:

```bash

## Install Docker
curl -fsSL https://get.docker.com | sh
sudo systemctl start docker
sudo systemctl status docker

## Install Ollama
curl -fsSL https://ollama.com/install.sh | sh
ollama --version
ollama pull llama3.2:1b
ollama run llama3.2:1b

## Install Net-tools
apt install net-tools
netstat -anp | grep 11434

## Install Python3
sudo apt update
sudo apt install python3
python3 --version

python3 analyzer.py

```

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/your-username/Logs_Analyser.git
cd Logs_Analyser
```

### 2. Start Ollama on the host

```bash
ollama serve &
```

Verify it's running:

```bash
curl http://localhost:11434
# Expected: Ollama is running
```

### 3. Add your logs

Edit `logs.txt` with your application logs, or use the sample provided:

```
2026-05-20 10:12:23 ERROR Failed to connect to database
2026-05-20 10:12:25 INFO  Retrying connection...
2026-05-20 10:12:30 ERROR Connection timeout
2026-05-20 10:13:00 WARN  High memory usage detected
2026-05-20 10:14:10 ERROR Service crashed unexpectedly
```

### 4. Build the Docker image

```bash
docker build -t log-analyzer .
```

### 5. Run the analyzer

```bash
docker run --network=host log-analyzer
```

> `--network=host` allows the container to reach Ollama running on the host at `localhost:11434`.

---

## 🖥️ Run Without Docker

```bash
pip install -r requirements.txt
python analyzer.py
```

---

## 📤 Sample Output

```
===== AI LOG SUMMARY =====

Key Issues:
- Database connection failure
- Service crash
- High memory usage

Root Causes:
- Database unreachable or misconfigured
- Resource exhaustion leading to crash
- Connection timeout values too low

Fix Suggestions:
- Verify database credentials and network connectivity
- Increase connection timeout limits
- Set up memory usage alerting and resource limits
```

---

## 🛠️ Configuration

| Variable | File | Default | Description |
|---|---|---|---|
| `OLLAMA_URL` | `analyzer.py` | `http://localhost:11434/api/generate` | Ollama API endpoint |
| `MODEL` | `analyzer.py` | `llama3.2:1b` | Local model to use |
| Log file path | `analyzer.py` | `logs.txt` | Input log file |

To switch models, update `MODEL` in `analyzer.py`:

```python
MODEL = "mistral"   # or llama3, phi3, etc.
```

---

## 🔧 Troubleshooting

**`Connection refused` on port 11434**
Ollama is not running. Start it with:
```bash
ollama serve &
```

**Model not found error**
Pull the model first:
```bash
ollama pull llama3.2:1b
```

**Container can't reach Ollama**
Ensure you're using `--network=host` when running the container.

---

## 📌 Tech Stack

- **Python 3.10**
- **Ollama** — local LLM runtime
- **llama3.2:1b** — lightweight local model
- **Docker** — containerized deployment

---
