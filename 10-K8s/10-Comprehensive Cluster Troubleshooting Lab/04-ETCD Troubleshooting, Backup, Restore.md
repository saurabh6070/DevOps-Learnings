# 🗄️ ETCD: Administration, Backup & Restore
### *The backbone of CKA cluster recovery exams*

---

## 📖 1. What is ETCD?

ETCD is a **consistent, distributed key-value store** used by Kubernetes to store **all cluster data** — nodes, pods, configs, secrets, roles, and more. It is the single source of truth for the cluster state.

- ETCD is deployed on **all Control Plane (Master) Nodes**.
- Default data storage path: `/var/lib/etcd/` (can be verified by describing the etcd pod).
- Kubernetes communicates with etcd through the **kube-apiserver** — no other component talks to etcd directly.

---

## 🔧 2. Installing `etcdctl`

`etcdctl` is the command-line client used to interact with etcd (backup, restore, get/put keys, etc.).

```bash
apt-get install etcd-client
```

> ⚠️ Always set `ETCDCTL_API=3` before using etcdctl — Kubernetes uses etcd v3, and many commands behave differently (or don't work at all) under the default v2 API.

```bash
export ETCDCTL_API=3
```

---

## 🔐 3. Checking Secrets Stored in ETCD

You can query etcd directly to inspect how Kubernetes objects (like Secrets) are stored.

```bash
ETCDCTL_API=3 etcdctl \
  --cacert=/etc/kubernetes/pki/etcd/ca.cert \
  --cert=/etc/kubernetes/pki/etcd/server.cert \
  --key=/etc/kubernetes/pki/etcd/server.key \
  get /registry/secrets/default/my-secret
```

To view the raw byte-level content:

```bash
ETCDCTL_API=3 etcdctl \
  --cacert=/etc/kubernetes/pki/etcd/ca.cert \
  --cert=/etc/kubernetes/pki/etcd/server.cert \
  --key=/etc/kubernetes/pki/etcd/server.key \
  get /registry/secrets/default/my-secret | hexdump -C
```

**🔎 Key Observation:** Even though the output looks jumbled (base64/binary), the *decoded* secret value is visible in plain text within it.

> **📌 This proves:** By default, data in etcd is stored in **decoded (unencrypted) format** — i.e., there is **no encryption at rest** unless explicitly configured.

### Checking if Encryption-at-Rest is Enabled

```bash
ps -aux | grep kube-api | grep "encryption-provider-config"
# OR
cat /etc/kubernetes/manifests/kube-apiserver.yaml | grep "encryption-provider-config"
```

- **Blank output** → encryption at rest is **NOT configured** on the API server.
- If a flag is present, it points to an `EncryptionConfiguration` file defining how secrets are encrypted before being written to etcd.

### Re-encrypting/Recreating Existing Secrets

If encryption-at-rest is enabled *after* secrets already exist, force them to be rewritten (and thus encrypted) using:

```bash
kubectl get secrets --all-namespaces -o json | kubectl replace -f -
```

---

## 💾 4. Backing Up the ETCD Cluster

### Step 1 — Find the Certificates & Endpoint

Describe the etcd pod to extract the required TLS paths:

```bash
kubectl describe pod etcd-controlplane -n kube-system | grep -i crt
kubectl describe pod etcd-controlplane -n kube-system | grep -i key
kubectl describe pod etcd-controlplane -n kube-system | grep -i url
```

Typical output paths:

| Flag | Path |
|------|------|
| `--cert-file` | `/etc/kubernetes/pki/etcd/server.crt` |
| `--key-file` | `/etc/kubernetes/pki/etcd/server.key` |
| `--trusted-ca-file` | `/etc/kubernetes/pki/etcd/ca.crt` |
| `--advertise-client-urls` | `https://<node-ip>:2379` |

### Step 2 — Take the Snapshot

```bash
ETCDCTL_API=3 etcdctl snapshot save snapshot.db \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/etcd/ca.crt \
  --cert=/etc/etcd/etcd-server.crt \
  --key=/etc/etcd/etcd-server.key
```

**Real exam-style example:**

```bash
ETCDCTL_API=3 etcdctl snapshot save /opt/snapshot-pre-boot.db \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key

# Output: Snapshot saved at /opt/snapshot-pre-boot.db
```

### Step 3 — Verify the Snapshot

```bash
ETCDCTL_API=3 etcdctl snapshot status snapshot.db \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/etcd/ca.crt \
  --cert=/etc/etcd/etcd-server.crt \
  --key=/etc/etcd/etcd-server.key

ls -lrth snapshot.db
```

---

## ♻️ 5. Restoring the ETCD Cluster from Backup

### Step 1 — Stop the API Server

```bash
service kube-apiserver stop
```

> The API server must be stopped because it's actively reading/writing to etcd — restoring while it's running can corrupt data.

### Step 2 — Restore the Snapshot to a New Data Directory

```bash
ETCDCTL_API=3 etcdctl snapshot restore snapshot.db \
  --data-dir /var/lib/etcd-from-backup/ \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/etcd/ca.crt \
  --cert=/etc/etcd/etcd-server.crt \
  --key=/etc/etcd/etcd-server.key
```

> 💡 **Best practice:** Always restore into a **new/different data directory** (never overwrite the live one directly) — this keeps the old data safe as a fallback.

### Step 3 — Point ETCD to the New Data Directory

Check the current path in the static pod manifest:

```bash
cat /etc/kubernetes/manifests/etcd.yaml | grep -i hostpath -A 1 | grep -i var
# path: /var/lib/etcd/
```

Edit the manifest:

```bash
vi /etc/kubernetes/manifests/etcd.yaml
```

Change the `hostPath` to the new restored directory:

```yaml
path: /var/lib/etcd-from-backup/
```

Verify the change:

```bash
cat /etc/kubernetes/manifests/etcd.yaml | grep -i hostpath -A 1 | grep -i var
# path: /var/lib/etcd-from-backup/
```

> **📌 Note:** Only the `hostPath` field needs to change. Updating the `volumeMounts` path too is optional (not required) since it maps to the same host path internally.

### Step 4 — Restart the ETCD Pod

Since etcd is a **static pod**, kubelet will automatically recreate it once the manifest changes (or you can force it):

```bash
kubectl delete pod -n kube-system etcd-controlplane
```

Monitor until it's back up:

```bash
watch "crictl ps | grep etcd"
```

> ⚙️ Expect `kube-scheduler` and `kube-controller-manager` to also restart automatically as part of this process.

### Step 5 — Reload & Restart Services

```bash
systemctl daemon-reload
service etcd restart
```

---

## 🧭 6. ETCDCTL Essentials

- `etcdctl` is the CLI client for etcd; in Kubernetes labs, etcd runs as a **static pod** on the control plane.
- Always export `ETCDCTL_API=3` before using it.
- Since our etcd is **TLS-enabled**, these flags are **mandatory**:

| Flag | Purpose |
|------|---------|
| `--cacert` | Verify the server's TLS certificate using this CA bundle |
| `--cert` | Client's TLS certificate for authentication |
| `--key` | Client's TLS private key |
| `--endpoints` | Defaults to `127.0.0.1:2379` (etcd on localhost) |

Get full help for any subcommand:

```bash
etcdctl snapshot save -h
etcdctl snapshot restore -h
```

### Basic Key-Value Operations

```bash
export ETCDCTL_API=3
etcdctl put name john
etcdctl get name
etcdctl get / --prefix --keys-only
```

### Finding the ETCD Data Directory

```bash
cat /etc/kubernetes/manifests/etcd.yaml | grep -i data-dir
```

---

## 🏗️ 7. Stacked vs External ETCD

| Type | Description |
|------|-------------|
| **Stacked (Internal) ETCD** | Runs as a pod on the same control plane node as the API server |
| **External ETCD** | Runs on separate, dedicated nodes outside the control plane |

### How to Identify Which Type is Used

1. SSH into the control plane node.
2. Check `kube-system` namespace for a pod named `etcd-*`:
   - **Found** → Stacked (Internal) etcd.
   - **Not found** → External etcd.

### Finding the ETCD Cluster IP

```bash
kubectl describe pod kube-apiserver-controlplane -n kube-system | grep -i "etcd-servers\|2379"
```

> The API server manifest contains the `--etcd-servers` flag pointing to the etcd cluster IP(s), since the API server is the only component that talks directly to etcd.

---

## 🌐 8. Working with an External ETCD Server

### Step 1 — SSH into the External ETCD Node

```bash
ssh 192.36.3.6
```

### Step 2 — Inspect the Running Process

```bash
ps -ef | grep -i etcd
```

Example output:

```
/usr/local/bin/etcd --name etcd-server \
  --data-dir=/var/lib/etcd-data \
  --cert-file=/etc/etcd/pki/etcd.pem \
  --key-file=/etc/etcd/pki/etcd-key.pem \
  --peer-cert-file=/etc/etcd/pki/etcd.pem \
  --peer-key-file=/etc/etcd/pki/etcd-key.pem \
  --trusted-ca-file=/etc/etcd/pki/ca.pem \
  --peer-trusted-ca-file=/etc/etcd/pki/ca.pem \
  --peer-client-cert-auth --client-cert-auth \
  --initial-advertise-peer-urls https://192.36.3.6:2380 \
  --listen-peer-urls https://192.36.3.6:2380 \
  --advertise-client-urls https://192.36.3.6:2379 \
  --listen-client-urls https://192.36.3.6:2379,https://127.0.0.1:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster etcd-server=https://192.36.3.6:2380 \
  --initial-cluster-state new
```

From this, you can extract the **data-dir**, **cert paths**, and **cluster URLs** directly.

### Step 3 — List Cluster Members

```bash
ETCDCTL_API=3 etcdctl --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/etcd/pki/ca.pem \
  --cert=/etc/etcd/pki/etcd.pem \
  --key=/etc/etcd/pki/etcd-key.pem \
  member list
```

Example output (single-node external cluster):

```
56a6cbd855a43a08, started, etcd-server, https://192.36.3.6:2380, https://192.36.3.6:2379, false
```

### Full Backup & Restore Walkthrough (External ETCD)

**Take the snapshot:**

```bash
ETCDCTL_API=3 etcdctl snapshot save snapshot.db \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/etcd/pki/ca.pem \
  --cert=/etc/etcd/pki/etcd.pem \
  --key=/etc/etcd/pki/etcd-key.pem
```

**Restore into a new data directory:**

```bash
ETCDCTL_API=3 etcdctl snapshot restore cluster2.db \
  --data-dir=/var/lib/etcd-data-new \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/etcd/pki/ca.pem \
  --cert=/etc/etcd/pki/etcd.pem \
  --key=/etc/etcd/pki/etcd-key.pem
```

**Fix ownership of the new directory:**

```bash
chown -R etcd:etcd /var/lib/etcd-data-new
```

**Update the systemd service to point at the new data-dir:**

```bash
vi /etc/systemd/system/etcd.service
# update --data-dir=/var/lib/etcd-data-new
```

**Reload and restart:**

```bash
systemctl daemon-reload
systemctl restart etcd
systemctl status etcd
```

Expected healthy output includes:

```
INFO: <member-id> became leader at term 2
setting up the initial cluster version to 3.4
ready to serve client requests
serving client requests on 192.36.3.6:2379
serving client requests on 127.0.0.1:2379
```

---

## 📈 9. Scaling ETCD for High Availability

In large clusters, etcd can be **moved off the control plane nodes entirely** and deployed on a **dedicated set of nodes** to provide better performance and high availability, independent of control plane resource usage.

---

## 🗳️ 10. How ETCD Handles Reads, Writes & Consensus

### Reads
A **read request** can be served by **any** etcd server directly, since etcd guarantees strong consistency across all members.

### Writes
A **write request** follows this flow:

1. Client sends write → forwarded to the **Leader** node.
2. Leader applies the change locally.
3. Leader replicates the change to all other etcd members.
4. Once the Leader receives acknowledgment (consent) from a **majority (quorum)** of members, the write is committed and considered successful.

### 🔢 Quorum Table

| Cluster Size | Quorum Needed |
|:---:|:---:|
| 1 | 1 |
| 2 | 2 |
| 3 | 2 |
| 4 | 3 |
| 5 | 3 |

> 💡 **Why odd numbers are preferred:** A 3-node cluster and a 4-node cluster both tolerate only 1 node failure, but the 4-node cluster requires more resources for the same fault tolerance — so clusters are typically sized as 3, 5, or 7 nodes.

### 🏆 Leader Election — RAFT Protocol

ETCD uses the **RAFT consensus algorithm** to elect a leader:

1. Every member waits a **random timeout** before initiating a leader-vote request.
2. The **first member** to finish its timeout sends vote requests to all other members.
3. Other members **cannot refuse** (deny) this vote request.
4. That member is **promoted to Leader**.
5. The Leader periodically sends heartbeats to inform other members it's still active and continuing as leader.

---

## ⚙️ 11. Manually Installing ETCD

```bash
wget -q --https-only "https://github.com/coreos/etcd/releases/download/v3.3.9/etcd-v3.3.9-linux-amd64.tar.gz"
tar -xvf etcd-v3.3.9-linux-amd64.tar.gz
mv etcd-v3.3.9-linux-amd64/etcd/* /usr/local/bin/
mkdir -p /etc/etcd/ /var/lib/etcd/
cp ca.pem kubernetes-key.pem kubernetes.pem /etc/etcd/
```

---

## ✅ 12. Full Backup & Restore Walkthrough (Stacked ETCD — CKA Exam Style)

**1. Check running pods:**

```bash
kubectl get pods -n kube-system
```

**2. Get certificate & key paths from the etcd pod:**

```bash
kubectl describe pod etcd-controlplane -n kube-system | grep -i crt
kubectl describe pod etcd-controlplane -n kube-system | grep -i key
kubectl describe pod etcd-controlplane -n kube-system | grep -i url
```

**3. Take the backup:**

```bash
ETCDCTL_API=3 etcdctl snapshot save /opt/snapshot-pre-boot.db \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key
```

**4. Confirm the snapshot file exists:**

```bash
ls -lrth /opt/snapshot-pre-boot.db
```

This exact flow — **describe pod → extract certs → snapshot save → verify** — is the pattern most CKA backup questions follow.

---

## 🧠 Quick Recap / Cheat Sheet

| Task | Command |
|------|---------|
| Set API version | `export ETCDCTL_API=3` |
| Take backup | `etcdctl snapshot save <file> --endpoints ... --cacert ... --cert ... --key ...` |
| Verify backup | `etcdctl snapshot status <file> ...` |
| Restore backup | `etcdctl snapshot restore <file> --data-dir <new-dir> ...` |
| Update manifest after restore | Edit `hostPath` in `/etc/kubernetes/manifests/etcd.yaml` |
| Check secrets encryption | `grep "encryption-provider-config"` in kube-apiserver manifest |
| List etcd members | `etcdctl member list` |
| Check stacked vs external | Look for `etcd-*` pod in `kube-system` |

### ⚠️ Common Exam Pitfalls
- Forgetting to set `ETCDCTL_API=3`.
- Restoring into the **same** data directory as the live cluster instead of a new one.
- Forgetting to stop the API server before restoring.
- Not updating the `hostPath` in the etcd static pod manifest after restore.
- Using the wrong cert/key paths (kube-apiserver certs vs etcd's own certs).
