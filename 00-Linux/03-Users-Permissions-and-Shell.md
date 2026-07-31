# 👤 Users, Permissions, and the Shell

## 1. Users and Groups

Linux identifies users with a username and a numeric UID. Groups are identified by a GID. This model is the basis of access control and security.

### UID ranges

- `UID 0` = root
- `UID 1-999` = system users and service accounts
- `UID 1000+` = regular human users

### View user and group information

```bash
whoami
id
id alice
cat /etc/passwd
cat /etc/group
getent passwd alice
getent group developers
```

### Create and manage users

```bash
useradd alice
useradd -m -s /bin/bash alice
passwd alice
usermod -s /bin/zsh alice
usermod -aG sudo alice
userdel -r alice
```

### Manage groups

```bash
groupadd developers
gpasswd -a alice developers
gpasswd -d alice developers
groups alice
newgrp developers
```

## 2. File Permissions and Ownership

Linux permissions are assigned to three categories:

- owner
- group
- others

Example:

```text
-rwxr-xr--
│││││││
││││││└── others
│││││└── group
││││└── owner
│││└── file type
```

### Permission values

| Permission | Symbol | Numeric |
|---|---|---:|
| Read | r | 4 |
| Write | w | 2 |
| Execute | x | 1 |

Common modes:

```bash
chmod 755 script.sh
chmod 644 file.txt
chmod 600 ~/.ssh/id_rsa
chmod 400 private.key
```

### Change ownership

```bash
chown alice file.txt
chown alice:developers file.txt
chgrp developers file.txt
chown -R www-data:www-data /var/www/html/
```

## 3. Special Permissions

### SUID

```bash
chmod u+s /usr/bin/passwd
```

It allows a file to run with the owner’s privileges.

### SGID

```bash
chmod g+s /opt/shared
```

It causes new files in the directory to inherit the directory group.

### Sticky bit

```bash
chmod +t /tmp
```

This is used to prevent users from deleting each other’s files in shared directories.

## 4. ACLs and umask

### ACLs

ACLs extend permission control beyond owner/group/others.

```bash
getfacl file.txt
setfacl -m u:bob:rw file.txt
setfacl -m g:developers:rx /opt/project/
setfacl -b file.txt
```

### umask

`umask` controls the default permissions for newly created files and directories.

```bash
umask
umask 022
umask 027
```

Typical result:

- `umask 022` → files get `644`, directories get `755`
- `umask 027` → files get `640`, directories get `750`

## 5. The Shell and Environment Variables

The shell is the command interpreter that accepts your commands and passes them to the kernel.

### Variables

```bash
name="Alice"
echo $name
echo ${name}
export PATH="$PATH:/opt/myapp/bin"
```

### Important variables

| Variable | Meaning |
|---|---|
| `$HOME` | Current user’s home directory |
| `$PATH` | Command lookup paths |
| `$USER` / `$LOGNAME` | User identity |
| `$PWD` | Current working directory |
| `$SHELL` | Active shell |
| `$HOSTNAME` | Machine name |
| `$?` | Exit status of last command |

## 6. Shell Startup Files

Bash uses profile files at login or when opening a new interactive shell.

### Common files

- `~/.bash_profile`
- `~/.bashrc`
- `~/.bash_logout`
- `~/.profile`

```bash
source ~/.bashrc
. ~/.bashrc
```

### Aliases

```bash
alias ll='ls -alF'
alias ..='cd ..'
alias grep='grep --color=auto'
alias update='sudo apt update && sudo apt upgrade -y'
```

Aliases help make repetitive commands faster, but they should be stored in shell config files for persistence.

## 7. sudo and visudo

`sudo` allows a user to run commands as another user, usually root.

```bash
sudo apt update
sudo -i
sudo -u alice id
sudo !!
```

Use `visudo` instead of editing the sudoers file directly.

```bash
visudo
```

### Example sudoers entry

```text
alice ALL=(ALL) ALL
%developers ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart nginx
```

## 8. Practical Labs

- Create a user and assign them to a group.
- Change permissions of a script and make it executable.
- Compare `chmod 755`, `chmod 644`, `chmod 600`, and `chmod 700`.
- Add an alias in `~/.bashrc` and reload it.
- Practice using `sudo` and inspect `/etc/sudoers.d`.
