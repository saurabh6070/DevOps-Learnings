Problem Statement 1. Based on what you have learnt in the class, do the following steps: <br>
a. Use the previous deployment of Ansible cluster.  <br>
b. Configure the files folder in the role with index.html which should be replaced with the original index.html  <br>
All of the above should only happen on the slave which has NGINX installed using the role. <br>

Do the above tasks using Ansible Playbooks. <br> <br>


**Solution :-**  <br>

**Commands for the solution :** <br>

Step 1:-	Create index.html file in nginx role

    Master #cat roles/nginx/files/index.html
    <!DOCTYPE html>
    <html>
    <head>
        <title>Welcome to Custom NGINX Page</title>
    </head>
    <body>
        <h1>This page was deployed using Ansible!</h1>
    </body>
    </html>


![image](https://github.com/user-attachments/assets/81ca5d84-a388-472b-a420-c01e09e8b968)

 <br>
Step 2:-	Modify existing playbook for nginx

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
    
    - name: Replace default index.html
      copy:
        src: index.html
        dest: /var/www/html/index.html
        owner: www-data
        group: www-data
        mode: '0644'

![image](https://github.com/user-attachments/assets/16eaf04c-0182-441a-a2db-d1113052f3a2)

 <br>
Step 3:-	Run playbook :

    Master #ansible-playbook task3.yml

![image](https://github.com/user-attachments/assets/8e50f2dc-148f-4798-9ac7-6af44cc60ce7)

 <br>
Step 4:-	Verify change

Before running playbook:

![image](https://github.com/user-attachments/assets/8233baaf-213e-46d9-aeb4-f65bce3a2102)

After Running Playbook: 
![image](https://github.com/user-attachments/assets/7d8796f7-8eb5-4799-9124-28f9bdea7dd4)

 <br>
