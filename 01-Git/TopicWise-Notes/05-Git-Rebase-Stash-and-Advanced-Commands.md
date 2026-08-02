# Rebase, Stash, Tags, Diff, Log, and Advanced Commands

> Adapted from [01-Introduction.md](../01-Introduction.md)

This note preserves the original content on rebase, stash, tags, diff, log, and related advanced Git operations.

## 1. Git Rebase

Rebase is used when you want to keep the project history visually linear and clean. It moves the work from one branch onto another so that commits appear to have been created in a more sequential order.

```bash
git rebase master
git rebase -i HEAD~3
```

### Interactive rebase options

| Command | Action |
|---|---|
| `pick` | Keep commit as-is |
| `reword` | Edit commit message |
| `edit` | Pause to amend |
| `squash` | Combine with previous |
| `fixup` | Combine and discard message |
| `drop` | Remove commit |

## 2. Git Stash

At times you need to set aside incomplete work to switch tasks without committing. Stash provides a temporary storage area so the current changes can be restored later.

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

## 3. Git Tags

Tags are used to mark meaningful points in history, especially releases. They make it easier to refer to a known-good version of the project later.

```bash
git tag v1.0
git tag -a v1.0 -m "First stable release"
git push origin v1.0
git push origin --tags
git tag -d v1.0
```

## 4. Git Cherry-Pick

Sometimes a single fix from one branch is needed in another branch without bringing the whole branch history. Cherry-pick allows that targeted transfer of one commit at a time.

```bash
git cherry-pick <commit-hash>
git cherry-pick <commit1> <commit2>
git cherry-pick <commit-hash> --no-commit
```

## 5. Git Diff

Diff commands are used to inspect the exact changes between versions, branches, or commits. They are essential for code review, debugging, and understanding the impact of a change.

```bash
git diff
git diff --staged
git diff HEAD
git diff branch1 branch2
git diff main..feature/login
git diff main...feature/login
git diff --stat
git diff --name-only
git diff --word-diff
```

## 6. Git Log

The log provides a historical view of the project. It helps developers understand who changed what, when, and in what order, which is especially valuable in debugging and auditing.

```bash
git log
git log --oneline
git log --oneline --graph
git log --oneline --graph --all
git log --decorate
git log --author="John"
git log --since="2024-01-01"
git log --until="2024-12-31"
git log --grep="fix"
```
