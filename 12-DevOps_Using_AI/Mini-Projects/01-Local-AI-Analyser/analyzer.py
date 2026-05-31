import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:1b"

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
