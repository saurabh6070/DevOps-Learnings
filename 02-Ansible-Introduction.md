1. Configuration Management Tool <br>
   1.1 Configuration management tools are essential for automating the setup, maintenance, and consistency of IT infrastructure. They help ensure that systems are configured correctly and consistently, reducing the risk of errors and improving efficiency.<br><br>
   1.2 Ansible is a popular configuration management tool developed by Red Hat.<br><br>
   1.3 Here are some key points about Ansible:<br>
       •  Simplicity and Ease of Use: Ansible uses YAML, a straightforward, human-readable language, to define automation tasks. This makes it accessible to both developers and system administrators.<br>
       •  Agentless Architecture: Unlike some other tools, Ansible does not require any agent software to be installed on the managed nodes. It operates from a control node, pushing commands to the target systems. <br>
       •  Idempotency: Ansible ensures that tasks are idempotent, meaning that running the same task multiple times will not change the system state after the first successful run. <br>
       •  Wide Range of Uses: Ansible can manage systems, applications, servers, storage, and networking devices, making it versatile for various IT environments. <br>
       •  Scalability: It can manage one to hundreds of systems from a central location, making it suitable for both small and large-scale environments.<br><br>


2.1 Ansible - Configuration Management Tool <br>
  •  Released in 2012<br>
  •  Idempotency :- While Shell scripts can be used to execute commands on multiple servers, they lack idempotency. This means that if a command has already been executed on a server, the script will not recognize this and may execute the same command again, such as installing a package. In contrast, Ansible ensures idempotency, meaning it will not re-execute commands that have already been successfully applied.<br>
  •  Large Scale Environments :- Shell scripts are not suitable for large-scale node configuration. Ansible, on the other hand, follows a single master and multiple slave architecture.<br>
  •  Push Based Configuration :- Ansible is a push-based configuration management tool. It is agentless, meaning there is no need to install any agent on the slave nodes for Ansible to manage them.<br> 
<br><br>
2.2 Pre-Requisites<br>
  •  Password-less/Key-based authentication must be established between the Ansible master and slave nodes. Ensure port 22 is open in the Security Group of the EC2 instance.<br>
  •  Python must be installed on both the Ansible master and slave nodes, as Ansible modules (specified with the -m option in commands) are Python-based.<br>
<br><br>
2.3 Setup Ansible Server :-<br>
  •  sudo apt update<br>
  •  sudo apt install software-properties-common<br>
  •  sudo add-apt-repository --yes --update ppa:ansible/ansible<br>
  •  sudo apt install ansible<br>
<br><br>
2.4 Module Path in Ansible Server:-<br>
  2.4.1 Navigate to the directory containing Ansible modules:-
  
    cd /usr/lib/python3/dist-packages/ansible/modules/
  2.4.2 List the modules:-<br>
  
    ls
This command will display all the modules, which are written in Python and are typically large in size.
These Python modules are designed to be compatible with all operating systems.
For example, the user.py file is used for user management and is supported across all operating systems.<br>
<br><br>
2.5 Host-File/ Inventory-File Ansible :-

    cat /etc/ansible/hosts

Example :

    [webservers]
    web1 ansible_host=192.168.1.101
    web2 ansible_host=192.168.1.102
    [dbservers]
    db1 ansible_host=192.168.1.103
    db2 ansible_host=192.168.1.104
    [loadbalancers]
    lb1 ansible_host=192.168.1.105
    [all_servers:children]
    webservers
    dbservers
    loadbalancers
    [webservers:vars]
    http_port=80
    [dbservers:vars]
    db_port=3306
    [loadbalancers:vars]
    lb_port=443<br>
<br><br>
2.6 To set up password-less SSH access between your Ansible server and Ansible slave:
  2.6.1 Generate SSH Key Pair:

    ssh-keygen -t rsa
    
  2.6.2 Follow the prompts to save the key pair in the default location (~/.ssh/id_rsa).
  2.6.3 Navigate to the .ssh Directory:
  2.6.4 List the Contents of the .ssh Directory:
        You should see your newly created id_rsa and id_rsa.pub files.
        Copy the Public Key to the Ansible Slave:
        Replace user with the username on the Ansible slave and ansible_slave_ip with the IP address of the Ansible slave.
  2.6.5 Verify SSH Access:
        You should be able to log in without being prompted for a password.
    These steps ensure that your Ansible server can communicate with the Ansible slave securely and without requiring a password each time.
