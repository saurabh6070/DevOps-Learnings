# Branching, Remotes, and Pull Requests

> Adapted from [01-Introduction.md](../01-Introduction.md)

## 1. Branching Basics

```bash
git branch <branch-name>
git checkout <branch-name>
git switch <branch-name>
git checkout -b <branch-name>
git switch -c <branch-name>
git branch -d <branch-name>
git branch -D <branch-name>
```

## 2. Merge and Conflict Handling

- Fast-forward merge happens when no new commits exist on the base branch
- Three-way merge happens when both branches changed
- Conflicts require manual resolution

```bash
git merge <branch-name>
```

## 3. Remotes

```bash
git remote add origin <url>
git remote -v
git push origin <branch>
git push -u origin <branch>
git pull origin <branch>
git fetch origin
git fetch --all
```

## 4. Pull Request Workflow

1. Fork the repository
2. Clone your fork
3. Create a feature branch
4. Commit and push changes
5. Open a pull request
6. Review and merge

## 5. Upstream Workflow

```bash
git remote add upstream <original-repo-url>
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```
