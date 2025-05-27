1. Initial Configuration Post-Launch
Once EC2 instances are provisioned, you often want to configure them:

ansible.builtin.yum or ansible.builtin.apt – Install packages.

- name: Install Nginx on Amazon Linux
  ansible.builtin.yum:
    name: nginx
    state: present
ansible.builtin.service – Start and enable services.

- name: Start and enable Nginx
  ansible.builtin.service:
    name: nginx
    state: started
    enabled: true


🛠️ 2. System Configuration
Used for managing system settings or files.

ansible.builtin.copy – Copy config files or scripts.

- name: Copy custom nginx config
  ansible.builtin.copy:
    src: files/nginx.conf
    dest: /etc/nginx/nginx.conf
    mode: '0644'


ansible.builtin.lineinfile – Modify lines in config files (like /etc/hosts).

- name: Add entry to /etc/hosts
  ansible.builtin.lineinfile:
    path: /etc/hosts
    line: "10.0.0.1 internal-db"
    state: present


🧑‍💻 3. User and Permission Management
Set up secure access to instances.

ansible.builtin.user – Create user accounts.

- name: Create a new deploy user
  ansible.builtin.user:
    name: deploy
    groups: wheel
    state: present
ansible.builtin.authorized_key – Add SSH keys.

- name: Add SSH key for deploy user
  ansible.builtin.authorized_key:
    user: deploy
    key: "{{ lookup('file', 'keys/deploy.pub') }}"

🗂️ 4. File and Directory Management
ansible.builtin.file – Create directories, set permissions.

- name: Ensure logs directory exists
  ansible.builtin.file:
    path: /var/log/myapp
    state: directory
    owner: deploy
    mode: '0755'

🔄 5. Execution and Orchestration
ansible.builtin.shell or ansible.builtin.command – Run arbitrary commands (carefully).

- name: Run a database migration script
  ansible.builtin.shell: "/opt/myapp/scripts/migrate.sh"

ansible.builtin.wait_for – Wait for ports or files to become available (useful when waiting for services).

- name: Wait for Nginx to be available
  ansible.builtin.wait_for:
    port: 80
    timeout: 30

📜 6. Facts and Inventory Handling
ansible.builtin.setup – Gather EC2 instance facts.

- name: Gather facts
  ansible.builtin.setup:
ansible.builtin.debug – Debug gathered facts or variables.

- name: Show EC2 instance's public IP
  ansible.builtin.debug:
    var: ansible_default_ipv4.address

🧪 Bonus Use-Case: EC2 Health Checks and Configuration Drift Detection
Use ansible.builtin.assert to ensure configurations are as expected.

- name: Ensure Nginx is running
  ansible.builtin.assert:
    that:
      - "'nginx' in ansible_facts.services"
      - "ansible_facts.services['nginx'].state == 'running'"
