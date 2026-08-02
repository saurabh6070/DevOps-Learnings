# Undo, Restore, Reset, and Revert

> Adapted from [01-Introduction.md](../01-Introduction.md)

## 1. Git Restore

Use `git restore` to discard or unstage changes.

```bash
git restore <file>
git restore --source <commit-hash> <file>
git restore .
git restore --staged <file>
```

## 2. Git Reset

`git reset` moves the current branch pointer and can modify the staging area and working directory.

| Mode | Effect |
|---|---|
| `--soft` | Moves HEAD, keeps changes staged |
| `--mixed` | Moves HEAD, unstages changes |
| `--hard` | Moves HEAD and discards all changes |

```bash
git reset --soft HEAD~1
git reset --mixed HEAD~1
git reset --hard HEAD~1
git reset --hard <commit-hash>
```

## 3. Git Revert

`git revert` creates a new commit that undoes an older one and is safer for shared branches.

```bash
git revert <commit-hash>
git revert <commit1>..<commit2>
```

## 4. When to Use Each

- Use `restore` for local file-level cleanup
- Use `reset` for private/local history cleanup
- Use `revert` for public or shared branch safety
