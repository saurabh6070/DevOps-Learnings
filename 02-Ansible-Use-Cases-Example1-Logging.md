Ansible Loggging

Here, we are using two modules namely :- Debug Module & Copy Module.
Debug Module: The ansible.builtin.debug module is used to log messages during playbook execution. The msg parameter specifies the message to log.<br>
Copy Module: The ansible.builtin.copy module is used to write the logged messages to a file (/tmp/playbook.log). The content parameter specifies the message content, and the dest parameter specifies the destination file. The mode: 'a' parameter appends the message to the file.<br><br>

This example demonstrates how to log custom messages to a file during playbook execution using the debug and copy modules.

        - name: Example playbook for logging
          hosts: localhost
          tasks:
            - name: Log a start message                                                                                  // Here, loggin starts but not into a file
              ansible.builtin.debug:                                                                                     // Uses the debug module to log a message.
                msg: "Starting the playbook execution"                                                                   // The message to be logged. 
              register: start_message                                                                                    // Register saves the output of the task in a variable named start_message.            

            - name: Log a custom message to a file                                                                       
              ansible.builtin.copy:                                                                                      // Uses the copy module to write content to a file.
                content: "{{ start_message.msg }}"                                                                       // The content to be written, which is the message stored in start_message.msg.
                dest: /tmp/playbook.log

            - name: Perform a sample task
              ansible.builtin.command:
                cmd: echo "Hello, Ansible!"
              register: sample_task

            - name: Log the result of the sample task
                ansible.builtin.copy:
                  content: "{{ sample_task.stdout }}"
                  dest: /tmp/playbook.log
                  mode: 'a'