<br><br>
2.7 Note: <br><br>
  2.7.1 Private-IP to be used for Ansible Master-Slave.<br>
        For AWS EC2-Instance, we can use both Public-IPs or Private-IPs of an instance in Ansible Inventory-File. But it is better to use Private IPs instead of Public IPs. This will be much reliable/ faster/ secure. Also, Public-IP in an EC2-instance will change once EC2 is restarted. But Private-IP will be same even after reboot.
<br><br>
![image](https://github.com/user-attachments/assets/7ba881e3-0f06-4321-8117-8c8b6e49eace)


  2.7.2 Private-Key for SSH connection for Master Slave.<br>
        In Ansible inventory file, we can have private key to login Slave servers instead of setting passwordless ssh access of all the slave nodes.
        Also, if in hosts section of ansible-playbook, it is mentioned as localhost, then it means master node itself(127.0.0.1)

        [webservers]
        slave1 ansible_user=10.10.100.12 ansible_ssh_private_key_file=/path/to/your/private/key ansible_python_interpreter=/usr/bin/python3
<br><br>
2.8 Ansible Variables: <br><br>
  2.8.1 Inline variable : Using variable in same playbook.
        Example :
              
        - name: Inline variable example
          hosts: all
          vars:
          region:
	        -  ap-south-1
	        -  us-east-1
          tasks:
          -	name: Ansible list variable example
            debug:
		        msg: "{{ region[1] }}"

  2.8.2 External variable : Using variable in other playbooks.
        Example :

        - name: Use variables from external file
          region: [ap-south-1, us-east-1]
          hosts: all
          vars_files:
	          - vars/main.yml
          tasks:
          -	name: Ansible list variable example
            debug:
		          msg: "{{ region[1] }}"

  NOTE : Precedence of variables defined in the file will be higher than variable defined in other files.<br>
        **Jinja Temleting:** It means defining code in different variables in different path.
<br><br>
2.9 Ansible Roles: <br>
  2.9.1 Ansible Roles <br>
  	Ansible Roles are self-contained units of automation that can be easily shared and reused. They follow a specific directory structure, making it easy to manage and understand the components involved. <br>
   
  2.9.2 Directory Structure <br>
  	A typical Ansible Role has the following directories: <br>
           •  tasks/: Contains the main list of tasks to be executed. <br>
           •  handlers/: Defines handlers, which are tasks triggered by other tasks. <br>
           •  templates/: Stores templates that can be used with the template module. <br>
           •  files/: Contains files that can be deployed to the managed nodes. <br>
           •  vars/: Defines variables that are used within the role. <br>
           •  defaults/: Sets default variables for the role. <br>
           •  meta/: Provides metadata about the role, including dependencies. <br>

  2.9.3 Using Roles <br>
  	We can use roles in playbooks by including them with the roles directive or by using the include_role or import_role modules. This allows us to modularize playbooks and reuse roles across different projects. <br> 

  2.9.4 Benefits of Using Roles <br>
       •  Reusability: Roles can be reused across multiple playbooks and projects. <br>
       •  Organization: Helps in organizing complex playbooks by breaking them down into smaller, manageable units. <br>
       •  Collaboration: Roles can be shared with others, promoting collaboration and standardization. <br> <br>

2.10 Ansible Handlers: <br>
  2.10.1 Ansible Handlers <br>
  	Ansible Handlers are special tasks that only run when notified by other tasks. They are typically used to perform actions like restarting services, reloading configurations, or any other operations that should only occur if a preceding task makes changes. <br>
   
   2.10.2 How Handlers Work <br>
  	**Notification: **Tasks notify handlers using the notify directive. This means that if a task changes the state of the system, it can trigger a handler to run. <br>
  	**Execution: **Handlers are executed at the end of the play, after all tasks have completed. This ensures that any necessary actions are taken only once, even if multiple tasks notify the same handler. <br>
 
   2.10.3 Benefits of Using Handlers <br>
  	**Efficiency: **Handlers ensure that actions like service restarts only happen once, even if multiple tasks notify the same handler. <br>
	**Order of Execution: **Handlers are executed in the order they are defined, not in the order they are notified. <br>
	**Conditional Execution: **Handlers only run if they are notified by a task that changes the system state. <br> <br>
 
