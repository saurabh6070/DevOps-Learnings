# Git Fundamentals and Setup

> Adapted from [01-Introduction.md](../01-Introduction.md)

This note preserves the full content of the original Git introduction guide and presents it as a structured learning document for beginners and DevOps students.

### Key takeaways

- Understand why version control matters in software development.
- Learn the core Git concepts and terminology.
- Set up Git correctly so your commits are traceable and consistent.

## 1. Version Control System (VCS)

A Version Control System is a tool that helps manage changes to files over time. It allows teams to collaborate, track history, and recover previous versions.

### Types of VCS

| Type | Description |
|---|---|
| Centralized VCS | A single central repository is used by all users |
| Distributed VCS | Every developer has a full local copy of the repository |

### CVCS vs DVCS

| Feature | CVCS | DVCS |
|---|---|---|
| Architecture | Centralized | Distributed |
| Repository location | Single central repo | Multiple local and remote repos |
| Offline work | Limited | Full support |
| Backup | Single point of failure | Multiple copies |
| Performance | Depends on network | Faster for local tasks |
| Example | SVN, CVS | Git, Mercurial |

## 2. What is Git?

Git is a free and open-source distributed version control system created by Linus Torvalds in 2005. It supports branching, merging, collaboration, and fast local operations.

## 3. Basic Terminologies

| Term | Meaning |
|---|---|
| Repository (Repo) | A directory where Git stores files and history |
| Commit | A snapshot of your changes |
| Branch | A separate line of development |
| Merge | Combine changes from different branches |
| Remote | A version of the repository hosted on a network |
| Staging Area | A place to prepare changes before committing |
| HEAD | Pointer to the current commit |
| Clone | Local copy of a remote repo |
| Fork | Personal copy of someone else’s repository |
| Tag | Named reference to a specific commit |
| Rebase | Reapply commits on top of another branch |
| Hook | Script that runs during Git events |

## 4. Setting Up Git

Before you can work with Git effectively, you need a working Git environment on your machine and a basic identity configuration. These setup steps ensure that each commit is attributed correctly and that Git behaves consistently across systems.

### Installation

```bash
# Windows
# Download Git from https://git-scm.com

# macOS (Homebrew)
brew install git

# Ubuntu/Debian
sudo apt install git
```

### Verify installation

```bash
git --version
```

### Initial configuration

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
git config --global core.editor "vi"
git config --global init.defaultBranch main
git config --list
```

## 5. Repository Commands

Once Git is installed, the next step is to create or obtain a repository. These commands form the foundation of working with Git because they define where your project history will live and how it will be shared.

### Initialize a repository

```bash
git init
```

### Clone a repository

```bash
git clone <repository-url>
git clone <repository-url> <folder-name>
```

### Forking

Forking creates a personal copy of another user’s repo on a hosting platform.

```bash
git clone <your-fork-url>
```

## 6. Working with Files

After a repository exists, the main activity becomes tracking and recording changes to files. Understanding the file lifecycle helps students reason about what happens when they create, edit, stage, and commit files.

### Git file lifecycle

```text
Untracked -> Staged -> Committed
Modified <- edit <-
```

### Status and staging

```bash
git status
git status -s
git add <file-name>
git add .
git add *.js
git add src/
```

### Commit changes

```bash
git commit -m "Your commit message"
git commit -am "Message"
git commit --amend -m "New msg"
```

### Remove files

```bash
git rm <file-name>
git rm --cached <file-name>
```
