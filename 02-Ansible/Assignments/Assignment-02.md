Problem Statement 1. Based on what you have learnt in the class, do the following steps: <br>
1. Create a script which can add text “This text has been added by custom script” to /tmp.1.txt  <br>
2. Run this script using Ansible on all the hosts. <br>

Do the above tasks using Ansible Playbooks. <br> <br>


**Solution :-**  <br>

**Commands for the solution :** <br>

Step 1:-	Create script.sh file : <br>

    Master #cat script.sh
    #!/bin/bash	
    echo "This text has been added by custom script" >> /tmp/1.txt

![image](https://github.com/user-attachments/assets/7a81975c-eb55-4430-810c-9f91fd6425a7)

<br> 
 
Step 2:-	Create playbook

    Master #cat task2.yml
    ---
    - name: Add text to /tmp.1.txt on all hosts
      hosts: all
      become: yes
      tasks:
        - name: Copy the script to the hosts
          copy:
            src: script.sh
            dest: /tmp/script.sh
            mode: '0755'
    
        - name: Run the script
          command: /tmp/script.sh
    
        - name: Verify if the text was added
          shell: cat /tmp/1.txt
          register: script_output
    
        - name: Print the script output
          debug:
            var: script_output.stdout


![image](https://github.com/user-attachments/assets/f26407b9-2876-4e14-b6a7-cd5ad4d1f053)



Step 3:-	Run Playbook

    Master #ansible-playbook task2.yml

![image](https://github.com/user-attachments/assets/ab973926-94b3-4c89-8189-dd71cb876c7d)

<br> 
 
Step 4:-	Check manually in slave nodes :-

Slave1 :

![image](https://github.com/user-attachments/assets/0e7eec20-fdd2-47f2-8254-21029ee0f1a9)

<br> 
 

Slave2:

![image](https://github.com/user-attachments/assets/af0500a9-5302-444c-846d-09b2df1dc805)
