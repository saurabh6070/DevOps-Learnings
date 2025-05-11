Problem Statement 1. Based on what you have learnt in the class, do the following steps: <br>
a. Create a new deployment of Ansible cluster of 5 nodes  <br>
b. Label 2 nodes as test and other 2 as prod  <br>
c. Install Java on test nodes  <br>
d. Install MySQL server on prod nodes Use Ansible roles for the above and group the hosts under test and prod.  <br>

Do the above tasks using Ansible Playbooks. <br> <br>


**Solution :-**  <br>

**Commands for the solution :** <br>

Step 1:-	Create ansible-hosts file for test and prod. <br>

    ubuntu@ip-172-31-26-177:~/Ansible-Playbook$ cat /etc/ansible/hosts | tail -7
    [test]
    test1 ansible_host=172.31.26.17
    test2 ansible_host=172.31.19.37
    [prod]
    prod1 ansible_host=172.31.21.231
    prod2 ansible_host=172.31.29.87

![image](https://github.com/user-attachments/assets/b739eea2-0806-42f5-bbfa-b8d18ba8240d)

Step 2:-	Create roles for java and mysql

    Master #ansible-galaxy init roles/java
    Master #ansible-galaxy init roles/mysql

![image](https://github.com/user-attachments/assets/b9a499e5-9306-488a-9477-a11515d974d8)

Step 3:-	Add tasks in role created for java and mysql

    ubuntu@ip-172-31-26-177:~/Ansible-Playbook$ cat roles/mysql/tasks/main.yml
    ---
    # tasks file for roles/mysql
    - name: Install MySQL Server
      apt:
        name: mysql-server
        state: present
        update_cache: yes
    
    - name: Ensure MySQL service is started and enabled
      service:
        name: mysql
        state: started
        enabled: yes
    
    ubuntu@ip-172-31-26-177:~/Ansible-Playbook$ cat roles/java/tasks/main.yml
    ---
    # tasks file for roles/java

    - name: Install OpenJDK 11
      apt:
        name: openjdk-11-jdk
        state: present
        update_cache: yes
    
    
![image](https://github.com/user-attachments/assets/1dd95dc6-238b-419a-848d-d48aa5a8e772)

Step 4:-	Create Playbook

    ubuntu@ip-172-31-26-177:~/Ansible-Playbook$ cat task5.yml
    ---
    - name: Install Java on test nodes
      hosts: test
      become: yes
      roles:
        - java

    - name: Install MySQL on prod nodes
      hosts: prod
      become: yes
      roles:
        - mysql

![image](https://github.com/user-attachments/assets/3e313995-239a-449d-a635-cc3c6fb54fb4)

Step 5:-	Run Playbook

    ubuntu@ip-172-31-26-177:~/Ansible-Playbook$ ansible-playbook task5.yml

![image](https://github.com/user-attachments/assets/6093ab73-ee0e-44c1-9ea4-0ff7732af758)

![image](https://github.com/user-attachments/assets/259c1d8a-a0b6-47c9-b377-cfdd1bf44228)
