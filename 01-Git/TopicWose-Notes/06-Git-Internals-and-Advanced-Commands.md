# Git Internals and Advanced Commands

> Adapted from [01-Introduction.md](../01-Introduction.md)

## 1. Git Internals

Git stores data as objects in the `.git` directory.

- Commit: metadata and parent pointers
- Tree: directory snapshot
- Blob: file contents

```bash
cat .git/HEAD
cat .git/refs/heads/main
git show-ref
git hash-object <file>
git hash-object -w <file>
```

## 2. Git Aliases

```bash
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.cm commit
git config --global alias.st status
git config --global alias.lg "log --oneline --graph --all --decorate"
```

## 3. Git Hooks

```bash
.git/hooks/
```

Examples:
- `pre-commit`
- `commit-msg`
- `post-commit`
- `pre-push`
- `post-merge`

## 4. Submodules

```bash
git submodule add <repo-url>
git submodule init
git submodule update
git submodule update --remote
git clone --recurse-submodules <repo-url>
```

## 5. Git Clean and Bisect

```bash
git clean -n
git clean -f
git clean -fd
git clean -fX
git clean -fx
git bisect start
git bisect bad
git bisect good <commit>
git bisect reset
```

## 6. Git Config Levels

```bash
git config --system core.editor "vim"
git config --global user.name "Your Name"
git config --local user.email "work@co.com"
git config --list --show-origin
```
