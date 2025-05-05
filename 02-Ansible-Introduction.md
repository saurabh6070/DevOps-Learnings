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
    lb_port=443


