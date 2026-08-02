# Git Fundamentals and Setup

> Adapted from [01-Introduction.md](../01-Introduction.md)

## 1. What is Version Control?

A Version Control System (VCS) tracks changes to files over time.

- Centralized VCS: one shared repository
- Distributed VCS: each developer has a local copy

Git is a distributed VCS created by Linus Torvalds.

## 2. Core Git Concepts

- Repository (repo): directory containing project files and history
- Commit: snapshot of changes
- Branch: separate line of development
- Merge: combine changes from branches
- Remote: shared copy of the repo
- Staging Area: place where changes are prepared before commit
- HEAD: pointer to the current commit

## 3. Installing and Configuring Git

```bash
git --version
brew install git        # macOS
sudo apt install git   # Ubuntu/Debian
```

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
git config --list
```

## 4. Repository Basics

```bash
git init
git clone <repo-url>
git clone <repo-url> <folder-name>
```

## 5. Common First Commands

```bash
git status
git add <file>
git add .
git commit -m "message"
```
