# 📂 Filesystem, Commands, and Editors

## 1. Linux Filesystem Concepts

Linux uses a single root filesystem represented by `/`. This is different from Windows, which uses drive letters. Everything in Linux is arranged under that root hierarchy.

### Important directories

| Directory | Purpose |
|---|---|
| `/` | Root of the entire filesystem |
| `/etc` | Configuration files |
| `/home` | User home directories |
| `/var` | Logs, spool, temporary state |
| `/tmp` | Temporary files |
| `/usr` | Applications and libraries |
| `/proc` | Virtual kernel/process information |
| `/dev` | Device files |
| `/boot` | Boot loader and kernel files |

### Absolute vs relative paths

```bash
/home/alice/report.txt        # absolute path
reports/report.txt           # relative path
./reports/report.txt         # current directory
../reports/report.txt        # parent directory
~                             # current user's home directory
```

## 2. File and Directory Management

Linux treats files, directories, sockets, devices, and links as filesystem objects. Understanding how to create, edit, move, copy, and remove these objects is essential.

### Create files and directories

```bash
touch file.txt
echo "Hello" > file.txt
echo "Hello" >> file.txt
mkdir -p /opt/app/logs
mkdir dir1 dir2 dir3
```

### Copy, move, rename, and delete

```bash
cp file.txt backup.txt
cp -r mydir/ backup/
mv file.txt newname.txt
mv file.txt /opt/app/
rm file.txt
rm -rf mydir/
rmdir emptydir
```

> `rm -rf` is dangerous and should be used carefully because it can delete data permanently.

## 3. Viewing and Searching Files

```bash
cat file.txt
cat -n file.txt
head file.txt
tail file.txt
tail -f /var/log/syslog
less file.txt
more file.txt
```

### Search files and content

```bash
find /home -name "*.txt"
find /var/log -name "*.log"
find / -user alice -type f 2>/dev/null
which python3
whereis nginx
type ls
```

`find` is the most powerful file search utility. It can search by filename, size, owner, permission, and modification time.

## 4. Compression and Archives

Linux commonly uses compression tools for backup and redistribution.

### gzip / gunzip

```bash
gzip file.txt
gzip -k file.txt
gunzip file.txt.gz
```

### zip / unzip

```bash
zip archive.zip file1 file2
zip -r archive.zip directory/
unzip archive.zip
```

### tar

```bash
tar -cvf archive.tar files/
tar -cvzf archive.tar.gz files/
tar -xvf archive.tar
tar -xvzf archive.tar.gz
tar -tvf archive.tar
```

`tar` is one of the most important Linux archive tools. It is widely used for backup and software packaging.

## 5. Hard Links and Symbolic Links

### Hard link

A hard link points to the same inode as the original file. It is another name for the same underlying file.

```bash
ln file.txt hardlink.txt
ls -li file.txt hardlink.txt
```

### Symbolic link

A symbolic link is a pointer to another path. It behaves like a shortcut.

```bash
ln -s /etc/nginx/nginx.conf ~/nginx.conf
ls -l ~/nginx.conf
```

### Key difference

- Hard links share the same inode and cannot span filesystems.
- Symlinks are more flexible and can point across filesystems.

## 6. Vi / Vim Editor

Vim is one of the most important editors in Linux administration. System configuration files are often edited using `vi` or `vim`.

### Modes

- Normal mode: navigate and issue commands
- Insert mode: type and edit text
- Command mode: save, quit, search, and replace

### Common commands

```bash
vim file.txt
# i -> insert mode
# Esc -> return to normal mode
# :w -> save
# :q -> quit
# :wq -> save and quit
# :q! -> quit without saving
```

### Useful shortcuts

```text
0        -> start of line
$        -> end of line
gg       -> first line
G        -> last line
x        -> delete character
dd       -> delete line
yy       -> copy line
p        -> paste
u        -> undo
Ctrl+r   -> redo
/search  -> search forward
:%s/old/new/g -> replace globally
```

## 7. Text Processing Tools

### grep

```bash
grep "error" /var/log/syslog
grep -i "error" /var/log/syslog
grep -n "error" file.txt
grep -v "info" file.log
```

### awk

```bash
awk '{print $1}' file.txt
awk -F: '{print $1}' /etc/passwd
awk '$3 >= 1000 {print $1}' /etc/passwd
```

### sed

```bash
sed 's/old/new/' file.txt
sed -i 's/old/new/g' file.txt
sed '/^#/d' file.txt
sed -n '5,10p' file.txt
```

## 8. Hidden Files and Aliases

Files and directories that begin with a dot are hidden.

```bash
ls -a
ls -la
touch .myhiddenfile
mkdir .myhiddendir
```

Aliases are shortcuts for commands.

```bash
alias ll='ls -alF'
alias ..='cd ..'
alias grep='grep --color=auto'
```

Aliases can be made permanent by adding them to `~/.bashrc`.

## 9. Practical Labs

- Create directories, files, and subdirectories and practice moving them around.
- Compare the behavior of hard links and symbolic links.
- Edit a file with `vim`, save it, and reopen it.
- Search logs with `grep` and inspect specific lines with `tail` and `head`.
- Create an archive with `tar` and extract it into another folder.
