Logging using Callback Plugins <br>  <br> 

Ansible offers several callback plugins for logging, each with unique use cases. <br> 
Here are some examples: <br> <br> 

1. log_plays Callback Plugin <br> 
Use Case: Logs playbook events to a file. <br>  <br> 

Configuration: Enable the plugin in ansible.cfg: <br> 

        [defaults]
        stdout_callback = yaml
        callbacks_enabled = log_plays

        [callback_log_plays]
        log_folder = /tmp/ansible/logs
 <br> 
Example: Logs each playbook event to /tmp/ansible/logs. <br>  <br> 


2. ara_default Callback Plugin <br> 
Use Case: Records playbook execution data and sends it to the ARA API. <br>  <br> 

Configuration: Enable the plugin by setting the ANSIBLE_CALLBACK_PLUGINS environment variable or in ansible.cfg: <br> 
  
        [defaults]
        callbacks_enabled = ara_default

 <br> 
Example: Integrates with ARA to provide detailed playbook execution reports. <br>  <br> 


3. mail Callback Plugin <br> 
Use Case: Sends email notifications on playbook failures. <br>  <br> 

Configuration: Enable the plugin in ansible.cfg: <br> 

        [defaults]
        callbacks_enabled = mail

        [callback_mail]
        mail_host = smtp.example.com
        mail_port = 587
        mail_user = user@example.com
        mail_password = password
        mail_to = admin@example.com


Example: Sends an email to admin@example.com if a playbook fails. <br>  <br> 


4. timer Callback Plugin <br> 
Use Case: Logs the duration of playbook execution. <br>  <br> 

Configuration: Enable the plugin in ansible.cfg: <br> 

        [defaults]
        callbacks_enabled = timer

Example: Logs the start and end time of each playbook run. <br>  <br> 


5. profile_tasks Callback Plugin <br> 
Use Case: Profiles the execution time of each task. <br>  <br> 

Configuration: Enable the plugin in ansible.cfg: <br> 

        [defaults]
        callbacks_enabled = profile_tasks
        
Example: Provides detailed timing information for each task in the playbook. <br>  <br> 


6. Combining Multiple Callback Plugins <br> 
You can enable multiple callback plugins simultaneously to leverage their combined functionality. <br> 
For example: <br>  <br> 

Running the Playbook <br> 
Execute your playbook with the configured callback plugins: <br> 

        [defaults]
        stdout_callback = yaml
        callbacks_enabled = log_plays, timer, profile_tasks

 <br>  <br> 
These callback plugins enhance Ansible's logging capabilities, providing valuable insights and notifications during playbook execution.
