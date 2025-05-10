Problem Statement 1. Based on what you have learnt in the class, do the following steps: <br>
a. Setup Ansible cluster with 3 nodes  <br>
b. On slave 1 install Java  <br>
c. On slave 2 install MySQL server  <br>

Do the above tasks using Ansible Playbooks. <br> <br>


**Solution :-**  <br>

**Commands for the solution :** <br>

Step 1:-	Deploy 3 EC2 Instances in AWS.

Step 2:-	Make Passwordless from Master to Slave Nodes (Copy Master Public key in both slave nodes authorized keys) :

Step 3:-	Install ansible in Master node :-

    export PS1="Master #"
    sudo apt update && sudo apt upgrade -y
    sudo apt install -y software-properties-common
    sudo add-apt-repository --yes --update ppa:ansible/ansible
    sudo apt install -y ansible
    ansible –version

Step 4:-	Upgrade Packages in Slave Nodes as well :-

    export PS1="Slave1 #"
    sudo apt update && sudo apt upgrade –y


Step 5:-	Add ansible hosts file in Master with private Ips of Slave Nodes :-

    Master #sudo cat /etc/ansible/hosts| tail -5
    [servers]
    slave1 ansible_host=172.31.30.188
    slave2 ansible_host=172.31.26.170
    #master ansible_host=172.31.26.177

![image](https://github.com/user-attachments/assets/3aafbaa0-4571-4bee-839d-eefa789e2556)


Step 6 :- Create Ansible Playbook :-

    Master #cat task1.yml
    ---
    - name: Install Java on slave1
    hosts: slave1
      tasks:
        - name: Install OpenJDK 11
          apt:
            name: openjdk-11-jdk
            state: present
          become: yes

    - name: Install MySQL on slave2
      hosts: slave2
      tasks:
        - name: Install MySQL server
          apt:
            name: mysql-server
            state: present
          become: yes
        - name: Start MySQL service
          service:
            name: mysql
            state: started
            enabled: yes

![image](https://github.com/user-attachments/assets/40218e5e-f0b3-4951-92d6-660d8b0d46f6)


Step 7 :- Run the playbook

    Master #ansible-playbook task1.yml

![image](https://github.com/user-attachments/assets/47ac4093-7d57-4b0a-8ba7-3ca8be2b1432)


Step 8 :- Check installation on Slave nodes :-

Slave1 :- <br>
![image](https://github.com/user-attachments/assets/c71b5219-27fd-4c79-adfb-b866529b90cc)


Slave2 :- <br>
![image](https://github.com/user-attachments/assets/19a94032-91da-472d-ac17-62bd9a68be22)
