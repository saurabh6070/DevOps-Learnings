# Shell, Vim, and Environment Variables

> Extracted from [00-Linux/01-Introduction.md](../01-Introduction.md)
>
> Covers source sections 7-10 from the original Linux introduction note.

## 7. 🐚 Vi / Vim Editor

Text editing is a core part of Linux administration and scripting. Vim is widely used because it is powerful, fast, and available on nearly every Linux system.

### 7.1 Vim Modes

```
Normal Mode     → Default mode. Navigate and issue commands.
Insert Mode     → Type/edit text. Enter with: i, I, a, A, o, O
Command Mode    → Run commands. Enter with: : (colon)
Visual Mode     → Select text. Enter with: v, V, Ctrl+v
```

### 7.2 Essential Vim Commands

```bash
vim file.txt        # Open file in vim
vi file.txt         # Open with vi

# MODE SWITCHING:
i        # Insert before cursor
I        # Insert at start of line
a        # Insert after cursor
A        # Insert at end of line
o        # Open new line below
O        # Open new line above
Esc      # Return to Normal mode

# SAVING AND QUITTING (in Command mode — press : first):
:w           # Save (write)
:q           # Quit (if no changes)
:wq          # Save and quit
:x           # Save and quit (same as :wq)
ZZ           # Save and quit (Normal mode shortcut)
:q!          # Quit WITHOUT saving (force)
:w filename  # Save as different filename

# NAVIGATION (Normal mode):
0            # Jump to start of line
$            # Jump to end of line
gg           # Jump to first line of file
G            # Jump to last line of file


# EDITING (Normal mode):
x            # Delete character under cursor
dd           # Delete (cut) current line
5dd          # Delete 5 lines
dw           # Delete word
d$           # Delete to end of line
d0           # Delete to start of line
yy           # Yank (copy) current line
5yy          # Yank 5 lines
p            # Paste after cursor
P            # Paste before cursor
u            # Undo
Ctrl+r       # Redo
>>           # Indent line right
<<           # Indent line left

# SEARCH (Normal mode):
/pattern      # Search forward
?pattern      # Search backward
n             # Next match
N             # Previous match
*             # Search for word under cursor (forward)
#             # Search for word under cursor (backward)

# SEARCH AND REPLACE (Command mode):
:s/old/new/          # Replace first occurrence in current line
:s/old/new/g         # Replace all in current line
:%s/old/new/g        # Replace all in entire file
:%s/old/new/gc       # Replace all with confirmation
:5,10s/old/new/g     # Replace in lines 5-10

# VISUAL MODE:
v            # Character visual mode
V            # Line visual mode
Ctrl+v       # Block visual mode
# Then: d=delete, y=yank, >=indent, <=unindent, :=command

# MULTIPLE FILES:
:e file.txt      # Open another file


# USEFUL COMMANDS:
:set number          # Show line numbers
:set nonumber        # Hide line numbers
:set syntax=python   # Set syntax highlighting
:syntax on           # Enable syntax highlighting
:set paste           # Paste mode (preserves formatting)
:set nopaste         # Disable paste mode
:set ignorecase      # Case-insensitive search
gg=G                 # Auto-indent entire file
```

---

## 8. 🔗 Shell & Environment Variables

The shell is the interface between the user and the operating system. Environment variables allow the shell and applications to store values that affect behavior, such as paths, editors, and custom settings.

### 8.1 Variables

```bash
# Define variables:
name="Alice"                      # No spaces around =
NUMBER=42
readonly CONSTANT="pi"            # Read-only variable

# Use variables:
echo $name
echo ${name}                      # Better syntax — avoids ambiguity
echo ${name:-"default"}           # Use default if variable is empty
echo ${name:="default"}           # Assign default if empty
echo ${#name}                     # Length of variable

# Unset:
unset name                        # Remove variable

# Environment variables (available to subprocesses):
export name="Alice"
export PATH="$PATH:/opt/myapp/bin"

# View all environment variables:
env                               # All exported variables
printenv                          # Same
printenv HOME                     # Specific variable
set                               # All variables + functions (shell)
```

