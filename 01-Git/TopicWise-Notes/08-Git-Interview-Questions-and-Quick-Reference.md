# Git Interview Questions and Quick Reference

> Adapted from [03-Questionaire-Interview.md](../03-Questionaire-Interview.md)

This file preserves the original interview-oriented content and turns it into a practical study guide for students preparing for DevOps and Git interviews.

## 1. Beginner Questions

For beginners, the goal is to understand the purpose of Git and how it fits into modern software development. These questions build the mindset needed before moving into advanced workflows and team practices.

### Q1. What is Git?

Git is a distributed version control system used to track changes in code and collaborate with others.

### Q2. What is a repository?

A repository stores the project files and their history.

### Q3. What is a commit?

A commit is a snapshot of changes made at a specific time.

### Q4. What is the difference between `git pull` and `git fetch`?

- `git fetch` downloads remote changes without merging them
- `git pull` fetches and merges immediately

### Q5. What is `.gitignore`?

It tells Git which files or directories to ignore.

### Q6. What is `HEAD`?

`HEAD` points to the current commit in the active branch.

### Q7. What is `origin`?

`origin` is the default name of the remote repository.

## 2. Intermediate Questions

Once the basics are clear, interviews often test how well a candidate understands practical Git workflows. These questions focus on branch management, history modification, and safe collaboration.

### Q8. What is the difference between `git merge` and `git rebase`?

- `merge` preserves history and creates a merge commit
- `rebase` rewrites history into a linear form

### Q9. What are the three types of `git reset`?

| Type | Effect |
|---|---|
| `--soft` | Moves HEAD, keeps changes staged |
| `--mixed` | Moves HEAD, unstages changes |
| `--hard` | Moves HEAD and deletes changes |

### Q10. How do you rollback to a specific commit?

```bash
git revert <commit-hash>
git reset --hard <commit-hash>
```

### Q11. When should you use `git stash`?

Use it when you need to temporarily save uncommitted work and switch tasks.

### Q12. What is `git cherry-pick`?

It applies the changes from one specific commit to another branch.

### Q13. What are Git tags?

Tags mark important points in history, often used for releases.

## 3. Advanced Questions

Advanced questions examine how well a developer understands Git internally and how to use it in sophisticated engineering environments. This includes repository internals, hooks, submodules, and history management.

### Q14. What is the `.git` directory?

It contains Git metadata, objects, refs, hooks, and the index.

### Q15. How does Git store objects?

Git stores commits, trees, and blobs using SHA-based object IDs.

### Q16. What is a detached HEAD?

It means `HEAD` points directly to a commit rather than a branch.

### Q17. How do hooks work?

Hooks are scripts that run automatically at specific Git events.

### Q18. What are submodules?

Submodules let one repository include another repository as a nested project.

## 4. Quick Reference Cheat Sheet

This final section consolidates the most commonly used Git commands into a compact reference that can be reviewed quickly before interviews, demos, or daily work.

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
