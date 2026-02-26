# 🤖 Ansible Interview Questions & Answers

> 💼 A comprehensive collection of Ansible interview questions — from beginner to advanced — covering architecture, playbooks, vault, roles, CI/CD, and real-world scenarios asked in top tech interviews in 2025.

---

## 📌 Table of Contents

| Level | Topics |
|-------|--------|
| 🟢 [Beginner](#-beginner-questions) | Q1–Q12: Basics, architecture, SSH, inventory |
| 🟡 [Intermediate](#-intermediate-questions) | Q13–Q25: Playbooks, variables, roles, vault, handlers |
| 🔴 [Advanced](#-advanced-questions) | Q26–Q38: Dynamic inventory, error handling, performance, CI/CD |
| 🏢 [Scenario-Based](#-scenario-based-questions) | Q39–Q48: Real-world "what would you do" questions |

---

## 🟢 Beginner Questions

---

### Q1. 🤖 What is Ansible? What are its key features?

**Ans:**
**Ansible** is an open-source, agentless IT automation and configuration management tool developed by **Red Hat**. It automates provisioning, configuration management, application deployment, and orchestration.

**Key Features:**

| Feature | Description |
|---------|-------------|
| 🚫 **Agentless** | No software installed on managed nodes — uses SSH/WinRM |
| 📤 **Push-Based** | Master pushes configuration to slaves (not pull-based like Chef/Puppet) |
| 🔁 **Idempotent** | Running same playbook multiple times gives same result — no side effects |
| 📝 **YAML-Based** | Human-readable, easy to write and understand |
| 🐍 **Python-Powered** | Built on Python; all modules are Python scripts |
| 📡 **SSH for Linux** | Uses SSH (port 22) to connect to Linux nodes |
| 🪟 **WinRM for Windows** | Uses WinRM to connect to Windows managed nodes |
| 📈 **Scalable** | Single master can manage thousands of nodes |

---

### Q2. 🏗️ What are the core components of Ansible?

**Ans:**

| Component | Description |
|-----------|-------------|
| 🖥️ **Control Node** | The machine where Ansible is installed and playbooks are run. Must be Linux/macOS. |
| 🧩 **Managed Nodes** | Target machines (slaves). Only need Python + SSH. No Ansible installation needed. |
| 📂 **Inventory** | File listing all managed nodes (IPs/hostnames), organized in groups |
| 📜 **Playbooks** | YAML files containing multiple plays, each with a set of tasks |
| 📦 **Modules** | Python scripts on the master node that perform specific tasks (e.g., `apt`, `service`, `copy`) |
| 🔌 **Plugins** | Extend Ansible functionality — used mainly for **logging, callbacks, inventory, connection** |
| 🎭 **Roles** | Reusable, structured units of automation with tasks, templates, variables, and handlers |
| 🔐 **Vault** | Encryption tool to protect sensitive data like passwords and API keys |

> 📝 **Plugins vs Modules:**
> - **Modules** = Do the actual work (install packages, manage files, restart services)
> - **Plugins** = Extend how Ansible itself works (how it logs, connects, filters data)

> 📝 **copy vs synchronize (recursive):**
> - `copy` — copies files from master to slave
> - `synchronize` — uses rsync for recursive/large directory sync

---

### Q3. 🔄 What is the difference between Push-Based and Pull-Based architecture?

**Ans:**

| | Push-Based (Ansible) | Pull-Based (Chef/Puppet) |
|--|---------------------|------------------------|
| **Direction** | Master pushes config TO slaves | Slaves pull config FROM master |
| **Agent required?** | ❌ No agent | ✅ Agent installed on each node |
| **Trigger** | Initiated by master | Initiated by agent on slave |
| **Real-time control** | ✅ Immediate | ⏱️ Delayed (poll interval) |
| **Overhead** | Low | Higher (agent process always running) |
| **Examples** | Ansible | Chef, Puppet, CFEngine |

---

### Q4. 🐧 Can Windows be used as an Ansible Control Node?

**Ans:**
**No.** The Ansible Control Node (Master) **must be a Linux or macOS machine**. Windows is **not supported** as a control node.

However, Windows users can:
- Use **WSL (Windows Subsystem for Linux)** to run Ansible
- Use a **Linux VM** on Windows
- Use **Docker** with a Linux container

```bash
# On WSL (Ubuntu):
sudo apt update && sudo apt install ansible -y
ansible --version
```

---

### Q5. 🪟 Can Windows be a Managed Node? How does Ansible connect to it?

**Ans:**
**Yes.** Windows machines **can be managed nodes (slaves)**, but Ansible uses a different protocol to connect to them.

| OS | Protocol | Port |
|----|---------|------|
| 🐧 Linux | SSH | 22 |
| 🪟 Windows | **WinRM** (Windows Remote Management) | 5985 (HTTP) / 5986 (HTTPS) |

**Setup on Windows node:**

```powershell
# Run on the Windows managed node (PowerShell as Admin):
winrm quickconfig
Set-Item WSMan:\localhost\Service\Auth\Basic -Value true
Set-Item WSMan:\localhost\Service\AllowUnencrypted -Value true
```

**Inventory entry for Windows:**

```ini
[windows]
win1 ansible_host=192.168.1.200

[windows:vars]
ansible_user=Administrator
ansible_password=YourPassword
ansible_connection=winrm
ansible_winrm_transport=basic
ansible_port=5985
```

---

### Q6. 📂 What is an Ansible Inventory File? What are the default groups?

**Ans:**
The **inventory file** lists all managed nodes (hosts) and organizes them into groups. Ansible reads this to know which machines to target.

**Default location:** `/etc/ansible/hosts`

**Two default groups always exist:**

| Group | Contains |
|-------|---------|
| `all` | Every host in the inventory |
| `ungrouped` | Hosts not assigned to any group |

**Example inventory:**

```ini
# Individual host (goes into 'ungrouped'):
192.168.1.50

[webservers]
web1 ansible_host=192.168.1.101
web2 ansible_host=192.168.1.102

[dbservers]
db1 ansible_host=192.168.1.103

# Group of groups:
[production:children]
webservers
dbservers

# Group variables:
[webservers:vars]
http_port=80
ansible_user=ubuntu
```

---

### Q7. ⚡ What is the difference between Static and Dynamic Inventory?

**Ans:**

| | Static Inventory | Dynamic Inventory |
|--|-----------------|------------------|
| **Definition** | IP addresses of slave nodes are **fixed**, manually listed in a file | IPs are **dynamic** (e.g., cloud auto-scaling), fetched at runtime via script or plugin |
| **Format** | INI or YAML file | Python script or inventory plugin |
| **Updates** | Manual edit required | Auto-refreshed each run |
| **Best for** | Small, fixed infrastructure | Cloud environments (AWS, Azure, GCP) |
| **Example** | `/etc/ansible/hosts` | `aws_ec2.yml` plugin or `ec2.py` script |

**Dynamic inventory Python script example:**

```python
#!/usr/bin/env python3
# dynamic_inventory.py
# Fetches IPs from a cloud API / database and builds inventory

import json, boto3

ec2 = boto3.client('ec2', region_name='us-east-1')
instances = ec2.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])

hosts = []
for r in instances['Reservations']:
    for i in r['Instances']:
        hosts.append(i['PrivateIpAddress'])

print(json.dumps({"webservers": {"hosts": hosts}}))
```

```bash
chmod +x dynamic_inventory.py
ansible all -i dynamic_inventory.py -m ping
```

---

### Q8. 🔐 What are the best practices for SSH-based Linux node connection?

**Ans:**

**✅ Best Practices:**

1. **Use Passwordless SSH (Key-Based Authentication):**
```bash
ssh-keygen -t rsa -b 4096           # Generate key pair on control node
ssh-copy-id ubuntu@192.168.1.101    # Copy public key to managed node
ssh ubuntu@192.168.1.101             # Verify passwordless login
```

2. **Avoid using the `root` user on managed nodes:**
   - Create a dedicated Ansible user
   - Grant only `sudo` access (not full root login)

3. **Use `become: yes` in playbooks for privilege escalation** instead of logging in as root directly

4. **Disable password authentication on SSH:**
```bash
# /etc/ssh/sshd_config on managed node:
PasswordAuthentication no
PubkeyAuthentication yes
```

5. **Use `known_hosts` or set `host_key_checking = False` in controlled environments:**
```ini
# ansible.cfg
[defaults]
host_key_checking = False   # Only for trusted/dev environments
```

---

### Q9. 🔢 What is the Default Fork Limit in Ansible? How do you change it?

**Ans:**
The **fork limit** controls how many nodes Ansible can manage **in parallel simultaneously**.

**Default fork value: `5`** (Ansible runs tasks on 5 nodes at a time by default)

**How to change it:**

**Method 1 — ansible.cfg:**

```ini
[defaults]
forks = 30
```

**Method 2 — Command line:**

```bash
ansible-playbook -f 30 playbook.yml
# OR:
ansible-playbook --forks 30 playbook.yml
```

**Considerations:**

| Forks | RAM Recommendation |
|-------|-------------------|
| 5 (default) | ~500 MB |
| 100 forks | ~4 GB RAM |
| 500 forks | ~20 GB RAM |

> 💡 **Rule of thumb:** ~4 GB RAM per 100 forks. Increasing forks improves speed but increases CPU and memory usage on the control node.

---

### Q10. 🔁 What is Idempotency in Ansible? Why is it important?

**Ans:**
**Idempotency** means running the same Ansible playbook **multiple times produces the same result** — no unintended side effects or duplicate changes.

```yaml
# Idempotent task:
- name: Install Nginx
  apt:
    name: nginx
    state: present    # If already installed → SKIPS. If not → INSTALLS.
```

**Without idempotency (Shell script — NOT idempotent):**

```bash
#!/bin/bash
useradd devuser    # Run twice → ERROR: "user already exists"
```

**Why it matters:**

| Reason | Benefit |
|--------|---------|
| ✅ Safe re-runs | Run playbooks repeatedly without fear |
| ✅ Drift correction | Re-applying corrects configuration drift |
| ✅ Reliability | Predictable, consistent infrastructure state |
| ✅ CI/CD friendly | Playbooks can run on every deployment pipeline trigger |

---

### Q11. 📜 What is an Ansible Playbook? What is its basic structure?

**Ans:**
A **Playbook** is a YAML file containing one or more **plays**. Each play targets a group of hosts and defines a list of **tasks** to run on them.

```
Playbook
  └── Play 1 (hosts: webservers)
        ├── Task 1: Install Nginx
        ├── Task 2: Copy config file
        └── Task 3: Start Nginx service
  └── Play 2 (hosts: dbservers)
        ├── Task 1: Install MySQL
        └── Task 2: Create database
```

**Basic structure:**

```yaml
---
- name: Configure Web Servers          # Play name
  hosts: webservers                    # Target group
  become: yes                          # Run with sudo
  vars:
    http_port: 80

  tasks:
    - name: Install Nginx              # Task 1
      apt:
        name: nginx
        state: present

    - name: Start Nginx                # Task 2
      service:
        name: nginx
        state: started
        enabled: yes
```

---

### Q12. ⚙️ What is the `ansible.cfg` file? What are its key parameters?

**Ans:**
`ansible.cfg` is Ansible's **central configuration file** that controls its default behavior.

**Default search order for ansible.cfg:**
1. `ANSIBLE_CONFIG` environment variable
2. `./ansible.cfg` (current directory)
3. `~/.ansible.cfg` (home directory)
4. `/etc/ansible/ansible.cfg` (global default)

**Key parameters:**

```ini
[defaults]
inventory           = /path/to/inventory    # Inventory file path
remote_user         = ubuntu                # Default SSH user
host_key_checking   = False                 # Disable SSH key checking
timeout             = 30                    # SSH connection timeout (seconds)
forks               = 10                    # Parallel execution threads
retry_files_enabled = False                 # Disable .retry file creation
log_path            = /var/log/ansible.log  # Enable logging

[privilege_escalation]
become              = True                  # Enable sudo
become_method       = sudo                  # Use sudo for escalation
become_user         = root                  # Escalate to root

[ssh_connection]
ssh_args            = -o ControlMaster=auto -o ControlPersist=60s
control_path        = /tmp/ansible-ssh-%%h-%%p-%%r
pipelining          = True                  # Reduces SSH connections (faster)

[inventory]
enable_plugins      = host_list, script, yaml, ini, auto

[logging]
log_path            = /var/log/ansible.log
log_format          = %(asctime)s %(levelname)s %(name)s: %(message)s
```

**Generate a sample config file with all options:**

```bash
ansible-config init --disabled > ansible.cfg
# Creates a fully commented config file you can customize
```

---

## 🟡 Intermediate Questions

---

### Q13. 🔐 How do you encrypt an existing file in Ansible? How do you create a new encrypted file?

**Ans:**

**Encrypt an existing file:**

```bash
ansible-vault encrypt test.yml
# Prompts for vault password → file is now encrypted
```

**Decrypt an existing file:**

```bash
ansible-vault decrypt test.yml
# Prompts for vault password once → file is decrypted
```

**Create a new encrypted file from scratch:**

```bash
ansible-vault create hello.yml
# Prompts to SET password (entered twice for confirmation)
# Opens editor → add your secrets → save → file is encrypted
```

**Edit an encrypted file:**

```bash
ansible-vault edit hello.yml
# Prompts for password once → opens in editor → re-encrypts on save
```

**View without decrypting:**

```bash
ansible-vault view hello.yml
```

**Password prompt summary:**

| Operation | Password Prompts |
|-----------|:---------------:|
| `create` | 2× (set + confirm) |
| `encrypt` | 2× (set + confirm) |
| `decrypt` | 1× (enter) |
| `edit` | 1× (enter) |
| `view` | 1× (enter) |

**Running playbook with vault-encrypted files:**

```bash
ansible-playbook playbook.yml --ask-vault-pass
# OR:
ansible-playbook playbook.yml --vault-password-file ~/.vault_pass
```

---

### Q14. 🔔 What is the purpose of Handlers in Ansible?

**Ans:**
**Handlers** are special tasks that run **only when notified** by another task — and only **if that task made a change**.

**The problem handlers solve:**

> Suppose you have tasks to: (1) Install Apache and (2) Restart Apache.
> If Apache is **already installed** (task 1 is skipped/no change), restarting it unnecessarily is wasteful.
> A handler solves this — it only restarts if the install task **actually made a change**.

```yaml
tasks:
  - name: Install Apache
    apt:
      name: apache2
      state: present
    notify: Restart Apache          # Only triggers if this task CHANGED

  - name: Deploy Apache config
    template:
      src: httpd.conf.j2
      dest: /etc/apache2/httpd.conf
    notify: Restart Apache          # Notified twice, but handler runs ONCE

handlers:
  - name: Restart Apache
    service:
      name: apache2
      state: restarted
```

**Handler key behaviors:**

| Behavior | Detail |
|----------|--------|
| ⏱️ Runs at end of play | Not immediately when notified |
| 1️⃣ Runs only ONCE | Even if notified multiple times |
| ✅ Runs only if notified | Skipped if triggering task reports no change |
| 📋 Runs in defined order | Predictable execution order |

---

### Q15. 🔢 How do Variables work in Ansible? Explain different ways to define them.

**Ans:**

**1. In the Playbook (inline `vars`):**

```yaml
vars:
  app_name: myapp
  http_port: 8080
```

**2. External variable files (`vars_files`):**

```yaml
vars_files:
  - vars/app_vars.yml
  - vars/secrets.yml   # Can be vault-encrypted
```

> 📌 **File variables override playbook inline variables.**

**3. Command-line (`-e` / `--extra-vars`) — Highest Priority:**

```bash
ansible-playbook playbook.yml -e "env=production version=2.1"
```

**4. group_vars / host_vars:**

```
inventory/
├── group_vars/
│   ├── all.yml          # Applies to all hosts
│   └── webservers.yml   # Applies to webserver group
└── host_vars/
    └── web1.yml         # Applies to web1 only
```

**5. Registered Variables (capture task output):**

```yaml
- name: Get system uptime
  command: uptime
  register: uptime_result

- debug:
    msg: "{{ uptime_result.stdout }}"
```

**Variable Precedence (Lowest → Highest):**

```
Role defaults → Inventory vars → group_vars → host_vars
→ Playbook vars → Task vars → set_facts
→ Extra vars (-e)  ← HIGHEST PRIORITY
```

---

### Q16. 🔍 What are Ansible Facts? How do you use them?

**Ans:**
**Facts** are system information automatically collected from managed nodes at the start of each playbook run using the built-in `setup` module.

```bash
# View all facts for a host:
ansible all -m setup

# Filter specific facts:
ansible all -m setup -a "filter=ansible_distribution*"
```

**Commonly used facts:**

| Fact | Example Value |
|------|--------------|
| `ansible_hostname` | `web1` |
| `ansible_os_family` | `Debian`, `RedHat` |
| `ansible_distribution` | `Ubuntu`, `CentOS` |
| `ansible_distribution_version` | `22.04` |
| `ansible_default_ipv4.address` | `192.168.1.101` |
| `ansible_memtotal_mb` | `8192` |
| `ansible_processor_cores` | `4` |

**Using facts in playbooks:**

```yaml
- name: OS-specific package install
  package:
    name: "{{ 'apache2' if ansible_os_family == 'Debian' else 'httpd' }}"
    state: present

- name: Print system info
  debug:
    msg: "Host: {{ ansible_hostname }}, OS: {{ ansible_distribution }} {{ ansible_distribution_version }}"
```

**Disable fact gathering (faster playbooks):**

```yaml
- hosts: all
  gather_facts: no    # Skip setup module — speeds up playbooks
  tasks:
    - name: Quick task
      command: echo "hello"
```

---

### Q17. 🔀 How do Conditionals work in Ansible?

**Ans:**
Conditionals use the `when` keyword to control whether a task executes.

```yaml
# Basic OS check:
- name: Install on Debian only
  apt:
    name: nginx
    state: present
  when: ansible_os_family == "Debian"

# AND condition (both must be true):
- name: Run on Ubuntu 22.04 only
  debug:
    msg: "Ubuntu 22.04!"
  when:
    - ansible_distribution == "Ubuntu"
    - ansible_distribution_version == "22.04"

# OR condition:
- name: Run on Ubuntu or Debian
  apt:
    name: curl
    state: present
  when: ansible_distribution == "Ubuntu" or ansible_distribution == "Debian"

# Based on registered variable:
- name: Check service status
  command: systemctl status nginx
  register: nginx_status
  ignore_errors: yes

- name: Start Nginx if not running
  service:
    name: nginx
    state: started
  when: nginx_status.rc != 0

# Check if variable is defined:
- name: Run only if variable exists
  debug:
    msg: "{{ custom_var }}"
  when: custom_var is defined
```

---

### Q18. 🔁 How do Loops work in Ansible? What is the difference between `loop` and `with_items`?

**Ans:**

| | `loop` | `with_items` |
|--|--------|-------------|
| **Status** | ✅ Modern (Ansible 2.5+) | ⚠️ Legacy (still works) |
| **Recommended?** | ✅ Yes | Use `loop` for new playbooks |
| **Flattening** | Does NOT flatten nested lists | Flattens one level |

**Basic loop:**

```yaml
- name: Install multiple packages
  apt:
    name: "{{ item }}"
    state: present
  loop:
    - nginx
    - git
    - curl
    - vim
```

**Loop with dictionaries:**

```yaml
- name: Create multiple users
  user:
    name: "{{ item.name }}"
    shell: "{{ item.shell }}"
  loop:
    - { name: "alice", shell: "/bin/bash" }
    - { name: "bob",   shell: "/bin/sh" }
```

**Loop with index:**

```yaml
- name: Print with index
  debug:
    msg: "{{ index }}: {{ item }}"
  loop: ["web", "db", "cache"]
  loop_control:
    index_var: index
```

---

### Q19. 📄 What are Jinja2 Templates in Ansible? When would you use them?

**Ans:**
**Jinja2 templates** (`.j2` files) allow you to create **dynamic configuration files** where variables are substituted at runtime.

**Template file (`nginx.conf.j2`):**

```jinja2
server {
    listen {{ http_port }};
    server_name {{ ansible_fqdn }};

    {% if enable_ssl %}
    listen {{ https_port }} ssl;
    ssl_certificate {{ ssl_cert_path }};
    {% endif %}

    location / {
        root {{ web_root }};
        index index.html;
    }
}
```

**Using in playbook:**

```yaml
- name: Deploy Nginx config
  template:
    src: templates/nginx.conf.j2
    dest: /etc/nginx/sites-available/default
    owner: root
    mode: '0644'
  notify: Reload Nginx
```

**Common Jinja2 syntax:**

```jinja2
{{ variable }}                           {# Variable substitution #}
{{ my_var | default("fallback") }}       {# Default filter #}
{{ my_var | upper }}                     {# Uppercase filter #}
{% if condition %}...{% endif %}          {# Conditional block #}
{% for item in list %}...{% endfor %}     {# Loop block #}
{# This is a comment #}                  {# Comment — not rendered #}
```

**Use cases:** Nginx/Apache config, app config files, systemd unit files, SSH config, Prometheus config.

---

### Q20. 🎭 What are Ansible Roles? What is the directory structure?

**Ans:**
**Roles** are reusable, self-contained units of automation with a standardized structure. They promote code reuse and team collaboration.

```bash
# Create a role:
ansible-galaxy role init webserver
```

**Directory structure:**

```
roles/webserver/
├── tasks/
│   └── main.yml       ← Main task list (required)
├── handlers/
│   └── main.yml       ← Handlers triggered by tasks
├── templates/
│   └── nginx.conf.j2  ← Jinja2 templates
├── files/
│   └── index.html     ← Static files to copy
├── vars/
│   └── main.yml       ← Role variables (high precedence)
├── defaults/
│   └── main.yml       ← Default variables (lowest precedence, overridable)
├── meta/
│   └── main.yml       ← Role metadata + dependencies
└── README.md
```

**Using a role in a playbook:**

```yaml
---
- name: Configure Servers
  hosts: webservers
  become: yes
  roles:
    - common           # Runs roles/common/tasks/main.yml
    - webserver        # Runs roles/webserver/tasks/main.yml
    - { role: ssl, when: enable_ssl }   # Conditional role
```

**Benefits of Roles:**
- ✅ Reusability across projects
- ✅ Better organization for large playbooks
- ✅ Easy team collaboration
- ✅ Testable with Molecule
- ✅ Shareable via Ansible Galaxy

---

### Q21. 🔍 How do you debug an Ansible Playbook execution?

**Ans:**

**Method 1 — Verbose flags:**

```bash
ansible-playbook playbook.yml -v        # Basic: task results
ansible-playbook playbook.yml -vv       # More: file diffs
ansible-playbook playbook.yml -vvv      # SSH-level details
ansible-playbook playbook.yml -vvvv     # Connection-level debug
```

**Method 2 — `debug` module + `register`:**

```yaml
- name: Run a command
  command: df -h
  register: disk_output

- name: Print output
  debug:
    msg: "{{ disk_output.stdout }}"

- name: Print all variables
  debug:
    var: hostvars[inventory_hostname]
```

**Method 3 — Check mode (dry run — no changes):**

```bash
ansible-playbook playbook.yml --check
ansible-playbook playbook.yml --check --diff   # Show exact file changes
```

**Method 4 — Step mode (confirm each task):**

```bash
ansible-playbook playbook.yml --step
```

**Method 5 — `assert` module for validation:**

```yaml
- name: Validate required variable
  assert:
    that:
      - db_host is defined
      - http_port | int > 0
    fail_msg: "Required variables are not set!"
```

**Method 6 — Enable logging in ansible.cfg:**

```ini
[defaults]
log_path = /var/log/ansible.log
```

---

### Q22. 🔒 How do you run tasks with sudo privileges in Ansible?

**Ans:**
Use `become: yes` to run tasks with elevated (sudo) privileges.

**Play-level (all tasks run as sudo):**

```yaml
- name: Configure Server
  hosts: webservers
  become: yes                  # All tasks in this play run with sudo
  become_user: root            # Escalate to root (default)
  become_method: sudo          # Use sudo (default; can also be su, pbrun, etc.)

  tasks:
    - name: Install Nginx
      apt:
        name: nginx
        state: present
```

**Task-level (selective sudo):**

```yaml
tasks:
  - name: Read app config (no sudo needed)
    shell: cat /opt/app/config.yml
    become: no

  - name: Restart service (sudo needed)
    service:
      name: myapp
      state: restarted
    become: yes               # Only this task uses sudo
```

**Run playbook and prompt for sudo password:**

```bash
ansible-playbook playbook.yml --ask-become-pass
```

---

### Q23. 🏷️ What are Tags in Ansible? Why are they useful?

**Ans:**
**Tags** allow you to run or skip **specific tasks** in a playbook without running the entire thing — very useful for large playbooks and CI/CD pipelines.

```yaml
tasks:
  - name: Install packages
    apt: { name: nginx, state: present }
    tags: [install, packages]

  - name: Configure Nginx
    template:
      src: nginx.conf.j2
      dest: /etc/nginx/nginx.conf
    tags: [configure, nginx]

  - name: Start services
    service: { name: nginx, state: started }
    tags: [start, services]
```

```bash
# Run only install tasks:
ansible-playbook playbook.yml --tags "install"

# Run multiple tags:
ansible-playbook playbook.yml --tags "install,configure"

# Skip specific tags:
ansible-playbook playbook.yml --skip-tags "start"

# List all available tags:
ansible-playbook playbook.yml --list-tags
```

**Special tags:**

```yaml
tags: always     # Always runs, even when other tags are specified
tags: never      # Never runs unless explicitly called by tag name
```

---

### Q24. 📦 What is Ansible Galaxy?

**Ans:**
**Ansible Galaxy** is the official community hub for sharing, downloading, and managing Ansible **roles** and **collections**.

🔗 https://galaxy.ansible.com

```bash
# Install a role:
ansible-galaxy role install geerlingguy.nginx

# Install specific version:
ansible-galaxy role install geerlingguy.nginx,3.0.0

# List installed roles:
ansible-galaxy role list

# Install from requirements.yml:
ansible-galaxy install -r requirements.yml

# Install a collection (modern format):
ansible-galaxy collection install community.general
ansible-galaxy collection install amazon.aws
```

**requirements.yml:**

```yaml
roles:
  - name: geerlingguy.nginx
  - name: geerlingguy.mysql
    version: "3.1.0"

collections:
  - name: community.general
  - name: amazon.aws
    version: ">=2.0"
```

---

### Q25. 🖥️ What is Ansible Tower / AWX?

**Ans:**

| | Ansible Tower | AWX |
|--|--------------|-----|
| **Type** | Commercial (Red Hat) | Open-source upstream |
| **Support** | ✅ Enterprise | Community only |
| **Cost** | Paid subscription | Free |
| **Stability** | Stable releases | Frequent, may be less stable |

**Key features of both:**

| Feature | Description |
|---------|-------------|
| 🖥️ **Web UI** | Run playbooks visually — no CLI needed |
| 👥 **RBAC** | Control who can run which jobs on which hosts |
| 📅 **Job Scheduling** | Cron-like scheduling for playbooks |
| 🔌 **REST API** | Trigger automation from external tools |
| 📊 **Audit Logging** | Full history of who ran what, when, and results |
| 🔐 **Credential Management** | Securely store SSH keys, passwords, cloud creds |
| 📦 **Inventory Sync** | Auto-sync with AWS/Azure/GCP dynamic inventories |
| 🔔 **Notifications** | Slack, email, webhook alerts on success/failure |

---

## 🔴 Advanced Questions

---

### Q26. 💥 What is Error Handling in Ansible? Explain `block`, `rescue`, `always`.

**Ans:**

`block` / `rescue` / `always` works like **try / catch / finally** in programming.

```yaml
tasks:
  - block:                              # TRY — normal tasks
      - name: Deploy application
        command: /opt/deploy.sh

      - name: Health check
        uri:
          url: http://localhost:8080/health
          status_code: 200

    rescue:                             # CATCH — runs if block fails
      - name: Rollback deployment
        command: /opt/rollback.sh

      - name: Send failure alert
        uri:
          url: "{{ slack_webhook }}"
          method: POST
          body: '{"text": "⚠️ Deploy FAILED on {{ inventory_hostname }}"}'

    always:                             # FINALLY — always runs
      - name: Send completion notification
        debug:
          msg: "Deployment attempt finished on {{ inventory_hostname }}"
```

**Other error handling keywords:**

```yaml
# Ignore task failure and continue:
- name: Stop old service (may not exist)
  service:
    name: old-service
    state: stopped
  ignore_errors: yes

# Custom failure condition:
- name: Run script
  command: /opt/check.sh
  register: result
  failed_when:
    - result.rc != 0
    - "'CRITICAL' in result.stdout"

# Custom changed condition:
- name: Read-only check (never mark as changed)
  command: /opt/status.sh
  changed_when: false

# Stop entire play if ANY host fails:
- hosts: all
  any_errors_fatal: true
  tasks:
    - name: Critical task
      command: /opt/critical.sh

# Rolling update — stop if >25% of hosts fail:
- hosts: webservers
  max_fail_percentage: 25
  serial: 2
```

---

### Q27. 🔄 How does Ansible work with CI/CD pipelines? Give an example.

**Ans:**
Ansible integrates with all major CI/CD tools to automate deployments after code is built and tested.

**Ansible + Jenkins (Jenkinsfile):**

```groovy
pipeline {
    agent any
    stages {
        stage('Build') {
            steps { sh 'docker build -t myapp:${BUILD_NUMBER} .' }
        }
        stage('Deploy') {
            steps {
                sh """
                  ansible-playbook -i inventory/production \
                    -e "image_tag=${BUILD_NUMBER}" \
                    --vault-password-file ~/.vault_pass \
                    deploy.yml
                """
            }
        }
    }
    post {
        failure { sh 'ansible-playbook rollback.yml' }
    }
}
```

**Ansible + GitHub Actions:**

```yaml
# .github/workflows/deploy.yml
name: Deploy with Ansible
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: pip3 install ansible
      - name: Setup SSH
        run: |
          mkdir -p ~/.ssh
          echo "${{ secrets.SSH_PRIVATE_KEY }}" > ~/.ssh/id_rsa
          chmod 600 ~/.ssh/id_rsa
      - name: Deploy
        run: ansible-playbook -i inventory/production deploy.yml
        env:
          ANSIBLE_VAULT_PASSWORD: ${{ secrets.VAULT_PASSWORD }}
```

---

### Q28. 🐳 How does Ansible work with Docker and Kubernetes?

**Ans:**

**Docker with Ansible:**

```yaml
- name: Deploy Docker container
  hosts: dockerhosts
  become: yes
  tasks:
    - name: Pull latest image
      docker_image:
        name: "myapp:{{ image_tag }}"
        source: pull

    - name: Run container
      docker_container:
        name: myapp
        image: "myapp:{{ image_tag }}"
        state: started
        restart_policy: always
        ports: ["8080:8080"]
        env:
          DB_HOST: "{{ db_host }}"
          APP_ENV: production
```

**Kubernetes with Ansible:**

```yaml
- name: Deploy to Kubernetes
  hosts: localhost
  tasks:
    - name: Apply K8s deployment
      kubernetes.core.k8s:
        state: present
        definition:
          apiVersion: apps/v1
          kind: Deployment
          metadata:
            name: myapp
            namespace: production
          spec:
            replicas: 3
            template:
              spec:
                containers:
                  - name: myapp
                    image: "myapp:{{ image_tag }}"

    - name: Wait for rollout to complete
      kubernetes.core.k8s_rollout_status:
        name: myapp
        namespace: production
```

---

### Q29. 🌐 Explain Dynamic Inventory in detail. How is it configured for AWS?

**Ans:**

```bash
# Install AWS dependencies:
pip3 install boto3 botocore
ansible-galaxy collection install amazon.aws
```

**aws_ec2.yml (inventory plugin config):**

```yaml
plugin: amazon.aws.aws_ec2
regions:
  - us-east-1
  - us-west-2
filters:
  instance-state-name: running
  tag:Environment: production
keyed_groups:
  - key: tags.Role
    prefix: role
  - key: placement.region
    prefix: region
hostnames:
  - private-ip-address
compose:
  ansible_host: private_ip_address
  ansible_user: "'ubuntu'"
```

```bash
# Test dynamic inventory:
ansible-inventory -i aws_ec2.yml --list
ansible-inventory -i aws_ec2.yml --graph

# Use with playbook:
ansible-playbook -i aws_ec2.yml deploy.yml
```

---

### Q30. 🚀 What are Ansible Execution Strategies? What is `serial`?

**Ans:**

**Execution strategies control how tasks run across hosts:**

| Strategy | Behavior |
|----------|---------|
| `linear` (default) | All hosts complete each task before moving to the next |
| `free` | Each host runs as fast as it can, independently |
| `debug` | Interactive debugging mode |

```yaml
- hosts: all
  strategy: free     # Each host runs independently — faster for independent tasks
  tasks:
    - name: Update packages
      apt: { upgrade: dist }
```

**Serial (Rolling Updates):**

```yaml
- hosts: webservers
  serial: 2          # Deploy to 2 hosts at a time (safe rolling update)
  tasks:
    - name: Remove from load balancer
      uri:
        url: "{{ lb_url }}/remove/{{ inventory_hostname }}"
    - name: Update app
      apt: { name: myapp, state: latest }
    - name: Re-add to load balancer
      uri:
        url: "{{ lb_url }}/add/{{ inventory_hostname }}"
```

```yaml
serial: "30%"        # 30% of hosts at a time
serial:
  - 1                # 1 first (canary deploy)
  - 5                # Then 5
  - "50%"            # Then 50% of remaining
```

---

### Q31. 🔧 What is `group_vars` and `host_vars`? Why use them?

**Ans:**
They are **directories** for organizing variables per group or per individual host — keeping playbooks clean and DRY.

```
inventory/
├── hosts
├── group_vars/
│   ├── all.yml            # Variables for EVERY host
│   ├── webservers.yml     # Variables for webserver group only
│   └── dbservers.yml      # Variables for dbserver group only
└── host_vars/
    ├── web1.yml           # Variables for web1 ONLY
    └── db1.yml            # Variables for db1 ONLY
```

```yaml
# group_vars/all.yml:
timezone: UTC
ntp_server: pool.ntp.org
admin_email: ops@company.com

# group_vars/webservers.yml:
http_port: 80
web_root: /var/www/html

# host_vars/web1.yml:
http_port: 8080        # Overrides group var for this specific host
server_role: primary
```

**Priority:** `host_vars` > `group_vars/{groupname}` > `group_vars/all`

---

### Q32. 📡 What is `pipelining` in Ansible? How does it improve performance?

**Ans:**
**Pipelining** reduces the number of SSH connections needed to execute a task by streaming module execution over a single SSH connection instead of copying files.

```ini
# ansible.cfg
[ssh_connection]
pipelining = True
```

**Without pipelining:**
```
1. SSH connect → 2. Copy module to /tmp → 3. Execute → 4. Delete temp files
```

**With pipelining:**
```
1. SSH connect → 2. Stream + execute in one step (no temp files)
```

> ⚠️ **Requirement:** `requiretty` must be **disabled** in `/etc/sudoers` on managed nodes for pipelining to work with `become`.

---

### Q33. ⏱️ How do you run long tasks asynchronously in Ansible?

**Ans:**

```yaml
# Fire and forget (poll: 0):
- name: Start backup job
  command: /opt/backup.sh
  async: 3600          # Max allowed time in seconds
  poll: 0              # Don't wait — fire and forget

# Check status later:
- name: Start deployment
  command: /opt/deploy.sh
  async: 600
  poll: 30             # Check every 30 seconds
  register: deploy_job

- name: Wait for deployment to complete
  async_status:
    jid: "{{ deploy_job.ansible_job_id }}"
  register: job_result
  until: job_result.finished
  retries: 20
  delay: 30
```

---

### Q34. 📎 What are Ansible Submodules? What are Git Submodules in Ansible context?

**Ans:**

**Ansible Submodules** refer to **Git Submodules** used within Ansible projects to include shared roles or libraries from separate repositories.

```bash
# Add a shared role as a git submodule:
git submodule add https://github.com/org/ansible-common-roles.git roles/common
git submodule update --init --recursive

# Clone a project WITH its submodules:
git clone --recurse-submodules https://github.com/myorg/ansible-project.git
```

> This is different from **Ansible Galaxy** — Galaxy is for installing community roles, while Git submodules are for embedding your own internal shared roles.

---

### Q35. 🔁 What is the difference between `copy` and `synchronize` modules?

**Ans:**

| | `copy` | `synchronize` |
|--|--------|-------------|
| **What it does** | Copies a file or directory to managed node | Uses `rsync` to sync files (recursive, incremental) |
| **Best for** | Small files, single files | Large directories, many files |
| **Speed** | Slower for large data | ⚡ Faster (only transfers changes) |
| **Recursive?** | Yes, with `src: dir/` | ✅ Yes, by default |
| **Requires** | Nothing extra | `rsync` on both nodes |

```yaml
# copy module:
- copy:
    src: /local/app.conf
    dest: /etc/app/app.conf
    backup: yes

# synchronize module:
- synchronize:
    src: /local/www/
    dest: /var/www/html/
    recursive: yes
    delete: yes     # Remove files on dest not in src
```

---

### Q36. 🧪 How do you test Ansible Roles? What is Molecule?

**Ans:**
**Molecule** is the official testing framework for Ansible roles. It provisions test instances, runs the role, verifies the results, and tears everything down.

```bash
# Install Molecule:
pip3 install molecule molecule-docker ansible-lint

# Initialize Molecule for an existing role:
cd roles/webserver
molecule init scenario

# Run tests:
molecule test           # Full test cycle: create → converge → verify → destroy
molecule converge       # Apply role to test instance
molecule verify         # Run assertions
molecule destroy        # Tear down test environment
```

**molecule/default/verify.yml:**

```yaml
- name: Verify Nginx is running
  hosts: all
  tasks:
    - name: Check Nginx service
      service_facts:

    - name: Assert Nginx is running
      assert:
        that:
          - "'nginx' in services"
          - "services['nginx'].state == 'running'"
```

---

### Q37. 🔐 How does Ansible ensure secrets are never exposed in logs?

**Ans:**

**1. Use `no_log: true` on sensitive tasks:**

```yaml
- name: Set database password
  mysql_user:
    name: appuser
    password: "{{ db_password }}"
  no_log: true          # Hides ALL output for this task
```

**2. Encrypt variables with Vault:**

```bash
ansible-vault encrypt_string 'secret_password' --name 'db_password'
```

**3. Use `--vault-password-file` instead of entering password interactively:**

```bash
ansible-playbook playbook.yml --vault-password-file ~/.vault_pass
```

**4. Restrict `log_path` file permissions:**

```bash
chmod 600 /var/log/ansible.log
chown ansible_user:ansible_user /var/log/ansible.log
```

---

### Q38. 🔄 What is `ansible-lint`? Why is it important?

**Ans:**
`ansible-lint` is a command-line tool that checks Ansible playbooks and roles for **best practice violations, syntax errors, and anti-patterns**.

```bash
# Install:
pip3 install ansible-lint

# Lint a playbook:
ansible-lint playbook.yml

# Lint all YAML in a project:
ansible-lint

# Lint a role:
ansible-lint roles/webserver/
```

**Common issues it catches:**

| Issue | Example |
|-------|---------|
| `yaml[truthy]` | Using `yes/no` instead of `true/false` |
| `name[missing]` | Task has no `name:` field |
| `no-free-form` | Using free-form `command:` instead of structured format |
| `risky-file-permissions` | Not specifying file mode |
| `deprecated-bare-vars` | Using bare variable names in loops |

---

## 🏢 Scenario-Based Questions

---

### Q39. 🚨 What would you do if an Ansible playbook fails halfway through on some hosts but completes on others?

**Ans:**

```bash
# 1. Check which hosts failed:
ansible-playbook playbook.yml -v
# Ansible creates a retry file: playbook.retry

# 2. Retry only failed hosts:
ansible-playbook playbook.yml --limit @playbook.retry

# 3. Or limit to specific host for debugging:
ansible-playbook playbook.yml --limit web3 -vvv

# 4. Use --check to verify fix before applying:
ansible-playbook playbook.yml --limit web3 --check
```

**Prevention with `max_fail_percentage`:**

```yaml
- hosts: webservers
  max_fail_percentage: 0     # Stop immediately if ANY host fails
  serial: 1                   # One host at a time for easy debugging
```

---

### Q40. 🔄 How would you perform a zero-downtime rolling deployment with Ansible?

**Ans:**

```yaml
---
- name: Zero-Downtime Rolling Deploy
  hosts: webservers
  serial: 1               # One server at a time
  max_fail_percentage: 0  # Stop if any server fails

  tasks:
    - name: Remove from load balancer
      uri:
        url: "http://lb.internal/remove/{{ inventory_hostname }}"
        method: POST

    - name: Wait for connections to drain
      pause:
        seconds: 30

    - name: Stop application
      service:
        name: myapp
        state: stopped

    - name: Deploy new version
      unarchive:
        src: "myapp-{{ version }}.tar.gz"
        dest: /opt/myapp/
        remote_src: no

    - name: Start application
      service:
        name: myapp
        state: started

    - name: Health check — wait for app to be ready
      uri:
        url: http://localhost:8080/health
        status_code: 200
      register: health
      until: health.status == 200
      retries: 10
      delay: 10

    - name: Re-add to load balancer
      uri:
        url: "http://lb.internal/add/{{ inventory_hostname }}"
        method: POST
```

---

### Q41. 🔐 A developer accidentally committed a plaintext password in a playbook. What do you do?

**Ans:**

```bash
# Step 1: Immediately rotate/revoke the exposed credential
# (Assume it's compromised — even if caught quickly)

# Step 2: Remove from Git history using BFG Repo Cleaner:
bfg --replace-text passwords.txt   # Replace leaked string with '***REMOVED***'
git push --force

# OR using git filter-branch:
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch playbooks/secrets.yml" \
  --prune-empty --tag-name-filter cat -- --all

# Step 3: Encrypt the secret properly with Ansible Vault:
ansible-vault encrypt_string 'new_password' --name 'db_password'

# Step 4: Add the file to .gitignore (if it was a vars file):
echo "vars/secrets.yml" >> .gitignore

# Step 5: Use vault in the playbook going forward:
vars_files:
  - vars/secrets.yml    # Now encrypted with vault
```

> ⚠️ **Always revoke credentials first** — assume they are compromised regardless of how fast you caught it.

---

### Q42. 🏢 What Git strategy does your organization use alongside Ansible?

**Ans (Sample):**
In our organization, we use **Gitflow** for managing Ansible code with the following structure:

```
main        → Production-ready playbooks (protected branch)
develop     → Integration branch for tested playbooks
feature/*   → New playbooks or role development
release/*   → Pre-release testing of playbook changes
hotfix/*    → Emergency fixes to production playbooks
```

**Our Ansible code workflow:**

```bash
# 1. Create feature branch:
git checkout -b feature/add-monitoring-role develop

# 2. Develop and test role with Molecule:
molecule test

# 3. Lint playbooks:
ansible-lint

# 4. Push and open PR to develop:
git push origin feature/add-monitoring-role

# 5. After code review → merge to develop → auto-runs in staging via Jenkins

# 6. Create release branch → test in staging → merge to main → deploy to prod
```

---

### Q43. 📊 How do you manage different environments (dev/staging/production) in Ansible?

**Ans:**

```
inventory/
├── dev/
│   ├── hosts
│   ├── group_vars/
│   │   ├── all.yml        # dev defaults
│   │   └── webservers.yml
│   └── host_vars/
├── staging/
│   ├── hosts
│   └── group_vars/
│       └── all.yml        # staging config
└── production/
    ├── hosts
    ├── group_vars/
    │   └── all.yml        # production config (stricter)
    └── host_vars/
```

```bash
# Deploy to dev:
ansible-playbook -i inventory/dev deploy.yml

# Deploy to staging:
ansible-playbook -i inventory/staging deploy.yml

# Deploy to production:
ansible-playbook -i inventory/production deploy.yml -e "version=2.1.0"
```

```yaml
# inventory/production/group_vars/all.yml
env: production
log_level: warn
replicas: 3
enable_ssl: true
db_host: prod-db.internal

# inventory/dev/group_vars/all.yml
env: development
log_level: debug
replicas: 1
enable_ssl: false
db_host: dev-db.internal
```

---

### Q44. ⚡ How would you speed up a slow Ansible playbook?

**Ans:**

```ini
# ansible.cfg optimizations:
[defaults]
forks = 20               # Increase parallel execution
gather_facts = False     # Disable if facts not needed (add per-play)

[ssh_connection]
pipelining = True        # Reduce SSH connection overhead
ssh_args = -o ControlMaster=auto -o ControlPersist=60s  # SSH multiplexing
```

**In playbooks:**

```yaml
# 1. Disable fact gathering where not needed:
gather_facts: no

# 2. Use async for long-running tasks:
async: 300
poll: 10

# 3. Use package module instead of apt/yum (auto-detects OS):
- package:
    name: nginx
    state: present

# 4. Use tags to run only what's needed:
ansible-playbook playbook.yml --tags "deploy"

# 5. Limit to specific hosts:
ansible-playbook playbook.yml --limit webservers
```

---

### Q45. 🔍 How do you check what an Ansible playbook will do BEFORE running it?

**Ans:**

```bash
# Check mode — shows what WOULD change, makes NO changes:
ansible-playbook playbook.yml --check

# Check mode + show file diffs:
ansible-playbook playbook.yml --check --diff

# List all tasks that WOULD run (with current tags/limits):
ansible-playbook playbook.yml --list-tasks

# List all hosts that WOULD be targeted:
ansible-playbook playbook.yml --list-hosts

# List all tags available:
ansible-playbook playbook.yml --list-tags

# Step-by-step confirmation:
ansible-playbook playbook.yml --step
```

> 💡 Make `--check --diff` a **mandatory step** in code review pipelines before any production deployment.

---

### Q46. 📋 What is the difference between `command`, `shell`, and `raw` modules?

**Ans:**

| Module | Shell features | Pipe/redirect | Python needed | Use when |
|--------|:-------------:|:-------------:|:-------------:|----------|
| `command` | ❌ No | ❌ No | ✅ Yes | Simple commands, most secure |
| `shell` | ✅ Yes | ✅ Yes | ✅ Yes | Need pipes, redirects, env vars |
| `raw` | ✅ Yes | ✅ Yes | ❌ No | Bootstrapping — before Python install |

```yaml
# command — no shell features, most secure:
- command: /usr/bin/systemctl status nginx

# shell — supports pipes and redirects:
- shell: ps aux | grep nginx | wc -l
  register: nginx_procs

# raw — no Python needed on remote:
- raw: apt-get install -y python3    # Bootstrap Python first
```

> ✅ **Best practice:** Use `command` by default. Use `shell` only when you need shell features. Use `raw` only for bootstrapping.

---

### Q47. 🧹 How do you clean up a managed node completely using Ansible?

**Ans:**

```yaml
---
- name: Clean up managed node
  hosts: decommission_servers
  become: yes

  tasks:
    - name: Stop all application services
      service:
        name: "{{ item }}"
        state: stopped
      loop: ["nginx", "mysql", "myapp"]
      ignore_errors: yes

    - name: Remove application packages
      apt:
        name: ["nginx", "mysql-server"]
        state: absent
        purge: yes

    - name: Remove application directories
      file:
        path: "{{ item }}"
        state: absent
      loop:
        - /opt/myapp
        - /etc/myapp
        - /var/log/myapp

    - name: Remove application user
      user:
        name: appuser
        state: absent
        remove: yes

    - name: Clean apt cache
      apt:
        autoclean: yes
        autoremove: yes
```

---

### Q48. 🏆 What are the most important Ansible Best Practices?

**Ans:**

| ✅ Practice | 💡 Why |
|------------|--------|
| Use **Roles** for all reusable logic | Modular, testable, shareable |
| Avoid hardcoding values | Use variables for flexibility |
| Use **group_vars / host_vars** | Clean separation per environment |
| Use **Ansible Vault** for ALL secrets | Security and compliance |
| Write descriptive `name:` for every task | Self-documenting automation |
| Use **Tags** | Run only what you need |
| Always test with `--check --diff` first | Prevent unintended changes |
| Use **Handlers** for service restarts | Efficient — runs only when needed, once |
| Pin versions (`state: present` not `latest`) | Predictable, stable deploys |
| Use `no_log: true` on credential tasks | Prevent secret leaks in output |
| Use `ansible-lint` and `yamllint` | Catch bugs and anti-patterns early |
| Test roles with **Molecule** | Verify before production |
| Version control everything in Git | Auditability, rollback, collaboration |
| Use **serial** for rolling updates | Zero-downtime deployments |
| Set `forks` based on infrastructure size | Optimal performance |
| Use `pipelining = True` in ansible.cfg | Faster SSH execution |
| Use `async` for long-running tasks | Avoid SSH timeout issues |
| Separate inventories per environment | dev / staging / production isolation |

---

## 📊 Quick Comparison Summary

### Core Concepts

| Concept | One Line |
|---------|---------|
| **Agentless** | No software on managed nodes — only SSH/WinRM needed |
| **Idempotent** | Same playbook run multiple times = same result |
| **Push-based** | Master sends config to slaves (not slaves pulling) |
| **Inventory** | List of managed hosts, organized in groups |
| **Playbook** | YAML file with plays; each play has tasks |
| **Role** | Reusable, structured automation unit |
| **Handler** | Task that runs only when notified + only once |
| **Vault** | Encryption for secrets in YAML files |
| **Facts** | Auto-gathered system info (OS, IP, RAM, etc.) |
| **Tags** | Run/skip specific tasks without running full playbook |

### Modules Quick Reference

| Task | Module |
|------|--------|
| Install package (Ubuntu) | `apt` |
| Install package (CentOS) | `yum` or `dnf` |
| Install package (any OS) | `package` |
| Manage services | `service` |
| Copy file | `copy` |
| Template file | `template` |
| Manage files/dirs | `file` |
| Run command (safe) | `command` |
| Run command (with pipes) | `shell` |
| Bootstrap (no Python) | `raw` |
| Create user | `user` |
| HTTP request | `uri` |
| Print message | `debug` |
| Set variable | `set_fact` |
| Gather system info | `setup` |

---

> 💡 **Interview Tip:** For every Ansible topic, know **what it does**, **when to use it**, and **when NOT to use it**. That shows real operational experience.

> 🌟 **Golden Rule:** Ansible automation should be **idempotent**, **version-controlled**, and **tested before production**.

---

*📘 Prepared for DevOps engineers appearing in Ansible interviews — 2025 edition.*
