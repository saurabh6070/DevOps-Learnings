1. Static and dynamic inventory file in ansible ?<br>
Ans :- Static means ip for slave nodes are fixed.
       Dynamic means ips for slave nodes are dynamic and can be configured python script to fetch these ips and add in inventory file
<br><br>

2. Ansible components ?<br>
Ans :- Playbooks : contains multiple plays where each play will have some tasks, like install nginx, start and enable nginx in a single block
       Plugin are also modules which are used generally for logging purposes.
       Modules are also present on master node which are written in python for each task category module is written which serves purpose for specific tasks in all OS.
       Copy and recursive two modules which can be used to copy files from master to ansible slave nodes.
<br><br>

3. How To encrypt already present file ?<br>
Ans :-  ansible-vault encrypt test.yml
        ansible-vault decrypt test.yml
<br><br>

4. To create a new encrypted file in ansible ?<br>
Ans :- In each case password will be asked. For setting two time and for decrypting one tIme

        ansible-vault create hello.yml
<br>

5. Default Fork Limit in Ansible ?<br>
Ans :- In Ansible, the fork limit refers to the number of parallel processes that Ansible can use to execute tasks on multiple hosts simultaneously. By default, Ansible uses 5 forks 1 2, but this can be adjusted based on your needs and the capacity of your system.

**Adjusting Fork Limit**
You can change the fork limit in two main ways:

5.1. Configuration File (ansible.cfg): Add or modify the forks parameter in the [defaults] section of your ansible.cfg file:

    [defaults]
    forks = 30

5.2. Command Line: Use the -f or --forks option when running your playbook:

    ansible-playbook -f 30 my_playbook.yml

Note :-
**Considerations**
**System Resources: **Increasing the number of forks can improve performance but also requires more CPU and memory. It's recommended to have 4 GB RAM per 100 forks.
**Task Execution: **More forks mean more tasks can be executed in parallel, which can speed up playbook execution, especially in large environments.
<br><br>

6. Can we have windows node as Ansible Controller node ?<br>
Ans :- No. Only linux machine can be used as controller node in Ansible.
<br><br>

7. Can we have Windows node as a Host node in Ansible. How ansible work with Windows node ?<br>
Ans :- Controller node will be able to connect with Window node using winrm.
<br><br>

8. How ansible work with Linux node ?<br>
Ans :- using SSH
<br><br>

9. What are best practices in ssh-based linux Node ?<br>
Ans :- 	• Establish Passwordless SSH
       	• Avoid using root user on Managed (Slave) Node. Allow using sudo access.
<br><br>
10. How to debug an ansible playbook execution ?<br>
Ans :- To debug an ansible playbook :-
	• Use verbose while running playbook
	
        ansibe-playbook play.yml -vvvv
	 • Debug Module in Ansible can be used to print logs for the task
	Use debug module and register keyword in ansible to write logs for the automation.
<br><br>

11. How to run tasks in ansible playbook with sudo privileges ?<br>
Ans :- Use **become : true** in playbook. Task will be executed with sudo privileges.
<br><br>

12. Default host groups in inventory file ?<br>
Ans :- Two Groups :-
	• All
	• Ungrouped
<br><br>

13. What is the purpose of handlers in Ansible ?<br>
Ans :- Suppose we have a task in ansible to install service of apache and then restart apache. Incase, if Apache is already up and running in slave node, then first step of installing apache will be skipped, but restart of service will be executed.
In this case, Handlers can be useful.
<br><br>

14. Features of Ansible ?<br>
Ans :- Features are :
	• Agentless 
	• Ansible follows push architecture
	• Works over ssh for Linux, and winrm for Windows.
<br><br>

15. Ansible.cfg file all parameters ?<br>
Ans :- The ansible.cfg file is a central configuration file for Ansible, allowing you to customize its behavior. It is structured in sections, each containing various parameters.
       Here are the key sections and some important parameters:
    Key Sections and Parameters
    **[defaults]**
        inventory: Path to your inventory file.
        remote_user: Default user for SSH connections.
        host_key_checking: Whether to check SSH host keys (set to False to disable).
        timeout: SSH connection timeout in seconds.
        retry_files_enabled: Enable/disable retry files.
    **[privilege_escalation]**
        become: Enable privilege escalation (e.g., sudo).
        become_method: Method for privilege escalation (e.g., sudo, su).
        become_user: User to become after privilege escalation.
    **[ssh_connection]**
        ssh_args: Additional SSH arguments.
        control_path: Path for SSH control socket.
        pipelining: Enable/disable pipelining to reduce SSH connections.
    **[paramiko_connection]**
        pipelining: Enable/disable pipelining for Paramiko connections.
    **[inventory]**
        enable_plugins: List of enabled inventory plugins.
    **[logging]**
        log_path: Path to the log file.
        log_format: Format for log messages.

Example :-
          
          [defaults]
          inventory = /path/to/inventory
          remote_user = your_user
          host_key_checking = False
          timeout = 30
          retry_files_enabled = False

          [privilege_escalation]
          become = True
          become_method = sudo
          become_user = root
          
          [ssh_connection]
          ssh_args = -o ControlMaster=auto -o ControlPersist=60s
          control_path = /tmp/ansible-ssh-%%h-%%p-%%r
          pipelining = True
          
          [paramiko_connection]
          pipelining = True
          
          [inventory]
          enable_plugins = host_list, script, yaml, ini, auto
          
          [logging]
          log_path = /var/log/ansible.log
          log_format = %(asctime)s %(levelname)s %(name)s: %(message)s


NOTE :- 
**• Generating a Sample Configuration File**
We can generate a sample ansible.cfg file with all parameters commented out using the ansible-config utility:
      
      ansible-config init --disabled > ansible.cfg
This command creates a fully commented-out example configuration file that we can customize as needed.
<br><br>