### 8.2 Important Environment Variables

| Variable | Description |
|----------|-------------|
| `$HOME` | Current user's home directory |
| `$USER` / `$LOGNAME` | Current username |
| `$PATH` | Directories searched for commands |
| `$SHELL` | Current shell path |
| `$PWD` | Current working directory |
| `$OLDPWD` | Previous working directory |
| `$HOSTNAME` | Machine hostname |
| `$PS1` | Primary prompt string |
| `$PS2` | Secondary prompt (continuation) |
| `$EDITOR` | Default text editor |
| `$LANG` | System language/locale |
| `$TZ` | Timezone |
| `$UID` | Current user's ID |
| `$?` | Exit status of last command |
| `$!` | PID of last background process |
| `$$` | PID of current shell |
| `$0` | Name of current script/shell |
| `$#` | Number of arguments to script |
| `$@` | All arguments to script |
| `$*` | All arguments as single string |

### 8.3 Shell Profile Files

```bash
# Login shell startup order:
/etc/environment        # System-wide environment variables
/etc/profile            # System-wide profile (all users)
/etc/profile.d/*.sh     # Drop-in profile scripts
~/.bash_profile         # User-specific (login shell)
~/.bash_login           # Fallback if .bash_profile not found
~/.profile              # Fallback (POSIX sh)

# Interactive non-login shell:
/etc/bash.bashrc        # System-wide bashrc
~/.bashrc               # User-specific bashrc

# Reload without logout:
source ~/.bashrc
. ~/.bashrc             # Same as source
```

### 8.4 PATH Management

```bash
# View current PATH:
echo $PATH
# /usr/local/bin:/usr/bin:/bin:/usr/local/sbin:/usr/sbin

# Add to PATH (in ~/.bashrc or ~/.bash_profile):
export PATH="$PATH:/opt/myapp/bin"        # Append
export PATH="/opt/myapp/bin:$PATH"        # Prepend (higher priority)

# Check which binary will run:
which python3
type python3
command -v python3
```
---

## 9. 🐚 Shell Profile Files — `.bash_profile`, `.bashrc`, `.bash_logout`

### 9.1 Profile File Execution Order

```
LOGIN SHELL (SSH, TTY login):
  /etc/environment        → System-wide env vars (all shells)
  /etc/profile            → System-wide (bash login)
  /etc/profile.d/*.sh     → Drop-in scripts
  ~/.bash_profile         → User login config (FIRST choice)
  ~/.bash_login           → Fallback if .bash_profile missing
  ~/.profile              → Fallback (POSIX compatible)
  ~/.bash_logout          → Runs when login shell EXITS

NON-LOGIN INTERACTIVE SHELL (new terminal, bash in GUI):
  /etc/bash.bashrc        → System-wide (Ubuntu/Debian)
  /etc/bashrc             → System-wide (RHEL/CentOS)
  ~/.bashrc               → User-specific interactive config
```

### 9.2 `.bash_profile` — Login Shell Config

```bash
cat ~/.bash_profile
```

```bash
# ~/.bash_profile — runs once at LOGIN
# Purpose: Set environment, PATH, export variables

# Source .bashrc to share settings with non-login shells:
if [ -f ~/.bashrc ]; then
    . ~/.bashrc
fi

# PATH customization:
export PATH="$HOME/.local/bin:$HOME/bin:$PATH"
export PATH="$PATH:/opt/myapp/bin"

# Environment variables:
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk
export EDITOR=vim
export PAGER=less
export HISTSIZE=10000
export HISTFILESIZE=20000

# Greeting at login:
echo "Welcome back, $USER! Today is $(date)"
```

### 9.3 `.bashrc` — Interactive Shell Config

```bash
cat ~/.bashrc
```

