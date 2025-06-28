# Miscelleneous

## ❌ 1. Docker `ps` Command Not Running

### 🔍 **Problem:**
When running `docker ps`, you get a **permission denied** error related to `/var/run/docker.sock`.

### 🖥️ **Explanation:**
- Docker communicates with its daemon via a Unix socket: `/var/run/docker.sock`.
- By default, this socket is owned by the `root` user and the `docker` group.
- If your user is **not in the `docker` group** or does not have the right permissions, you won't be able to interact with Docker.

### 📂 Also relevant:
- `/run/containerd/containerd.sock` is the default Unix socket for **containerd**, the container runtime used by Docker and Kubernetes.
- These `.sock` files act like APIs over Unix sockets.

---

### 🧪 **Example Output:**

```bash
ubuntu@ip-172-31-23-34:~$ docker -v
Docker version 24.0.7, build 24.0.7-0ubuntu4.1

ubuntu@ip-172-31-23-34:~$ docker ps
permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock:
Get "http://%2Fvar%2Frun%2Fdocker.sock/v1.24/containers/json": dial unix /var/run/docker.sock: connect: permission denied

ubuntu@ip-172-31-23-34:/home/ubuntu# ps aux | grep -i docker
root     1722  0.1  8.4 1929248 82564 ? Ssl  07:20  0:02 /usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock
```

🧾 Check Docker Socket File:
```bash
ls -lrth /var/run/docker.sock
Output:
srw-rw---- 1 root docker 0 Sep  7 07:20 /var/run/docker.sock
```
This means the socket belongs to root and the docker group.

✅ Solution:
Use chown to assign ownership of the socket to your current user (in this case, ubuntu):
sudo chown ubuntu:ubuntu /var/run/docker.sock

🟢 Verify:
```bash
docker ps
Output:
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```
✅ Success! You now have permission to interact with Docker.

💡 Alternative (Best Practice): Instead of changing socket ownership manually every time, add your user to the docker group:

```bash
sudo usermod -aG docker $USER
newgrp docker   # or log out and log back in
```


## 2. 📁 More Info on `/run/containerd/containerd.sock`

When troubleshooting issues with **containerd** or attempting to connect to it via its Unix socket, here are some key steps to follow:

### ✅ What to Check:

- 🔐 **Permissions**  
  Ensure the user or process has access to the socket file.

  ```bash
  ls -l /run/containerd/containerd.sock
  ```
  
🟢 Containerd Status
Make sure the containerd service is active and running.

```bash
systemctl status containerd
```

📡 Socket Availability
Check if the socket file exists and is in use.

```bash
ss -x | grep containerd.sock
```

🧾 Logs
View containerd logs for any runtime issues.

```bash
journalctl -u containerd
```

## 📊 3. More Info on the ss Command (Advanced Version of netstat)
The ss (socket statistics) command is a powerful tool for viewing network connections and socket information. It is a modern replacement for netstat, offering faster performance and better filtering.

🔍 Key Benefits:
⚡ Faster than netstat (direct kernel access)

🧠 Supports advanced filtering

🛠️ Preferred for modern Linux systems

🔗 Common ss Usage Examples
List Active TCP Connections

```bash
ss -t
```

List Active UDP Connections

```bash
ss -u
```

Show Listening Ports (TCP & UDP)

```bash
ss -l
```

Detailed View (TCP, UDP, Listening)

```bash
ss -tuln
```

Filter by Destination Address

```bash
ss dst 192.168.1.1
```

Filter by Source Port

```bash
ss sport = :80
```

Show Active Unix Sockets

```bash
ss -x
```

📎 Useful for checking sockets like /run/containerd/containerd.sock.

Display Socket Statistics

```bash
ss -s
```

📈 Shows summary of TCP, UDP, and other active socket types.

