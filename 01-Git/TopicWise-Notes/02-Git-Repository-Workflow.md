# 🔄 Git Repository Workflow and Everyday Commands

This file preserves the original content about the day-to-day repository workflow and common Git commands used by students and engineers.

### 🔹 Key takeaways

- Learn how to inspect the state of a repository before changing anything.
- Practice staging and committing in a structured way.
- Use tags and stash to manage workflow interruptions safely.

## 📌 1. Checking Repository Status

In daily Git work, the first thing a developer usually wants to know is what changed. Status checks provide a quick overview of modified, staged, or untracked files before any further action is taken.

```bash
git status
git status -s
```

## 📌 2. Adding Files to the Staging Area

The staging area acts as a review step between editing files and creating a commit. It allows developers to choose exactly which changes should be part of the next snapshot.

```bash
git add <file-name>
git add .
git add *.js
git add src/
```

## 📌 3. Committing Changes

A commit is the actual record of a logical change in the project history. Good commits help teams understand what changed, why it changed, and when it changed.

```bash
git commit -m "Your commit message"
git commit -am "Message"
git commit --amend -m "New msg"
```

## 📌 4. Removing Files from Git

Sometimes a file should no longer be part of the project history. Removing it properly from Git ensures the repository reflects the current architecture and intent of the project.

```bash
git rm <file-name>
git rm --cached <file-name>
```

## 📌 5. Viewing Changes

Before reviewing a change with a teammate or preparing a pull request, it is important to inspect what has been modified. Diff commands make it easier to understand the exact impact of the change.

```bash
git diff
git diff --staged
git diff HEAD
git diff --stat
git diff --name-only
git diff --word-diff
```

## 📌 6. Working with Tags

Tags are useful when a project reaches a milestone such as a release or a stable version. They create a human-readable marker for a specific point in history.

```bash
git tag v1.0
git tag -a v1.0 -m "First stable release"
git push origin v1.0
git push origin --tags
git tag -d v1.0
```

## 📌 7. Temporary Save with Git Stash

During development, a team member may need to switch context quickly without losing unfinished work. Stash provides a temporary place to store those in-progress changes safely.

```bash
git stash
git stash -u
git stash -m "message"
git stash list
git stash apply
git stash pop
git stash drop
git stash clear
```
