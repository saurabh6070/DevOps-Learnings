## 1. ✅ Default Bridge Network (`docker0`)

Docker creates the `docker0` bridge network automatically during installation. It connects containers on the **same host** and routes their traffic to the internet via NAT.

### 🔄 Communication Flows

- **Container to Internet:**

Container A → docker0 → eth0 → Internet

- **Container A to Container B (same bridge):**

Container A → docker0 → Container B

### 🔍 Commands

```bash
ip addr show                        # Check docker0 (e.g., 172.17.0.1)
docker network ls                  # Shows default networks
docker inspect bridge | grep Subnet
```

🚀 Running Containers on Default Bridge

```bash
docker run -td --name contA alpine
docker run -td --name contB alpine

docker attach contA  # Check IP: likely 172.17.0.2
# Detach: Ctrl + P + Q

docker attach contB  # Check IP: likely 172.17.0.3
❌ ping contB from contA fails – DNS is not supported on default bridge.
```

## 2. ✅ User-Defined Bridge Network
Custom bridge networks enable DNS support and better isolation between containers.

🛠️ Create and Inspect Custom Bridge

```bash
# Example commands to create and inspect a custom bridge network
docker network create my-bridge
docker network inspect my-bridge
```
