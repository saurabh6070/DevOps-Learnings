Problem Statement 3. Based on what you have learnt in the class, do the following steps: <br>
1. Create 2 Ansible roles  <br> 
2. Install Apache2 on slave1 using one role and NGINX on slave2 using the other role  <br> 
3. Above should be implemented using different Ansible roles <br> 

Do the above tasks using Ansible Playbooks. <br> <br>


**Solution :-**  <br>

**Commands for the solution :** <br>

Step 1:-	Create Roles for nginx and apache

    Master #ansible-galaxy init roles/apache
    Master #ansible-galaxy init roles/nginx

![image](https://github.com/user-attachments/assets/26da2087-6e2d-45c4-9bb2-18b19dfd62c8)

Creating roles using ansible-galaxy creates empty tasks files in respective directories.

Step 2:-	Add tasks in created roles

    Master #cat roles/apache/tasks/main.yml
    ---
    # tasks file for roles/apache
    
    - name: Install Apache2
      apt:
        name: apache2
        state: present
        update_cache: yes
    
    - name: Start and enable Apache2 service
      service:
        name: apache2
        state: started
        enabled: yes
    
    
    Master #cat roles/nginx/tasks/main.yml
    ---
    # tasks file for roles/nginx
    
    - name: Install NGINX
      apt:
        name: nginx
        state: present
        update_cache: yes
    
    - name: Start and enable NGINX service
      service:
        name: nginx
        state: started
        enabled: yes
    
![image](https://github.com/user-attachments/assets/1f979f94-9f29-407d-bbdc-0b03e9d07640)

Step 3:-	Create playbook to use above created roles

    Master #cat task3.yml
    ---
    - name: Install Apache on slave1
      hosts: slave1
      become: yes
      roles:
        - apache
    
    - name: Install NGINX on slave2
      hosts: slave2
      become: yes
      roles:
        - nginx
    
![image](https://github.com/user-attachments/assets/a3679050-74e7-43d2-b0fe-921ad0bf4066)

Step 4:-	Run playbook

    Master #ansible-playbook task3.yml

![image](https://github.com/user-attachments/assets/2713aa8f-dd8a-4f00-b21e-b03c7c3b0465)
