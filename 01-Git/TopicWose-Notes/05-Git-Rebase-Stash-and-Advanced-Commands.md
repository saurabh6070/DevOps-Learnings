# Rebase, Stash, Tags, Cherry-Pick, and Log

> Adapted from [01-Introduction.md](../01-Introduction.md)

## 1. Git Rebase

Rebasing reapplies commits on top of another branch to create a linear history.

```bash
git rebase master
git rebase -i HEAD~3
```

### Interactive rebase options

- `pick`: keep commit as-is
- `reword`: change message
- `edit`: pause and amend
- `squash`: combine with previous
- `fixup`: squash without message
- `drop`: remove commit

## 2. Git Stash

```bash
git stash
git stash -u
git stash list
git stash pop
git stash apply stash@{1}
git stash drop
git stash clear
```

## 3. Git Tags

```bash
git tag v1.0
git tag -a v1.0 -m "Release"
git push origin v1.0
git push origin --tags
git tag -d v1.0
```

## 4. Cherry-Pick

```bash
git cherry-pick <commit-hash>
git cherry-pick <commit1> <commit2>
git cherry-pick <commit-hash> --no-commit
```

## 5. Git Log

```bash
git log
git log --oneline
git log --graph --all --decorate
git log --author="John"
git log --since="2024-01-01"
git log --grep="fix"
```
