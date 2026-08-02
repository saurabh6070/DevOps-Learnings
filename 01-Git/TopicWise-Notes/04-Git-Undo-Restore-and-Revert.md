# Undo, Restore, Reset, and Revert

> Adapted from [01-Introduction.md](../01-Introduction.md)

This note preserves the original content on how to undo and recover from changes safely.

### Key takeaways

- Know when to use restore, reset, or revert.
- Understand the difference between rewriting history and preserving it.
- Learn how to recover from mistakes without losing control of the project.

## 1. Git Restore

Sometimes a file needs to return to a previous state because the latest edits are no longer wanted. Git restore provides a safe way to discard local changes or undo a staged change without affecting the full repository history.

```bash
git restore <file-name>
git restore --source <commit-hash> <file-name>
git restore .
git add myapp.py
git restore --staged myapp.py
```

## 2. Git Reset

Reset is used when you want to move the current branch pointer to a different commit. It is powerful because it can change what is recorded in history, what is staged, and what remains in the working directory.

Reset moves the HEAD pointer and can modify the staging area and working directory.

| Type | Effect |
|---|---|
| `--soft` | Moves HEAD, keeps changes staged |
| `--mixed` | Moves HEAD, resets staging, keeps changes in working dir |
| `--hard` | Moves HEAD and deletes uncommitted changes |

```bash
git reset --soft HEAD~1
git reset --mixed HEAD~1
git reset --hard HEAD~1
git reset --hard <commit-hash>
```

## 3. Git Revert

Revert is the safer alternative when the change has already been shared with others. Instead of rewriting history, it creates a new commit that undoes the effect of an earlier commit.

Revert creates a new commit that undoes an earlier change and is safe for shared branches.

```bash
git revert <commit-hash>
git revert <commit1>..<commit2>
```

## 4. Reset vs Revert

| Command | History | Safe for shared branches |
|---|---|---|
| `git reset` | Rewrites history | No |
| `git revert` | Preserves history | Yes |
