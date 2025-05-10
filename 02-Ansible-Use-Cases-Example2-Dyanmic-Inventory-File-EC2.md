Dynamic Inventory File

Ansible can interact with EC2 instances based on labels (tags) by dynamically generating inventory and performing tasks on instances that match specific tags.

Steps :-

1. Install the AWS Collection: Ensure you have the amazon.aws collection installed:

       ansible-galaxy collection install amazon.aws

2. Configure AWS Credentials: Set up your AWS credentials in the environment or in the ~/.aws/credentials file:

        [default]
        aws_access_key_id = YOUR_ACCESS_KEY_ID
        aws_secret_access_key = YOUR_SECRET_ACCESS_KEY


3. Create an Inventory File: Use the aws_ec2 inventory plugin to dynamically fetch EC2 instances based on tags and connects to EC2-Instances on Purivate-IP only. Create an inventory file (aws_ec2.yml):

       plugin: amazon.aws.aws_ec2
       regions:
         - us-east-1
       filters:
          tag:Environment: production
          tag:Role: webserver
       hostnames:
          - private_ip_address
       keyed_groups:
          - key: tags.Name
            prefix: tag


4. Configure Group Variables: Create a group variables file (group_vars/tag_production.yml) to specify the SSH private key:

          ansible_ssh_private_key_file: /path/to/your/private_key.pem
          ansible_user: ec2-user


6. Write Your Playbook: Create a playbook (playbook.yml) to perform tasks on instances with specific tags:

       - name: Perform tasks on EC2 instances based on tags
         hosts: tag_production:&tag_webserver
         tasks:
            - name: Install Apache
              ansible.builtin.yum:
                   name: httpd
                   state: present
                   update_cache: yes
              become: yes
            - name: Start Apache service
              ansible.builtin.service:
                   name: httpd
                   state: started
                   enabled: yes

7. Run Your Playbook: Execute the playbook using the dynamic inventory:

        ansible-playbook -i aws_ec2.yml playbook.yml


This setup allows you to filter EC2 instances based on multiple tags and perform tasks on those instances.
