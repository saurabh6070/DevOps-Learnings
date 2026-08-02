# Git Interview Questions and Quick Reference

> Adapted from [03-Questionaire-Interview.md](../03-Questionaire-Interview.md)

## 1. Beginner Questions

Examples include:

- What is Git?
- What is a repository?
- What is a commit?
- Difference between `git pull` and `git fetch`
- What is `.gitignore`?
- What is `HEAD`?
- What is `origin`?

## 2. Intermediate Questions

Examples include:

- What is the difference between `git merge` and `git rebase`?
- What are the three types of `git reset`?
- How do you rollback to a specific commit?
- When should you use `git stash`?
- What is `git cherry-pick`?
- What are Git tags?

## 3. Advanced Questions

Examples include:

- What is the `.git` directory structure?
- How does Git store objects?
- What is a detached HEAD?
- How does Git handle submodules?
- How do hooks work?

## 4. Quick Reference Cheat Sheet

```bash
git init
git clone <url>
git status
git add .
git commit -m "msg"
git push origin <branch>
git pull origin <branch>
git branch
git checkout -b <branch>
git merge <branch>
git revert <hash>
git reset --hard HEAD~1
git stash
git tag v1.0
git log --oneline --graph --all --decorate
```