```bash
# ~/.bashrc — runs for every NEW interactive bash session
# Purpose: Aliases, functions, prompt, history settings

# If not running interactively, exit:
case $- in
    *i*) ;;
      *) return;;
esac

# History settings:
HISTSIZE=10000
HISTFILESIZE=20000
HISTCONTROL=ignoreboth:erasedups   # Ignore duplicates and lines starting with space
HISTTIMEFORMAT="%Y-%m-%d %H:%M:%S "
shopt -s histappend                # Append to history, don't overwrite

# Window size check after each command:
shopt -s checkwinsize

# Prompt customization:
PS1='\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
# Colors: 32=green, 34=blue, 31=red, 33=yellow

# Aliases:
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias ..='cd ..'
alias ...='cd ../..'
alias grep='grep --color=auto'
alias df='df -h'
alias du='du -sh'
alias free='free -h'
alias ps='ps aux'
alias update='sudo apt update && sudo apt upgrade -y'
alias vi='vim'
alias cls='clear'

# Custom functions:
mkcd() { mkdir -p "$1" && cd "$1"; }
extract() {
    case "$1" in
        *.tar.gz)  tar -xzf "$1" ;;
        *.tar.bz2) tar -xjf "$1" ;;
        *.zip)     unzip "$1" ;;
        *.gz)      gunzip "$1" ;;
        *) echo "Unknown format: $1" ;;
    esac
}
```

### 9.4 `.bash_logout` — Logout Cleanup

```bash
cat ~/.bash_logout
```

```bash
# ~/.bash_logout — runs when LOGIN shell exits
# Purpose: Cleanup, security, messages

# Clear terminal for security:
clear

# Save command history:
history -a

# Remove temp files:
rm -f /tmp/mytempfile 2>/dev/null

# Optional: log logout time
echo "$(date) - $USER logged out from $HOSTNAME" >> ~/.logout_history
```

### 9.5 Applying Changes Without Logout

```bash
source ~/.bashrc           # Reload .bashrc
. ~/.bashrc                # Same (POSIX syntax)
source ~/.bash_profile     # Reload .bash_profile
exec bash                  # Replace current shell with fresh one
```

---

## 10. 🔑 Hidden Files and Aliases

### 10.1 Hidden Files in Linux

```bash
# Files/directories starting with . are hidden:
ls                   # Shows regular files only
ls -a                # Shows ALL including hidden (. files)
ls -la               # Hidden files with details

# Common hidden files in home directory:
~/.bashrc            # Shell config
~/.bash_profile      # Login shell config
~/.bash_history      # Command history
~/.ssh/              # SSH keys directory
~/.gitconfig         # Git config
~/.vimrc             # Vim config
~/.profile           # Generic shell profile

# Create hidden file:
touch .myhiddenfile

# Create hidden directory:
mkdir .myhiddendir

# Find ALL hidden files in a directory:
find /home/alice -name ".*" -type f

# Find hidden files (exclude . and ..):
ls -la | grep '^\.' 
find . -name ".*" ! -name "." ! -name ".."
```

### 10.2 alias — Command Shortcuts

```bash
# Create temporary alias (lost on logout):
alias ll='ls -alF'
alias ..='cd ..'
alias update='sudo apt update && sudo apt upgrade -y'
alias vi='vim'
alias ports='ss -tuln'
alias myip='curl -s ifconfig.me'
alias df='df -h'
alias ping='ping -c 4'

# View all aliases:
alias

# View specific alias:
alias ll

# Remove alias:
unalias ll
unalias -a                         # Remove ALL aliases

# Permanent aliases — add to ~/.bashrc:
echo "alias ll='ls -alF'" >> ~/.bashrc
source ~/.bashrc

# Alias with sudo:
alias apt-update='sudo apt update && sudo apt upgrade -y'

# Useful admin aliases:
alias sysl='sudo journalctl -f'
alias nginx-reload='sudo systemctl reload nginx'
alias grep='grep --color=auto'
alias alert='notify-send --urgency=low -i "$([ $? = 0 ] && echo terminal || echo error)"'

# Bypass alias (run actual command):
\cp file1 file2          # Run 'cp' not aliased version
command cp file1 file2   # Same
```



---
