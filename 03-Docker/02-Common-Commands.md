## 🐳 Common Docker and Linux Commands

### 📦 1. Docker Container Commands

```bash
docker ps
docker run -d nginx
docker ps      # 📝 Shows running Docker containers (processes)
```
<br>

### 🧠 2. Linux Process Commands

```bash
ps -aux
ps -aux | grep -i nginx
kill -9 <pid>  # 🔒 Terminate a process (requires root)
```

Then check:

```bash
docker ps      # ❌ The container is gone now.
```

✅ This proves that containers are OS-level processes,
but they behave like lightweight VMs or standalone environments.

<br>


### 🛠️ 3. Additional Docker Commands


```bash
docker ps -a                   # 📋 List all containers (including stopped)
docker stop <psId>            # 🛑 Stop a container
docker ps
docker ps -a
docker images                 # 🖼️ List all Docker images
docker rm <psId>              # 🗑️ Remove a container
docker ps -a
docker rmi <imgId>            # 🧼 Remove an image
```

<br>


### 🔁 4. Container Lifecycle Commands


```bash
docker run -d nginx           # 🚀 Start new nginx container (detached)
docker ps
docker kill <psId>           # ❌ Force stop container
docker ps -a
docker start <psId>          # 🔄 Restart a stopped container
docker ps
docker exec -it <psId> bash  # 🧭 Enter container shell (exit: Ctrl+p+q)
```

<br>


### 🧹 5. System Cleanup


```bash
docker system prune --all     # 🧼 Clean up unused containers, images, volumes
```

<br>


### 🏗️ 6. Docker Image Build Process


```bash
docker build -t hpsaurabh2022/samplewebimage .
```

🧱 Docker builds an image by creating temporary containers at each step in the Dockerfile.
You may see multiple image IDs during the build process.

<br>


### 📂 7. Docker Volumes


```bash
docker volume ls                      # 📋 List volumes
docker volume create myvol           # ➕ Create named volume
docker run -d --name conZ -v myvol:/app nginx
docker attach conZ                   # 🔌 Attach to container
# Inside container:
df -kh                               # 💽 Show disk space
```

<br>


🧼 8. Clean-Up Commands


```bash
docker ps
docker kill conZ
docker rm conZ
docker volume inspect myvol          # 🔍 Inspect volume details
```
<br>

