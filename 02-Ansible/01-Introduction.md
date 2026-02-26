# 🤖 Ansible — Complete Notes (Beginner to Advanced)

> 🚀 A comprehensive guide to Ansible — covering architecture, playbooks, roles, vault, dynamic inventory, CI/CD integration, and production best practices.

---

## 📌 Table of Contents

| # | Section |
|---|---------|
| 1 | [⚙️ Configuration Management](#1-%EF%B8%8F-configuration-management) |
| 2 | [🤖 What is Ansible?](#2--what-is-ansible) |
| 3 | [🏗️ Ansible Architecture](#3-%EF%B8%8F-ansible-architecture) |
| 4 | [✅ Pre-Requisites](#4--pre-requisites) |
| 5 | [📥 Installing Ansible](#5--installing-ansible) |
| 6 | [📂 Inventory File](#6--inventory-file) |
| 7 | [🔐 Password-less SSH Setup](#7--password-less-ssh-setup) |
| 8 | [⚡ Ad-Hoc Commands](#8--ad-hoc-commands) |
| 9 | [📜 Ansible Playbooks](#9--ansible-playbooks) |
| 10 | [🔢 Variables in Ansible](#10--variables-in-ansible) |
| 11 | [🔍 Ansible Facts](#11--ansible-facts) |
| 12 | [🔀 Conditionals](#12--conditionals) |
| 13 | [🔁 Loops](#13--loops) |
| 14 | [📄 Templates (Jinja2)](#14--templates-jinja2) |
| 15 | [🔐 Ansible Vault](#15--ansible-vault) |
| 16 | [🎭 Ansible Roles](#16--ansible-roles) |
| 17 | [🔔 Handlers](#17--handlers) |
| 18 | [🏷️ Tags in Ansible](#18-%EF%B8%8F-tags-in-ansible) |
| 19 | [🌐 Dynamic Inventory](#19--dynamic-inventory) |
| 20 | [🌌 Ansible Galaxy](#20--ansible-galaxy) |
| 21 | [🖥️ Ansible Tower / AWX](#21-%EF%B8%8F-ansible-tower--awx) |
| 22 | [💥 Error Handling](#22--error-handling) |
| 23 | [🔄 Ansible with CI/CD](#23--ansible-with-cicd) |
| 24 | [🐳 Ansible with Containers](#24--ansible-with-containers) |
| 25 | [📦 Ansible Modules — Deep Dive](#25--ansible-modules--deep-dive) |
| 26 | [🔧 group_vars & host_vars](#26--group_vars--host_vars) |
| 27 | [🚀 Ansible Execution Strategies](#27--ansible-execution-strategies) |
| 28 | [🔍 Debugging in Ansible](#28--debugging-in-ansible) |
| 29 | [🔒 Security Best Practices](#29--security-best-practices) |
| 30 | [✅ Ansible Best Practices](#30--ansible-best-practices) |
| 31 | [⚡ Quick Reference Cheat Sheet](#31--quick-reference-cheat-sheet) |

---

## 1. ⚙️ Configuration Management

**Configuration Management (CM)** is the process of automating the **setup, configuration, maintenance, and consistency** of IT infrastructure at scale.

### Why Configuration Management?

| Problem (Manual) | Solution (CM Tool) |
|------------------|-------------------|
| ❌ Manual errors | ✅ Consistent, automated execution |
| ❌ Configuration drift between servers | ✅ Enforces desired state |
| ❌ Hard to scale to 100s of servers | ✅ Single command manages thousands |
| ❌ Slow provisioning | ✅ Fast, repeatable deployments |
| ❌ No audit trail | ✅ Infrastructure as Code (IaC) |

### Popular Configuration Management Tools

| Tool | Agent? | Language | Push/Pull |
|------|:------:|----------|:---------:|
| **Ansible** | ❌ Agentless | YAML | Push |
| **Chef** | ✅ Agent | Ruby DSL | Pull |
| **Puppet** | ✅ Agent | Puppet DSL | Pull |
| **SaltStack** | Optional | YAML / Python | Both |

> ✅ **Ansible** is the most popular due to its simplicity, agentless nature, and low barrier to entry.

---

## 2. 🤖 What is Ansible?

**Ansible** is an open-source, agentless IT automation tool developed by **Michael DeHaan** and acquired by **Red Hat in 2015**.

📅 **First Released:** 2012

### Core Characteristics

| Property | Description |
|----------|-------------|
| 🚫 **Agentless** | No software to install on managed nodes — uses SSH |
| 📤 **Push-Based** | Master pushes config to slaves (vs. Chef/Puppet which pull) |
| 🔁 **Idempotent** | Running the same playbook multiple times produces the same result |
| 📝 **YAML-Based** | Human-readable configuration language |
| 🐍 **Python-Powered** | Built in Python; modules are Python scripts |
| 📡 **SSH Communication** | Uses standard SSH (port 22) — no extra ports needed |

### 🔁 Why Idempotency Matters

```
Shell Script:  Runs commands repeatedly → can cause errors on re-run
Ansible:       Checks current state → only acts if change is needed
```

**Example:**
```yaml
- name: Install Nginx
  apt:
    name: nginx
    state: present   # If already installed → skips. If not → installs.
```

### 🆚 Ansible vs Shell Scripts

| Factor | Shell Script | Ansible |
|--------|-------------|---------|
| **Idempotency** | ❌ Must code manually | ✅ Built-in |
| **Scale** | ❌ Cumbersome for 100s of servers | ✅ Manages thousands easily |
| **Readability** | Moderate | ✅ Human-readable YAML |
| **Error handling** | Manual | ✅ Built-in |
| **Cross-platform** | Limited | ✅ OS-independent modules |
| **Learning curve** | Low | ✅ Very low |

---

## 3. 🏗️ Ansible Architecture

### 3.1 Core Components

```
┌─────────────────────────────────────────────────────┐
│                  CONTROL NODE (Master)               │
│                                                     │
│  ┌──────────┐  ┌───────────┐  ┌──────────────────┐ │
│  │Inventory │  │ Playbooks │  │ Ansible Config   │ │
│  │(Hosts)   │  │ (YAML)    │  │ (ansible.cfg)    │ │
│  └──────────┘  └───────────┘  └──────────────────┘ │
│                                                     │
│  ┌──────────┐  ┌───────────┐  ┌──────────────────┐ │
│  │ Modules  │  │  Roles    │  │     Vault        │ │
│  └──────────┘  └───────────┘  └──────────────────┘ │
└────────────────────────┬────────────────────────────┘
                         │  SSH (Port 22)
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
   ┌──────────┐   ┌──────────┐   ┌──────────┐
   │  Slave 1 │   │  Slave 2 │   │  Slave 3 │
   │ (Linux)  │   │ (Linux)  │   │ (Windows)│
   └──────────┘   └──────────┘   └──────────┘
```

### 3.2 Component Descriptions

| Component | Description |
|-----------|-------------|
| 🖥️ **Control Node** | The machine where Ansible is installed and playbooks are executed. Cannot be Windows. |
| 🧩 **Managed Nodes** | Target servers (slaves) managed by Ansible. Only need Python + SSH. |
| 📦 **Modules** | Units of work (Python scripts). e.g., `apt`, `yum`, `copy`, `service` |
| 📜 **Playbooks** | YAML files defining automation tasks |
| 📂 **Inventory** | List of managed nodes (static file or dynamic script) |
| 🔌 **Plugins** | Extend Ansible's functionality (connection, callback, lookup) |
| 🔐 **Vault** | Encryption tool for sensitive data |

### 3.3 How Ansible Works (Step by Step)

```
1. 📝 You write a Playbook (YAML)
2. 📋 Ansible reads the Inventory (which servers to target)
3. 🔐 Ansible connects to servers via SSH
4. 📦 Ansible copies & executes Modules (Python scripts) on remote
5. ✅ Results are returned to the Control Node
6. 🧹 Temporary files are cleaned up on the remote
```

---

## 4. ✅ Pre-Requisites

### Control Node Requirements
- Linux/macOS (Windows not supported as control node)
- Python 3.8+
- Ansible installed

### Managed Node Requirements
- Python 2.7+ or Python 3.5+
- SSH access (port 22)
- A user with `sudo` privileges

### Network Requirements

```bash
# Verify SSH connectivity from control node:
ssh user@slave_ip

# Check Python on slave:
python3 --version

# Check port 22 is open (if using AWS EC2, allow in Security Group):
# Inbound rule: TCP port 22 from Control Node IP
```

> 💡 **Windows Managed Nodes** are supported but require **WinRM** instead of SSH.

---

## 5. 📥 Installing Ansible

### 5.1 Ubuntu / Debian

```bash
sudo apt update
sudo apt install software-properties-common -y
sudo add-apt-repository --yes --update ppa:ansible/ansible
sudo apt install ansible -y

# Verify:
ansible --version
```

### 5.2 CentOS / RHEL

```bash
sudo yum install epel-release -y
sudo yum install ansible -y
```

### 5.3 macOS

```bash
brew install ansible
```

### 5.4 Using pip (Universal)

```bash
pip3 install ansible

# Install specific version:
pip3 install ansible==8.0.0
```

### 5.5 Ansible Configuration File

```bash
# Default config location:
/etc/ansible/ansible.cfg

# View active config:
ansible --version    # Shows "config file" path

# Key settings in ansible.cfg:
[defaults]
inventory       = /etc/ansible/hosts
remote_user     = ubuntu
private_key_file = ~/.ssh/id_rsa
host_key_checking = False       # Disable for first-time connections
forks           = 10            # Parallel execution threads
timeout         = 30

[privilege_escalation]
become          = True
become_method   = sudo
become_user     = root
```

---

## 6. 📂 Inventory File

The **inventory** is a file that lists all managed nodes (slaves). Ansible reads this to know which servers to target.

### 6.1 Default Location

```bash
cat /etc/ansible/hosts
```

### 6.2 Basic Inventory Structure

```ini
# Individual hosts:
192.168.1.10
web1.example.com

# Host groups:
[webservers]
web1 ansible_host=192.168.1.101
web2 ansible_host=192.168.1.102

[dbservers]
db1 ansible_host=192.168.1.103
db2 ansible_host=192.168.1.104

# Group of groups:
[all_servers:children]
webservers
dbservers

# Group variables:
[webservers:vars]
http_port=80
ansible_user=ubuntu
```

### 6.3 Host Variables in Inventory

```ini
[webservers]
web1 ansible_host=192.168.1.101 ansible_user=ubuntu ansible_port=22
web2 ansible_host=192.168.1.102 ansible_user=ec2-user
```

### 6.4 YAML Format Inventory

```yaml
all:
  children:
    webservers:
      hosts:
        web1:
          ansible_host: 192.168.1.101
        web2:
          ansible_host: 192.168.1.102
    dbservers:
      hosts:
        db1:
          ansible_host: 192.168.1.103
```

### 6.5 Common Inventory Variables

| Variable | Description |
|----------|-------------|
| `ansible_host` | IP or hostname of the managed node |
| `ansible_port` | SSH port (default: 22) |
| `ansible_user` | SSH user to connect as |
| `ansible_password` | SSH password (use Vault instead!) |
| `ansible_ssh_private_key_file` | Path to SSH private key |
| `ansible_python_interpreter` | Path to Python on remote |
| `ansible_become` | Enable privilege escalation |

### 6.6 Custom Inventory File

```bash
# Use a custom inventory file:
ansible all -i /path/to/my_inventory -m ping

# Or set in ansible.cfg:
[defaults]
inventory = ./inventory/hosts
```

---

## 7. 🔐 Password-less SSH Setup

Ansible relies on **SSH key-based authentication** to connect to managed nodes without a password prompt.

### Step 1 — Generate SSH Key Pair (Control Node)

```bash
ssh-keygen -t rsa -b 4096 -C "ansible-control"
# Press Enter for defaults (saves to ~/.ssh/id_rsa)
```

### Step 2 — Copy Public Key to Managed Node

```bash
ssh-copy-id user@slave_ip

# Example:
ssh-copy-id ubuntu@192.168.1.101
# Enter password once — after this, passwordless SSH works
```

### Step 3 — Verify Passwordless Login

```bash
ssh ubuntu@192.168.1.101
# Should log in without password prompt
```

### Step 4 — Test with Ansible

```bash
ansible all -m ping
# Expected output:
# 192.168.1.101 | SUCCESS => {"ping": "pong"}
```

### Manual Method (Without ssh-copy-id)

```bash
# Copy public key manually:
cat ~/.ssh/id_rsa.pub | ssh user@slave_ip "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"

# Set correct permissions on slave:
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

> 💡 For AWS EC2, use the `.pem` key file:
> ```bash
> ansible all -i inventory --private-key=~/.ssh/my-key.pem -m ping
> ```

---

## 8. ⚡ Ad-Hoc Commands

Ad-hoc commands let you run **one-off tasks instantly** without writing a playbook. Perfect for quick checks, tests, and simple operations.

### Syntax

```bash
ansible <target> -m <module> -a "<arguments>" [options]
```

### 8.1 Connectivity & Info

```bash
# Ping all hosts:
ansible all -m ping

# Ping a specific group:
ansible webservers -m ping

# Run shell command:
ansible all -m shell -a "uptime"
ansible all -m shell -a "df -h"
ansible all -m command -a "hostname"

# Gather facts:
ansible all -m setup
ansible all -m setup -a "filter=ansible_distribution*"
```

### 8.2 Package Management

```bash
# Install package (apt — Ubuntu/Debian):
ansible all -m apt -a "name=nginx state=present" --become

# Install package (yum — RHEL/CentOS):
ansible webservers -m yum -a "name=httpd state=present" --become

# Remove package:
ansible all -m apt -a "name=nginx state=absent" --become

# Update all packages:
ansible all -m apt -a "upgrade=dist update_cache=yes" --become
```

### 8.3 Service Management

```bash
# Start a service:
ansible all -m service -a "name=nginx state=started" --become

# Stop a service:
ansible all -m service -a "name=nginx state=stopped" --become

# Restart a service:
ansible all -m service -a "name=nginx state=restarted" --become

# Enable service on boot:
ansible all -m service -a "name=nginx enabled=yes" --become
```

### 8.4 File & Directory Operations

```bash
# Create a file:
ansible all -m file -a "path=/tmp/test.txt state=touch"

# Create a directory:
ansible all -m file -a "path=/opt/myapp state=directory mode=0755"

# Delete a file:
ansible all -m file -a "path=/tmp/test.txt state=absent"

# Copy a file to remote:
ansible all -m copy -a "src=/local/file.conf dest=/etc/file.conf" --become

# Fetch file from remote:
ansible all -m fetch -a "src=/etc/nginx/nginx.conf dest=/backup/"
```

### 8.5 User Management

```bash
# Create user:
ansible all -m user -a "name=devuser state=present shell=/bin/bash" --become

# Delete user:
ansible all -m user -a "name=devuser state=absent" --become
```

### 8.6 Common Options

| Option | Description |
|--------|-------------|
| `-i <inventory>` | Specify inventory file |
| `-m <module>` | Specify module |
| `-a <args>` | Module arguments |
| `--become` / `-b` | Run with sudo |
| `--become-user=root` | Become specific user |
| `-u <user>` | SSH user |
| `--private-key=<key>` | SSH private key |
| `-f <num>` | Number of parallel forks (default: 5) |
| `-v / -vv / -vvv` | Verbosity level |
| `--check` | Dry run (no actual changes) |
| `--diff` | Show file differences |

> 📌 **Ad-Hoc** = Quick one-time task | **Playbook** = Repeatable, complex automation

---

## 9. 📜 Ansible Playbooks

A **Playbook** is a YAML file that defines a set of automation tasks to be executed on managed nodes. It's the heart of Ansible automation.

### 9.1 Playbook Structure

```yaml
---
- name: Configure Web Server          # Play name (human readable)
  hosts: webservers                   # Target group from inventory
  become: yes                         # Privilege escalation (sudo)
  become_user: root                   # Become this user

  vars:
    http_port: 80
    app_dir: /var/www/html

  tasks:
    - name: Install Nginx             # Task name
      apt:                            # Module
        name: nginx
        state: present
        update_cache: yes

    - name: Start and enable Nginx
      service:
        name: nginx
        state: started
        enabled: yes

    - name: Copy website files
      copy:
        src: ./files/index.html
        dest: /var/www/html/index.html
        mode: '0644'
```

### 9.2 Running a Playbook

```bash
# Basic run:
ansible-playbook playbook.yml

# With custom inventory:
ansible-playbook -i inventory/hosts playbook.yml

# Dry run (check mode):
ansible-playbook playbook.yml --check

# Show file diffs:
ansible-playbook playbook.yml --diff

# Verbose output:
ansible-playbook playbook.yml -v       # level 1
ansible-playbook playbook.yml -vvv     # level 3 (very detailed)

# Run specific tags only:
ansible-playbook playbook.yml --tags "install"

# Skip specific tags:
ansible-playbook playbook.yml --skip-tags "deploy"

# Limit to specific hosts:
ansible-playbook playbook.yml --limit web1

# Ask for sudo password:
ansible-playbook playbook.yml --ask-become-pass
```

### 9.3 Multi-Play Playbook

```yaml
---
- name: Install Web Servers
  hosts: webservers
  become: yes
  tasks:
    - name: Install Nginx
      apt:
        name: nginx
        state: present

- name: Configure Database Servers
  hosts: dbservers
  become: yes
  tasks:
    - name: Install MySQL
      apt:
        name: mysql-server
        state: present
```

### 9.4 Common Modules in Playbooks

| Module | Purpose | Example |
|--------|---------|---------|
| `apt` / `yum` | Package management | Install/remove packages |
| `service` | Service management | Start/stop/enable services |
| `copy` | Copy files | Copy local files to remote |
| `template` | Deploy Jinja2 templates | Dynamic config files |
| `file` | File/directory management | Create/delete files, set permissions |
| `user` | User management | Create/delete users |
| `lineinfile` | Edit file lines | Add/modify specific lines in files |
| `command` / `shell` | Run commands | Execute arbitrary commands |
| `git` | Git operations | Clone/pull repositories |
| `docker_container` | Docker management | Manage containers |
| `uri` | HTTP requests | API calls, health checks |
| `debug` | Print messages | Output variable values |
| `set_fact` | Set variables | Define computed variables |
| `include_tasks` | Include task files | Modular task files |

---

## 10. 🔢 Variables in Ansible

Variables make playbooks **dynamic and reusable**. Ansible supports multiple ways to define and use variables.

### 10.1 Inline Variables (in playbook)

```yaml
---
- name: Deploy Application
  hosts: webservers
  vars:
    app_name: "myapp"
    app_version: "2.1.0"
    app_dir: "/opt/{{ app_name }}"
    http_port: 8080

  tasks:
    - name: Create app directory
      file:
        path: "{{ app_dir }}"
        state: directory
```

### 10.2 External Variable Files

```yaml
# vars/app_vars.yml
app_name: myapp
db_host: 192.168.1.103
db_port: 5432
```

```yaml
# playbook.yml
---
- name: Deploy App
  hosts: webservers
  vars_files:
    - vars/app_vars.yml
  tasks:
    - name: Connect to DB at {{ db_host }}:{{ db_port }}
      debug:
        msg: "Connecting to {{ db_host }}"
```

### 10.3 Command-Line Variables (Extra Vars)

```bash
# Pass variables at runtime:
ansible-playbook playbook.yml -e "env=production version=2.1"
ansible-playbook playbook.yml --extra-vars "app_port=9090"

# From a JSON file:
ansible-playbook playbook.yml -e "@vars.json"
```

### 10.4 Registered Variables

Capture the output of a task for use in subsequent tasks.

```yaml
- name: Check disk space
  command: df -h
  register: disk_output

- name: Print disk info
  debug:
    msg: "{{ disk_output.stdout }}"

- name: Show return code
  debug:
    msg: "Exit code: {{ disk_output.rc }}"
```

### 10.5 Variable Precedence (Lowest to Highest)

```
1.  Command line values (e.g., -u user)
2.  Role defaults (defaults/main.yml)
3.  Inventory file variables
4.  Inventory group_vars/all
5.  Playbook group_vars/all
6.  Inventory host_vars
7.  Playbook host_vars
8.  Host facts (gathered by setup module)
9.  Play vars
10. Play vars_prompt
11. Play vars_files
12. Role vars (vars/main.yml)
13. Block vars
14. Task vars
15. include_vars
16. set_facts / registered vars
17. ✅ Extra vars (-e) — HIGHEST PRIORITY
```

---

## 11. 🔍 Ansible Facts

**Facts** are system information automatically gathered by Ansible from managed nodes at the start of every playbook run using the `setup` module.

### 11.1 View All Facts

```bash
# Ad-hoc:
ansible all -m setup

# Filter facts:
ansible all -m setup -a "filter=ansible_distribution*"
ansible all -m setup -a "filter=ansible_memory_mb"
```

### 11.2 Common Facts

| Fact | Description | Example Value |
|------|-------------|--------------|
| `ansible_hostname` | Hostname of managed node | `web1` |
| `ansible_fqdn` | Fully qualified domain name | `web1.example.com` |
| `ansible_os_family` | OS family | `Debian`, `RedHat` |
| `ansible_distribution` | OS name | `Ubuntu`, `CentOS` |
| `ansible_distribution_version` | OS version | `22.04` |
| `ansible_architecture` | CPU architecture | `x86_64` |
| `ansible_processor_cores` | Number of CPU cores | `4` |
| `ansible_memtotal_mb` | Total RAM in MB | `8192` |
| `ansible_default_ipv4.address` | Primary IP address | `192.168.1.101` |
| `ansible_interfaces` | List of network interfaces | `['eth0', 'lo']` |
| `ansible_python_version` | Python version | `3.10.6` |

### 11.3 Using Facts in Playbooks

```yaml
- name: Print system info
  debug:
    msg: "Running {{ ansible_distribution }} {{ ansible_distribution_version }} on {{ ansible_hostname }}"

- name: Install correct package for OS
  package:
    name: "{{ 'apache2' if ansible_os_family == 'Debian' else 'httpd' }}"
    state: present
```

### 11.4 Custom Facts

You can create your own facts on managed nodes:

```bash
# On managed node, create a facts file:
mkdir -p /etc/ansible/facts.d
cat > /etc/ansible/facts.d/myapp.fact << EOF
[application]
version=2.1.0
environment=production
EOF
```

```yaml
# Access in playbook:
- debug:
    msg: "App version: {{ ansible_local.myapp.application.version }}"
```

### 11.5 Disabling Fact Gathering

```yaml
- name: Fast playbook (skip fact gathering)
  hosts: all
  gather_facts: no      # Speeds up playbook when facts not needed
  tasks:
    - name: Quick task
      command: echo "hello"
```

---

## 12. 🔀 Conditionals

**Conditionals** control whether a task executes based on a condition using the `when` keyword.

### 12.1 Basic when

```yaml
- name: Install Apache on Debian systems
  apt:
    name: apache2
    state: present
  when: ansible_os_family == "Debian"

- name: Install Apache on RedHat systems
  yum:
    name: httpd
    state: present
  when: ansible_os_family == "RedHat"
```

### 12.2 Multiple Conditions

```yaml
# AND condition:
- name: Task runs only on Ubuntu 22.04
  debug:
    msg: "Ubuntu 22.04 detected"
  when:
    - ansible_distribution == "Ubuntu"
    - ansible_distribution_version == "22.04"

# OR condition:
- name: Task runs on Ubuntu or Debian
  apt:
    name: nginx
    state: present
  when: ansible_distribution == "Ubuntu" or ansible_distribution == "Debian"
```

### 12.3 Conditionals with Registered Variables

```yaml
- name: Check if Nginx is installed
  command: nginx -v
  register: nginx_check
  ignore_errors: yes

- name: Install Nginx only if not present
  apt:
    name: nginx
    state: present
  when: nginx_check.rc != 0
```

### 12.4 Conditionals with Variables

```yaml
vars:
  env: "production"
  deploy_app: true

tasks:
  - name: Deploy only in production
    copy:
      src: app.tar.gz
      dest: /opt/app/
    when: env == "production" and deploy_app

  - name: Run only if variable is defined
    debug:
      msg: "{{ my_var }}"
    when: my_var is defined

  - name: Run only if list is not empty
    debug:
      msg: "List has items"
    when: my_list | length > 0
```

---

## 13. 🔁 Loops

**Loops** allow you to repeat a task with different values, avoiding repetitive code.

### 13.1 Basic Loop (loop)

```yaml
# Install multiple packages:
- name: Install required packages
  apt:
    name: "{{ item }}"
    state: present
  loop:
    - nginx
    - git
    - curl
    - vim
    - python3
```

### 13.2 Loop with Dictionaries

```yaml
- name: Create multiple users
  user:
    name: "{{ item.name }}"
    shell: "{{ item.shell }}"
    groups: "{{ item.groups }}"
    state: present
  loop:
    - { name: "alice", shell: "/bin/bash", groups: "sudo" }
    - { name: "bob",   shell: "/bin/sh",   groups: "docker" }
    - { name: "carol", shell: "/bin/bash", groups: "www-data" }
```

### 13.3 Loop with Files

```yaml
- name: Copy multiple config files
  copy:
    src: "{{ item.src }}"
    dest: "{{ item.dest }}"
    mode: "{{ item.mode }}"
  loop:
    - { src: "nginx.conf",  dest: "/etc/nginx/nginx.conf",      mode: "0644" }
    - { src: "app.conf",    dest: "/etc/nginx/sites-available/", mode: "0644" }
```

### 13.4 Loop with Index

```yaml
- name: Print items with index
  debug:
    msg: "Item {{ index }}: {{ item }}"
  loop:
    - apple
    - banana
    - cherry
  loop_control:
    index_var: index
```

### 13.5 with_items (Legacy — still works)

```yaml
# Old syntax (still valid, use loop for new playbooks):
- name: Install packages
  apt:
    name: "{{ item }}"
    state: present
  with_items:
    - nginx
    - git
```

### 13.6 Looping over Registered Variable

```yaml
- name: Get list of files
  find:
    paths: /tmp
    patterns: "*.log"
  register: log_files

- name: Delete old log files
  file:
    path: "{{ item.path }}"
    state: absent
  loop: "{{ log_files.files }}"
```

---

## 14. 📄 Templates (Jinja2)

**Templates** allow dynamic configuration file generation using **Jinja2** templating engine. Template files use the `.j2` extension.

### 14.1 Why Templates?

Instead of static config files, templates let you:
- Inject variables into config files
- Generate environment-specific configs
- Reuse one template for dev/staging/production

### 14.2 Creating a Template

```jinja2
# templates/nginx.conf.j2

server {
    listen {{ http_port }};
    server_name {{ server_name }};

    location / {
        root {{ web_root }};
        index index.html;
    }

    # Environment: {{ environment }}
    # Generated by Ansible on {{ ansible_date_time.date }}
}
```

### 14.3 Using template Module

```yaml
- name: Deploy Nginx config from template
  template:
    src: templates/nginx.conf.j2
    dest: /etc/nginx/sites-available/default
    owner: root
    group: root
    mode: '0644'
  vars:
    http_port: 80
    server_name: "{{ ansible_fqdn }}"
    web_root: /var/www/html
    environment: production
  notify: Restart Nginx
```

### 14.4 Jinja2 Syntax Reference

```jinja2
{# Comment — not rendered #}

{# Variable substitution: #}
{{ variable_name }}
{{ ansible_hostname }}

{# Filters: #}
{{ my_var | upper }}                   {# Uppercase #}
{{ my_var | lower }}                   {# Lowercase #}
{{ my_var | default("fallback") }}     {# Default value #}
{{ my_list | join(", ") }}             {# Join list #}
{{ my_var | replace("old", "new") }}   {# String replace #}

{# Conditionals: #}
{% if environment == "production" %}
  worker_processes auto;
{% else %}
  worker_processes 1;
{% endif %}

{# Loops: #}
{% for host in groups['webservers'] %}
  server {{ hostvars[host]['ansible_host'] }};
{% endfor %}
```

### 14.5 Template Use Cases

| Use Case | Template File |
|----------|--------------|
| Nginx/Apache virtual host | `nginx.conf.j2` |
| Application config | `app.properties.j2` |
| Database config | `my.cnf.j2` |
| Systemd service file | `myapp.service.j2` |
| SSH config | `sshd_config.j2` |
| Prometheus config | `prometheus.yml.j2` |

---

## 15. 🔐 Ansible Vault

**Ansible Vault** encrypts sensitive data (passwords, API keys, certificates) stored in YAML files, keeping secrets out of version control.

### 15.1 Create an Encrypted File

```bash
ansible-vault create secrets.yml
# Prompts for vault password, then opens editor
# Add your secrets:
# db_password: SuperSecret123
# api_key: abc123xyz
```

### 15.2 Edit Encrypted File

```bash
ansible-vault edit secrets.yml
```

### 15.3 View Encrypted File

```bash
ansible-vault view secrets.yml
```

### 15.4 Encrypt / Decrypt Existing Files

```bash
# Encrypt an existing file:
ansible-vault encrypt vars/secrets.yml

# Decrypt a file:
ansible-vault decrypt vars/secrets.yml

# Re-key (change vault password):
ansible-vault rekey secrets.yml
```

### 15.5 Encrypt a Single String

```bash
ansible-vault encrypt_string 'MySecretPassword' --name 'db_password'
# Output:
# db_password: !vault |
#   $ANSIBLE_VAULT;1.1;AES256
#   38633...
```

### 15.6 Using Vault in Playbooks

```yaml
# vars/secrets.yml (encrypted)
# db_password: !vault | ...

---
- name: Deploy with secrets
  hosts: dbservers
  vars_files:
    - vars/secrets.yml      # Encrypted file
    - vars/app_vars.yml     # Plain file

  tasks:
    - name: Configure DB password
      template:
        src: my.cnf.j2
        dest: /etc/mysql/my.cnf
```

### 15.7 Running Playbook with Vault

```bash
# Method 1: Prompt for password:
ansible-playbook playbook.yml --ask-vault-pass

# Method 2: Use a password file:
echo "MyVaultPassword" > ~/.vault_pass
chmod 600 ~/.vault_pass
ansible-playbook playbook.yml --vault-password-file ~/.vault_pass

# Method 3: Set in ansible.cfg:
[defaults]
vault_password_file = ~/.vault_pass
```

> 🔐 **Best Practice:** Never commit vault password files to Git. Add them to `.gitignore`.

---

## 16. 🎭 Ansible Roles

**Roles** provide a way to organize playbooks into **reusable, shareable units** with a standardized directory structure.

### 16.1 Role Directory Structure

```
roles/
└── webserver/
    ├── tasks/
    │   └── main.yml        ← Main task list
    ├── handlers/
    │   └── main.yml        ← Event-driven handlers
    ├── templates/
    │   └── nginx.conf.j2   ← Jinja2 templates
    ├── files/
    │   └── index.html      ← Static files to copy
    ├── vars/
    │   └── main.yml        ← Role-specific variables (high precedence)
    ├── defaults/
    │   └── main.yml        ← Default variables (low precedence, overridable)
    ├── meta/
    │   └── main.yml        ← Role metadata, dependencies
    └── README.md
```

### 16.2 Create a Role

```bash
# Automatically creates the directory structure:
ansible-galaxy role init webserver
```

### 16.3 Role Tasks (tasks/main.yml)

```yaml
---
- name: Install Nginx
  apt:
    name: nginx
    state: present
    update_cache: yes

- name: Deploy Nginx config
  template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
  notify: Restart Nginx

- name: Ensure Nginx is started
  service:
    name: nginx
    state: started
    enabled: yes
```

### 16.4 Role Defaults (defaults/main.yml)

```yaml
---
# Overridable defaults
http_port: 80
https_port: 443
server_name: localhost
web_root: /var/www/html
```

### 16.5 Role Handlers (handlers/main.yml)

```yaml
---
- name: Restart Nginx
  service:
    name: nginx
    state: restarted

- name: Reload Nginx
  service:
    name: nginx
    state: reloaded
```

### 16.6 Using Roles in a Playbook

```yaml
---
- name: Configure Web Servers
  hosts: webservers
  become: yes
  roles:
    - webserver           # Use the role
    - { role: ssl, when: enable_ssl }   # Conditional role

- name: Configure DB Servers
  hosts: dbservers
  become: yes
  roles:
    - common
    - mysql
```

### 16.7 Role Dependencies (meta/main.yml)

```yaml
---
dependencies:
  - role: common
  - role: firewall
    vars:
      allowed_ports:
        - 80
        - 443
```

---

## 17. 🔔 Handlers

**Handlers** are special tasks that run **only when notified** by another task. They run at the **end of the play** and only **once**, regardless of how many times they are notified.

### 17.1 Define and Trigger Handlers

```yaml
---
- name: Configure Web Server
  hosts: webservers
  become: yes

  tasks:
    - name: Install Nginx
      apt:
        name: nginx
        state: present

    - name: Deploy Nginx config
      template:
        src: nginx.conf.j2
        dest: /etc/nginx/nginx.conf
      notify: Restart Nginx         # Trigger handler if config changes

    - name: Deploy SSL certificate
      copy:
        src: cert.pem
        dest: /etc/ssl/certs/cert.pem
      notify:
        - Restart Nginx             # Can notify multiple handlers
        - Send deployment alert

  handlers:
    - name: Restart Nginx
      service:
        name: nginx
        state: restarted

    - name: Send deployment alert
      uri:
        url: "https://hooks.slack.com/services/XXXXX"
        method: POST
        body: '{"text": "Nginx restarted on {{ inventory_hostname }}"}'
```

### 17.2 Handler Behavior

| Behavior | Description |
|----------|-------------|
| ✅ Runs at end of play | Not immediately when notified |
| ✅ Runs once only | Even if notified 10 times in one play |
| ✅ Only if notified | Skipped if the triggering task reports no change |
| ✅ Order guaranteed | Run in order they are defined |

### 17.3 Force Handlers to Run Immediately

```yaml
- name: Deploy config
  template:
    src: app.conf.j2
    dest: /etc/app/app.conf
  notify: Restart App

- name: Flush handlers now
  meta: flush_handlers     # Run all pending handlers at this point

- name: Run health check
  uri:
    url: http://localhost:8080/health
```

---

## 18. 🏷️ Tags in Ansible

**Tags** allow you to run or skip **specific parts** of a playbook without running the entire thing.

### 18.1 Adding Tags

```yaml
tasks:
  - name: Install packages
    apt:
      name: nginx
      state: present
    tags:
      - install
      - packages

  - name: Configure Nginx
    template:
      src: nginx.conf.j2
      dest: /etc/nginx/nginx.conf
    tags:
      - configure
      - nginx

  - name: Start Nginx
    service:
      name: nginx
      state: started
    tags:
      - start
      - services
```

### 18.2 Using Tags When Running Playbooks

```bash
# Run only tasks tagged 'install':
ansible-playbook playbook.yml --tags "install"

# Run multiple tags:
ansible-playbook playbook.yml --tags "install,configure"

# Skip specific tags:
ansible-playbook playbook.yml --skip-tags "start"

# List all tags in a playbook:
ansible-playbook playbook.yml --list-tags
```

### 18.3 Special Tags

```bash
# Run all tasks (including those with 'never' tag):
ansible-playbook playbook.yml --tags "all"

# Always run (even with --tags):
tags: always

# Never run (unless explicitly called):
tags: never
```

---

## 19. 🌐 Dynamic Inventory

**Dynamic Inventory** automatically queries cloud providers or external sources to build the inventory at runtime — instead of a static file.

### 19.1 Static vs Dynamic

| | Static Inventory | Dynamic Inventory |
|--|-----------------|------------------|
| **Source** | Manual `hosts` file | Cloud API / Script |
| **Updates** | Manual edit | Auto-refreshed |
| **Best for** | Small, fixed infrastructure | Cloud, auto-scaling |
| **Format** | INI / YAML file | Python script / Plugin |

### 19.2 AWS EC2 Dynamic Inventory

```bash
# Install AWS inventory plugin:
pip3 install boto3 botocore

# aws_ec2.yml (inventory plugin config):
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
    prefix: aws_region
hostnames:
  - private-ip-address
```

```bash
# Test dynamic inventory:
ansible-inventory -i aws_ec2.yml --list
ansible-inventory -i aws_ec2.yml --graph

# Use with playbook:
ansible-playbook -i aws_ec2.yml playbook.yml
```

### 19.3 GCP Dynamic Inventory

```yaml
# gcp.yml
plugin: google.cloud.gcp_compute
projects:
  - my-gcp-project
regions:
  - us-central1
auth_kind: serviceaccount
service_account_file: /path/to/credentials.json
```

### 19.4 Azure Dynamic Inventory

```bash
pip install azure-cli
# Use azure_rm inventory plugin
```

### 19.5 Custom Dynamic Inventory Script

```python
#!/usr/bin/env python3
# custom_inventory.py
import json

inventory = {
    "webservers": {
        "hosts": ["10.0.1.10", "10.0.1.11"],
        "vars": {"http_port": 80}
    },
    "_meta": {
        "hostvars": {
            "10.0.1.10": {"ansible_user": "ubuntu"},
            "10.0.1.11": {"ansible_user": "ubuntu"}
        }
    }
}

print(json.dumps(inventory))
```

```bash
chmod +x custom_inventory.py
ansible all -i custom_inventory.py -m ping
```

---

## 20. 🌌 Ansible Galaxy

**Ansible Galaxy** is a community hub for sharing, downloading, and reusing Ansible roles and collections.

🔗 https://galaxy.ansible.com

### 20.1 Install a Role

```bash
# Install a role:
ansible-galaxy role install geerlingguy.nginx

# Install specific version:
ansible-galaxy role install geerlingguy.nginx,3.0.0

# Install to a custom path:
ansible-galaxy role install geerlingguy.nginx -p ./roles/

# List installed roles:
ansible-galaxy role list
```

### 20.2 Install from requirements.yml

```yaml
# requirements.yml
roles:
  - name: geerlingguy.nginx
    version: 3.0.0
  - name: geerlingguy.mysql
  - src: https://github.com/myorg/my-role

collections:
  - name: community.general
  - name: amazon.aws
    version: ">=2.0"
```

```bash
ansible-galaxy install -r requirements.yml
```

### 20.3 Collections (Modern Approach)

Collections are the newer format that packages roles, modules, plugins together.

```bash
# Install a collection:
ansible-galaxy collection install community.general
ansible-galaxy collection install amazon.aws

# Use in playbook:
collections:
  - community.general
  - amazon.aws
```

### 20.4 Create and Publish Your Own Role

```bash
# Initialize:
ansible-galaxy role init my_custom_role

# Build and publish to Galaxy:
ansible-galaxy role import github_user repo_name
```

---

## 21. 🖥️ Ansible Tower / AWX

**Ansible Tower** (commercial) and **AWX** (open-source upstream) provide an **enterprise web UI** and API layer on top of Ansible.

### 21.1 Key Features

| Feature | Description |
|---------|-------------|
| 🖥️ **Web UI** | Visual dashboard to run playbooks, view results |
| 👥 **RBAC** | Role-Based Access Control — control who can run what |
| 📅 **Job Scheduling** | Schedule playbooks to run at specific times |
| 🔌 **REST API** | Trigger automation via API from any tool |
| 📊 **Audit Logging** | Full history of who ran what and when |
| 🔐 **Credential Management** | Securely store SSH keys, cloud credentials |
| 📦 **Inventory Sync** | Auto-sync dynamic inventories |
| 🔔 **Notifications** | Slack, email, webhook alerts on job completion |

### 21.2 AWX Setup (Docker)

```bash
# Install AWX using Docker Compose:
git clone https://github.com/ansible/awx.git
cd awx/tools/docker-compose
make docker-compose
```

### 21.3 Tower vs AWX

| | Ansible Tower | AWX |
|--|--------------|-----|
| **Type** | Commercial (Red Hat) | Open-source |
| **Support** | ✅ Enterprise support | Community |
| **Updates** | Stable, tested releases | Frequent, less stable |
| **Cost** | Paid subscription | Free |

---

## 22. 💥 Error Handling

Production playbooks need robust error handling to prevent partial failures and provide clear feedback.

### 22.1 ignore_errors

```yaml
- name: Try to stop a service (may not exist)
  service:
    name: old-service
    state: stopped
  ignore_errors: yes         # Continue even if this fails
```

### 22.2 failed_when

Define custom failure conditions:

```yaml
- name: Run deployment script
  command: /opt/deploy.sh
  register: deploy_result
  failed_when:
    - deploy_result.rc != 0
    - "'ERROR' in deploy_result.stdout"
```

### 22.3 changed_when

Control when a task is marked as "changed":

```yaml
- name: Check application version
  command: /opt/app --version
  register: app_version
  changed_when: false        # Never mark as changed (read-only operation)

- name: Run idempotent script
  command: /opt/setup.sh
  register: setup_out
  changed_when: "'already configured' not in setup_out.stdout"
```

### 22.4 block / rescue / always

Works like try/catch/finally:

```yaml
tasks:
  - block:
      - name: Try to deploy application
        command: /opt/deploy.sh

      - name: Run health check
        uri:
          url: http://localhost:8080/health
          status_code: 200

    rescue:
      - name: Deployment failed — rollback
        command: /opt/rollback.sh

      - name: Alert on failure
        uri:
          url: "{{ slack_webhook }}"
          method: POST
          body: '{"text": "⚠️ Deployment FAILED on {{ inventory_hostname }}"}'

    always:
      - name: Send completion notification (success or fail)
        debug:
          msg: "Deployment attempt finished on {{ inventory_hostname }}"
```

### 22.5 any_errors_fatal

Stop the entire play if any host fails:

```yaml
- name: Critical update
  hosts: all
  any_errors_fatal: true    # Stop ALL hosts if one fails
  tasks:
    - name: Update kernel
      apt:
        name: linux-image-generic
        state: latest
```

### 22.6 max_fail_percentage

```yaml
- name: Rolling update
  hosts: webservers
  max_fail_percentage: 25   # Stop if more than 25% of hosts fail
  serial: 2                  # Update 2 hosts at a time
  tasks:
    - name: Update application
      command: /opt/update.sh
```

---

## 23. 🔄 Ansible with CI/CD

Ansible integrates seamlessly with CI/CD pipelines to automate deployments.

### 23.1 Ansible with Jenkins

```groovy
// Jenkinsfile
pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/myorg/myapp.git'
            }
        }
        stage('Build') {
            steps {
                sh 'docker build -t myapp:${BUILD_NUMBER} .'
            }
        }
        stage('Deploy with Ansible') {
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
        failure {
            sh 'ansible-playbook rollback.yml'
        }
    }
}
```

### 23.2 Ansible with GitHub Actions

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

      - name: Install Ansible
        run: pip3 install ansible

      - name: Setup SSH Key
        run: |
          mkdir -p ~/.ssh
          echo "${{ secrets.SSH_PRIVATE_KEY }}" > ~/.ssh/id_rsa
          chmod 600 ~/.ssh/id_rsa

      - name: Deploy
        run: |
          ansible-playbook -i inventory/production \
            -e "version=${{ github.sha }}" \
            deploy.yml
        env:
          ANSIBLE_VAULT_PASSWORD: ${{ secrets.VAULT_PASSWORD }}
```

### 23.3 Ansible with GitLab CI

```yaml
# .gitlab-ci.yml
stages:
  - test
  - deploy

deploy_production:
  stage: deploy
  image: python:3.11
  before_script:
    - pip install ansible
    - mkdir -p ~/.ssh
    - echo "$SSH_PRIVATE_KEY" > ~/.ssh/id_rsa
    - chmod 600 ~/.ssh/id_rsa
  script:
    - ansible-playbook -i inventory/production deploy.yml
  only:
    - main
  environment:
    name: production
```

---

## 24. 🐳 Ansible with Containers

### 24.1 Managing Docker with Ansible

```yaml
---
- name: Deploy Docker Application
  hosts: dockerhosts
  become: yes

  tasks:
    - name: Install Docker
      apt:
        name: docker.io
        state: present

    - name: Pull Docker image
      docker_image:
        name: myapp
        tag: "{{ image_tag }}"
        source: pull

    - name: Run container
      docker_container:
        name: myapp
        image: "myapp:{{ image_tag }}"
        state: started
        restart_policy: always
        ports:
          - "8080:8080"
        env:
          DB_HOST: "{{ db_host }}"
          APP_ENV: production
        volumes:
          - /opt/myapp/logs:/app/logs

    - name: Remove old containers
      docker_container:
        name: myapp-old
        state: absent
```

### 24.2 Ansible with Kubernetes

```yaml
---
- name: Deploy to Kubernetes
  hosts: localhost
  gather_facts: no

  tasks:
    - name: Apply Kubernetes manifest
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
            selector:
              matchLabels:
                app: myapp
            template:
              spec:
                containers:
                  - name: myapp
                    image: "myapp:{{ image_tag }}"

    - name: Wait for rollout
      kubernetes.core.k8s_rollout_status:
        name: myapp
        namespace: production
```

---

## 25. 📦 Ansible Modules — Deep Dive

Modules are the building blocks of Ansible. They are **Python scripts** executed on managed nodes.

```bash
# View all installed modules:
ansible-doc -l

# Read module documentation:
ansible-doc apt
ansible-doc service
ansible-doc copy
```

### 25.1 Module Location

```bash
cd /usr/lib/python3/dist-packages/ansible/modules/
ls
```

### 25.2 Important Modules by Category

#### 📦 Package Management
```yaml
# apt (Debian/Ubuntu):
- apt: { name: nginx, state: present, update_cache: yes }

# yum / dnf (RHEL/CentOS):
- yum: { name: httpd, state: latest }

# pip (Python):
- pip: { name: flask, version: "2.0" }

# package (generic — works on any OS):
- package: { name: curl, state: present }
```

#### 🔧 File Operations
```yaml
- file:
    path: /opt/myapp
    state: directory      # touch / directory / absent / link
    owner: www-data
    group: www-data
    mode: '0755'

- copy:
    src: local/file.conf
    dest: /etc/app/file.conf
    backup: yes           # Keep backup of old file

- lineinfile:
    path: /etc/ssh/sshd_config
    regexp: '^PasswordAuthentication'
    line: 'PasswordAuthentication no'
    backup: yes

- replace:
    path: /etc/app.conf
    regexp: 'old_value'
    replace: 'new_value'

- fetch:
    src: /var/log/app.log
    dest: ./logs/{{ inventory_hostname }}/
    flat: no
```

#### 🌐 Network / Web
```yaml
- uri:
    url: https://api.example.com/health
    method: GET
    status_code: 200
    return_content: yes
  register: health_check

- get_url:
    url: https://example.com/file.tar.gz
    dest: /tmp/file.tar.gz
    checksum: "sha256:abc123..."
```

#### ☁️ Cloud
```yaml
# AWS EC2:
- amazon.aws.ec2_instance:
    name: my-server
    key_name: my-keypair
    instance_type: t3.micro
    image_id: ami-0abcdef123456
    region: us-east-1
    state: present
```

---

## 26. 🔧 group_vars & host_vars

**group_vars** and **host_vars** are directories that store variables for groups and individual hosts, keeping variable definitions clean and organized.

### 26.1 Directory Structure

```
inventory/
├── hosts                     # Inventory file
├── group_vars/
│   ├── all.yml               # Variables for ALL hosts
│   ├── webservers.yml        # Variables for webservers group
│   ├── dbservers.yml         # Variables for dbservers group
│   └── webservers/           # Directory style (for large var sets)
│       ├── vars.yml
│       └── vault.yml         # Encrypted secrets for this group
└── host_vars/
    ├── web1.yml              # Variables specific to web1
    └── db1.yml               # Variables specific to db1
```

### 26.2 group_vars/all.yml

```yaml
# group_vars/all.yml — applies to every host
ntp_server: pool.ntp.org
timezone: UTC
admin_email: ops@company.com
log_level: info
```

### 26.3 group_vars/webservers.yml

```yaml
# group_vars/webservers.yml
http_port: 80
https_port: 443
web_root: /var/www/html
max_connections: 1000
```

### 26.4 host_vars/web1.yml

```yaml
# host_vars/web1.yml
ansible_host: 192.168.1.101
ansible_user: ubuntu
http_port: 8080      # Override group var for this specific host
server_role: primary
```

---

## 27. 🚀 Ansible Execution Strategies

### 27.1 Serial Execution (Rolling Updates)

```yaml
- name: Rolling update of web servers
  hosts: webservers
  serial: 2          # Update 2 hosts at a time (safe rolling update)
  tasks:
    - name: Remove from load balancer
      uri:
        url: "{{ lb_url }}/remove/{{ inventory_hostname }}"

    - name: Update application
      apt:
        name: myapp
        state: latest

    - name: Re-add to load balancer
      uri:
        url: "{{ lb_url }}/add/{{ inventory_hostname }}"
```

```yaml
serial: "30%"    # Update 30% of hosts at a time
serial:
  - 1            # Update 1 host first (canary)
  - 5            # Then 5 hosts
  - "50%"        # Then 50% of remaining
```

### 27.2 Execution Strategy Plugin

```yaml
- name: Faster playbook
  hosts: all
  strategy: free          # Each host runs independently (faster)
  # strategy: linear      # Default: all hosts complete each task before next
  tasks:
    - name: Update packages
      apt:
        upgrade: dist
```

### 27.3 Async Tasks

Run long-running tasks asynchronously:

```yaml
- name: Start long backup job
  command: /opt/backup.sh
  async: 3600        # Max time (seconds) to wait
  poll: 30           # Check every 30 seconds (0 = fire and forget)
  register: backup_job

- name: Wait for backup to complete
  async_status:
    jid: "{{ backup_job.ansible_job_id }}"
  register: job_result
  until: job_result.finished
  retries: 60
  delay: 30
```

---

## 28. 🔍 Debugging in Ansible

### 28.1 debug Module

```yaml
- name: Print a message
  debug:
    msg: "Deploying to {{ inventory_hostname }} in {{ environment }}"

- name: Print variable value
  debug:
    var: ansible_default_ipv4.address

- name: Print all variables
  debug:
    var: hostvars[inventory_hostname]
```

### 28.2 Verbosity Levels

```bash
ansible-playbook playbook.yml -v      # Basic output
ansible-playbook playbook.yml -vv     # More detail
ansible-playbook playbook.yml -vvv    # SSH-level debug
ansible-playbook playbook.yml -vvvv   # Connection debug
```

### 28.3 Check Mode (Dry Run)

```bash
# Preview what WOULD happen without making changes:
ansible-playbook playbook.yml --check
ansible-playbook playbook.yml --check --diff   # Show file changes
```

### 28.4 Step Mode

```bash
# Confirm each task before running:
ansible-playbook playbook.yml --step
```

### 28.5 assert Module

Validate conditions and fail with clear messages:

```yaml
- name: Validate variables are set
  assert:
    that:
      - app_version is defined
      - db_host | length > 0
      - http_port | int > 0
    fail_msg: "Required variables are missing!"
    success_msg: "All variables validated ✅"
```

---

## 29. 🔒 Security Best Practices

### 29.1 Always Use Vault for Secrets

```bash
# ❌ Bad — plaintext password in playbook
db_password: SuperSecret123

# ✅ Good — encrypted with Vault
db_password: !vault |
  $ANSIBLE_VAULT;1.1;AES256
  ...
```

### 29.2 Principle of Least Privilege

```yaml
# Only escalate when actually needed:
- name: Read application config (no sudo needed)
  slurp:
    src: /opt/myapp/config.yml
  become: no           # Explicitly no sudo

- name: Restart service (sudo needed)
  service:
    name: myapp
    state: restarted
  become: yes          # Only where required
```

### 29.3 Disable Host Key Checking Carefully

```ini
# ansible.cfg — only disable in trusted, controlled environments:
[defaults]
host_key_checking = False   # Only for dev/testing
```

### 29.4 Use no_log for Sensitive Tasks

```yaml
- name: Set database password
  mysql_user:
    name: appuser
    password: "{{ db_password }}"
  no_log: true         # Prevents password appearing in output/logs
```

### 29.5 Protect Sensitive Data in Output

```yaml
- name: Deploy with credentials
  command: /opt/deploy.sh --token {{ api_token }}
  no_log: true
```

---

## 30. ✅ Ansible Best Practices

### 30.1 Project Structure

```
ansible-project/
├── ansible.cfg                  # Project-level config
├── inventory/
│   ├── production/
│   │   ├── hosts
│   │   ├── group_vars/
│   │   └── host_vars/
│   └── staging/
│       ├── hosts
│       ├── group_vars/
│       └── host_vars/
├── roles/
│   ├── common/
│   ├── webserver/
│   └── database/
├── playbooks/
│   ├── site.yml                 # Master playbook
│   ├── webservers.yml
│   └── databases.yml
├── files/
├── templates/
└── requirements.yml             # Galaxy dependencies
```

### 30.2 Key Best Practices

| ✅ Practice | Why |
|------------|-----|
| Use **Roles** for reusability | Modular, shareable, testable |
| Avoid hardcoding values | Use variables for flexibility |
| Use **group_vars / host_vars** | Clean separation of concerns |
| Use **Vault** for all secrets | Security & compliance |
| Use **Tags** | Run only what you need |
| Use **`--check`** before production | Prevent unintended changes |
| Follow YAML indentation (2 spaces) | Consistent, error-free files |
| Write descriptive task names | Self-documenting automation |
| Use **handlers** for restarts | Efficient, runs once only |
| Pin versions (`state: present` vs `latest`) | Predictable, stable deploys |
| Use `no_log: true` on sensitive tasks | Prevent credential leaks |
| Test roles with **Molecule** | Catch bugs before production |
| Version control everything | Auditability and collaboration |
| Use `ansible-lint` | Catch YAML and logic errors |

### 30.3 Useful Tools

| Tool | Purpose |
|------|---------|
| `ansible-lint` | Linting and best practice checks |
| `Molecule` | Role testing framework |
| `ansible-vault` | Secrets encryption |
| `ansible-doc` | Module documentation |
| `ansible-inventory` | Inspect inventory |
| `yamllint` | YAML syntax validation |
| `AWX / Tower` | Enterprise UI and scheduling |

```bash
# Install development tools:
pip3 install ansible-lint molecule yamllint

# Lint a playbook:
ansible-lint playbook.yml

# Lint all YAML:
yamllint .
```

---

## 31. ⚡ Quick Reference Cheat Sheet

### 📋 Ad-Hoc Commands

| Command | Description |
|---------|-------------|
| `ansible all -m ping` | Test connectivity to all hosts |
| `ansible all -m setup` | Gather facts from all hosts |
| `ansible all -m shell -a "uptime"` | Run shell command |
| `ansible webservers -m apt -a "name=nginx state=present" -b` | Install package |
| `ansible all -m service -a "name=nginx state=restarted" -b` | Restart service |
| `ansible all -m copy -a "src=f.txt dest=/tmp/"` | Copy file |
| `ansible all -m user -a "name=alice state=present" -b` | Create user |

### 📜 Playbook Commands

| Command | Description |
|---------|-------------|
| `ansible-playbook playbook.yml` | Run a playbook |
| `ansible-playbook playbook.yml --check` | Dry run |
| `ansible-playbook playbook.yml --diff` | Show file diffs |
| `ansible-playbook playbook.yml -v` | Verbose output |
| `ansible-playbook playbook.yml --tags "install"` | Run tagged tasks |
| `ansible-playbook playbook.yml --limit web1` | Target one host |
| `ansible-playbook playbook.yml -e "env=prod"` | Extra variables |
| `ansible-playbook playbook.yml --ask-become-pass` | Prompt sudo pass |

### 🔐 Vault Commands

| Command | Description |
|---------|-------------|
| `ansible-vault create secrets.yml` | Create encrypted file |
| `ansible-vault edit secrets.yml` | Edit encrypted file |
| `ansible-vault view secrets.yml` | View encrypted file |
| `ansible-vault encrypt file.yml` | Encrypt existing file |
| `ansible-vault decrypt file.yml` | Decrypt file |
| `ansible-vault rekey secrets.yml` | Change vault password |
| `ansible-vault encrypt_string 'pass' --name 'db_pass'` | Encrypt single string |

### 🌌 Galaxy Commands

| Command | Description |
|---------|-------------|
| `ansible-galaxy role install user.role` | Install a role |
| `ansible-galaxy role list` | List installed roles |
| `ansible-galaxy role init myrole` | Create role scaffold |
| `ansible-galaxy install -r requirements.yml` | Install from requirements |
| `ansible-galaxy collection install community.general` | Install collection |

### 📂 Inventory Commands

| Command | Description |
|---------|-------------|
| `ansible-inventory --list` | Show all inventory |
| `ansible-inventory --graph` | Show inventory tree |
| `ansible-inventory -i hosts --list` | Use custom inventory |
| `ansible all --list-hosts` | List all managed hosts |

---

> 💡 **Tip:** Always run `ansible-playbook playbook.yml --check --diff` before applying changes in production.

> 🌟 **Golden Rule:** Write playbooks that are **idempotent** — safe to run multiple times. This is the foundation of reliable infrastructure automation.

---

*📘 Made with ❤️ for DevOps engineers learning Ansible — from zero to production-ready automation.*
