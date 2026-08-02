# Git Repository Workflow

> Adapted from [01-Introduction.md](../01-Introduction.md)

## 1. File Lifecycle in Git

Files move through these states:

- Untracked
- Modified
- Staged
- Committed

## 2. Working with Files

```bash
git status
git status -s
git add <file>
git add .
git commit -m "Your message"
git commit -am "Message"
git rm <file>
git rm --cached <file>
```

## 3. Viewing Changes

```bash
git diff
git diff --staged
git diff HEAD
git diff --stat
```

## 4. Stashing Work-in-Progress

```bash
git stash
git stash -u
git stash list
git stash pop
git stash apply stash@{1}
```

## 5. Tags

```bash
git tag v1.0
git tag -a v1.0 -m "Release"
git push origin v1.0
git push origin --tags
git tag -d v1.0
```
