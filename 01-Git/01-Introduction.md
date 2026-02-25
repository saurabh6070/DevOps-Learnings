# 📘 Git & Version Control — Complete Reference Guide

> 🚀 A comprehensive guide covering Git fundamentals, advanced commands, workflows, and internals — ready for real-world team development.

---

## 📌 Table of Contents

| # | Section |
|---|---------|
| 1 | [🗂️ Version Control System (VCS)](#1-%EF%B8%8F-version-control-system-vcs) |
| 2 | [🔧 What is Git?](#2--what-is-git) |
| 3 | [📖 Basic Terminologies](#3--basic-terminologies) |
| 4 | [⚙️ Setting Up Git](#4-%EF%B8%8F-setting-up-git) |
| 5 | [📁 Repository Commands](#5--repository-commands) |
| 6 | [📝 Working with Files](#6--working-with-files) |
| 7 | [🌿 Branching and Merging](#7--branching-and-merging) |
| 8 | [🌐 Working with Remotes](#8--working-with-remotes) |
| 9 | [♻️ Git Restore](#9-%EF%B8%8F-git-restore) |
| 10 | [↩️ Git Reset](#10-%EF%B8%8F-git-reset) |
| 11 | [⏪ Git Revert](#11--git-revert) |
| 12 | [🔀 Git Rebase](#12--git-rebase) |
| 13 | [🚦 Git Workflow Strategies](#13--git-workflow-strategies) |
| 14 | [📦 Git Stash](#14--git-stash) |
| 15 | [🏷️ Git Tags](#15-%EF%B8%8F-git-tags) |
| 16 | [🔍 Git Diff](#16--git-diff) |
| 17 | [🍒 Git Cherry-Pick](#17--git-cherry-pick) |
| 18 | [📜 Git Log — Advanced](#18--git-log--advanced) |
| 19 | [🔑 Git Aliases](#19--git-aliases) |
| 20 | [🪝 Git Hooks](#20--git-hooks) |
| 21 | [📎 Git Submodules](#21--git-submodules) |
| 22 | [🧹 Git Clean](#22--git-clean) |
| 23 | [🐛 Git Bisect](#23--git-bisect) |
| 24 | [🙈 Git Ignore](#24--git-ignore) |
| 25 | [🔬 Git Cat-File](#25--git-cat-file) |
| 26 | [🧠 Git Internals (Advanced)](#26--git-internals-advanced) |
| 27 | [🔗 Git Upstream](#27--git-upstream) |
| 28 | [⚙️ Git Config Levels](#28-%EF%B8%8F-git-config-levels) |
| 29 | [🔁 Pull Request Workflow](#29--pull-request-workflow) |
| 30 | [⚡ Quick Reference Cheat Sheet](#30--quick-reference-cheat-sheet) |

---

## 1. 🗂️ Version Control System (VCS)

A **Version Control System (VCS)** is a tool that helps manage changes to source code over time, allowing multiple developers to collaborate efficiently. It tracks revisions, enabling you to revert to previous versions and maintain a complete history of changes.

### Types of Version Control Systems

| Type | Description |
|------|-------------|
| 🏢 **Centralised VCS (CVCS)** | A single central repository that all developers connect to (e.g., SVN, CVS) |
| 🌐 **Distributed VCS (DVCS)** | Every developer has a full local copy of the repository (e.g., Git, Mercurial) |

### CVCS vs DVCS — Comparison

| Feature | CVCS | DVCS |
|---------|------|------|
| **Architecture** | Centralized | Distributed |
| **Repository Location** | Single central repository | Multiple repositories (local and remote) |
| **Access** | Requires network access to central server | Can work offline with local repository |
| **Commit History** | Stored on central server | Stored locally, can be pushed to remote |
| **Collaboration** | Changes shared via central server | Changes shared directly between developers |
| **Backup** | ❌ Single point of failure | ✅ Multiple copies of the repository |
| **Performance** | 🐢 Slower (network dependency) | ⚡ Faster (local operations) |
| **Branching & Merging** | Complex, less flexible | Easier and more flexible |
| **Conflict Resolution** | Handled on central server | Handled locally before pushing |
| **Security** | Centralized control | Decentralized control |
| **Scalability** | Limited by central server | Highly scalable |
| **Examples** | SVN, CVS | Git, Mercurial |

---

## 2. 🔧 What is Git?

**Git** is a free, open-source distributed version control system created by **Linus Torvalds** in 2005. It allows multiple developers to work on a project simultaneously, keeps track of changes made to files and directories, and enables reverting to previous versions if needed. Git is fast, efficient, and supports non-linear development through powerful branching and merging.

---

## 3. 📖 Basic Terminologies

| Term | 💡 Description |
|------|----------------|
| 🗃️ **Repository (Repo)** | A directory where Git stores all files and their history |
| 📸 **Commit** | A snapshot of your changes; each commit has a unique ID and message |
| 🌿 **Branch** | A separate line of development; default branch is `main` or `master` |
| 🔀 **Merge** | Combining changes from different branches into one |
| 🌐 **Remote** | A version of your repository hosted on a network (e.g., GitHub, GitLab) |
| 🎭 **Staging Area (Index)** | A preparation zone where changes are gathered before committing |
| 👉 **HEAD** | A pointer to the current commit in your working branch |
| 📋 **Clone** | A local copy of a remote repository |
| 🍴 **Fork** | A personal copy of someone else's repository on a hosting service |
| 🏷️ **Tag** | A named reference to a specific commit, usually used for releases |
| 🔃 **Rebase** | Re-applying commits on top of another branch for a cleaner history |
| 🎣 **Hook** | A script that runs automatically at certain Git events |

---

## 4. ⚙️ Setting Up Git

### 📥 Installation

```bash
# 🪟 Windows: Download from https://git-scm.com

# 🍎 macOS (via Homebrew):
brew install git

# 🐧 Linux (Debian/Ubuntu):
sudo apt-get install git

# ✅ Verify installation:
git --version
```

### 🛠️ Configuration

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
git config --global core.editor "vi"           # Set default editor
git config --global init.defaultBranch main    # Set default branch name

# 📋 View all configurations:
git config --list
```

---

## 5. 📁 Repository Commands

### 5.1 Initialize a New Repository

```bash
git init
```

### 5.2 Clone an Existing Repository

```bash
git clone <repository-url>
git clone <repository-url> <folder-name>   # Clone into a specific folder
```

### 5.3 🍴 Forking

Forking creates a personal copy of someone else's repository on a hosting platform (e.g., GitHub). After forking on the platform, clone your fork locally:

```bash
git clone <your-fork-url>
```

---

## 6. 📝 Working with Files

### 🔄 Git File Lifecycle

```
Untracked  ──git add──►  Staged  ──git commit──►  Committed
                                                       │
              ◄──git restore──  Modified  ◄──── edit ──┘
```

### 6.1 Check Repository Status

```bash
git status
git status -s    # Short/compact format
```

### 6.2 ➕ Add Files to Staging Area

```bash
git add <file-name>     # Stage a specific file
git add .               # Stage all changes
git add *.js            # Stage all JS files
git add src/            # Stage an entire directory
```

### 6.3 💾 Commit Changes

```bash
git commit -m "Your commit message"
git commit -am "Message"        # Stage tracked files and commit in one step
git commit --amend -m "New msg" # Edit the last commit message
```

### 6.4 🗑️ Remove Files

```bash
git rm <file-name>              # Remove file from repo and disk
git rm --cached <file-name>     # Untrack file but keep it on disk
```

---

## 7. 🌿 Branching and Merging

### 7.1 Create a New Branch

```bash
git branch <branch-name>
```

### 7.2 Switch to a Branch

```bash
git checkout <branch-name>
# OR (modern syntax):
git switch <branch-name>

# Create and switch in one step:
git checkout -b <branch-name>
git switch -c <branch-name>
```

### 7.3 List All Branches

```bash
git branch        # Local branches
git branch -a     # Local and remote branches
git branch -v     # With last commit info
```

### 7.4 ⚡ Fast-Forward Merge

If no new commits exist on the base branch since the feature branch was created, Git performs a **fast-forward merge** — the simplest merge with no conflicts.

```bash
git merge <branch-name>
```

> 📝 The output will mention `Fast-forward` when this type of merge occurs.

### 7.5 🗑️ Delete a Branch

```bash
git branch -d <branch-name>   # Safe delete (merged branches only)
git branch -D <branch-name>   # Force delete
```

### 7.6 ⚠️ 3-Way Merge / Merge Conflict

A **3-way merge** occurs when both the feature branch and the base branch have new commits since the branch was created. If the same lines were modified, a **conflict** occurs and must be resolved manually.

```bash
# Setup example:
mkdir my_Git_Project && cd my_Git_Project
git init
echo "initial content" > file.txt
git add file.txt
git commit -m "Initial commit on main"

# Create feature branch and make changes:
git checkout -b feature
echo "Feature branch changes" >> file.txt
git commit -am "Added changes to feature branch"

# Switch to master and make a conflicting change:
git checkout master
echo "Master branch content" >> file.txt
git commit -am "Changes on master"

# Merge — this triggers a conflict:
git merge feature

# Resolve conflicts in file.txt manually, then:
git add file.txt
git commit -m "Resolved merge conflict"
```

> ⚠️ After a conflict, `git status` shows files that need resolution. Open conflicting files, resolve the `<<<<<<<`, `=======`, `>>>>>>>` markers, then stage and commit.

---

## 8. 🌐 Working with Remotes

### 8.1 Add a Remote Repository

```bash
git remote add origin <repository-url>
```

### 8.2 View Remotes

```bash
git remote -v
```

### 8.3 📤 Push Changes to Remote

```bash
git push origin <branch-name>
git push -u origin <branch-name>   # Push and set upstream
```

### 8.4 📥 Pull Changes from Remote

```bash
git pull origin <branch-name>
```

### 8.5 Fetch Changes (Without Merging)

```bash
git fetch origin       # Fetch all remote changes
git fetch --all        # Fetch from all remotes
```

---

## 9. ♻️ Git Restore

The `git restore` command discards changes in the working directory or removes files from the staging area.

### 9.1 Discard Changes in Working Directory

```bash
git restore <file-name>
```

### 9.2 Restore a File from a Specific Commit

```bash
git restore --source <commit-hash> <file-name>
```

### 9.3 Restore All Files in Working Directory

```bash
git restore .
```

### 9.4 Unstage a File

```bash
git add myapp.py               # Accidentally staged
git restore --staged myapp.py  # Remove from staging, keep changes
```

### 9.5 Full Example

```bash
echo "Adding second line" >> myapp.py
git status                      # Shows myapp.py as modified

git restore myapp.py            # Discard changes
git status                      # Clean again

echo "Adding second line" >> myapp.py
git add myapp.py
git restore --staged myapp.py   # Unstage without losing changes
git status
```

---

## 10. ↩️ Git Reset

The `git reset` command moves the `HEAD` pointer and optionally modifies the staging area and working directory.

### Reset Types Comparison

| Type | HEAD | Staging Area | Working Directory |
|------|:----:|:------------:|:-----------------:|
| `--soft` | ✅ Moves | Unchanged | Unchanged |
| `--mixed` *(default)* | ✅ Moves | 🔄 Reset | Unchanged |
| `--hard` | ✅ Moves | 🔄 Reset | 🔄 Reset (⚠️ lost) |

### 10.1 🟢 Soft Reset

Moves HEAD but keeps changes in the staging area.

```bash
git reset --soft HEAD~1
```

### 10.2 🟡 Mixed Reset (Default)

Moves HEAD and resets the staging area, but keeps changes in the working directory.

```bash
git reset --mixed HEAD~1
```

### 10.3 🔴 Hard Reset

Moves HEAD and resets everything. **All uncommitted changes are permanently lost.**

```bash
git reset --hard HEAD~1
git reset --hard <commit-hash>   # Reset to a specific commit
```

> ⚠️ **Warning:** `git reset --hard` is destructive and cannot be undone. If you've already pushed commits to a remote, use `git revert` instead.

---

## 11. ⏪ Git Revert

`git revert` creates a **new commit** that undoes the changes from a previous commit. The original commit remains in history — making it safe for shared/public branches.

### 11.1 Revert a Single Commit

```bash
git revert <commit-hash>
```

### 11.2 Revert a Range of Commits

```bash
git revert <commit1>..<commit2>
```

### 📊 git reset vs git revert

| | `git reset` | `git revert` |
|---|---|---|
| **History** | ❌ Rewrites history | ✅ Preserves history |
| **Safety on shared branch** | ⚠️ Risky | ✅ Safe |
| **Creates new commit?** | No | Yes |
| **Best for** | Local/private cleanup | Undoing on shared branches |

---

## 12. 🔀 Git Rebase

Rebasing re-applies commits from the current branch on top of another branch. It produces a **cleaner, linear history** compared to merging, but rewrites commit hashes.

### 12.1 Regular Rebase

```bash
git rebase master
```

### 12.2 Interactive Rebase

Opens an editor to squash, reorder, edit, or drop commits:

```bash
git rebase -i HEAD~3
```

**Interactive rebase options:**

| Command | Action |
|---------|--------|
| `pick` | ✅ Keep the commit as-is |
| `reword` | ✏️ Keep commit, edit message |
| `edit` | 🛑 Pause to amend commit |
| `squash` | 🔗 Combine with previous commit |
| `fixup` | 🔗 Like squash, discard message |
| `drop` | 🗑️ Remove the commit entirely |

> ⚠️ **Warning:** Avoid rebasing commits already pushed to a shared remote. Use `git merge` instead in those cases.

---

## 13. 🚦 Git Workflow Strategies

Choosing the right workflow is critical for team productivity. Here are the most common strategies.

---

### 13.1 🏢 Centralized Workflow

**Best for:** Small teams or beginners transitioning from SVN.

All developers commit directly to the `main` branch.

```
Developer A ──┐
Developer B ──┼──► main branch ──► Remote (origin/main)
Developer C ──┘
```

```bash
git clone <repo-url>
# make changes
git pull origin main      # Sync before pushing
git push origin main
```

> ⚠️ Risk of frequent conflicts. No code review process. Not recommended for large teams.

---

### 13.2 🌿 Feature Branch Workflow

**Best for:** Most teams. Enables parallel development and code review via Pull Requests.

Each feature or fix is developed on its own branch and merged via a Pull Request.

```
main ──────────────────────────────────────────► main
         │                              ↑
         └──► feature/login ───────────┘  (PR + Merge)
```

```bash
# 1. Create a feature branch
git checkout -b feature/login

# 2. Work on the feature, commit regularly
git add .
git commit -m "Add login form"

# 3. Push to remote
git push origin feature/login

# 4. Open a Pull Request on GitHub/GitLab for code review

# 5. After approval, merge into main and delete branch
git checkout main
git merge feature/login
git branch -d feature/login
```

---

### 13.3 🌊 Git Flow (Advanced)

**Best for:** Structured production environments with scheduled releases.

Git Flow defines a strict branching model with dedicated roles for each branch.

#### Branch Structure

| Branch | Purpose |
|--------|---------|
| 🔵 `main` | Production-ready code only. Tagged with version numbers. |
| 🟢 `develop` | Integration branch where features are merged. |
| 🌱 `feature/*` | New features, branched from `develop`. |
| 🟡 `release/*` | Preparation for a new release. Branched from `develop`. |
| 🔴 `hotfix/*` | Emergency fixes to `main`. Merged into both `main` and `develop`. |

#### Git Flow Diagram

```
main      ──────────────────────────────────── v1.0 ─────────────────► v1.1
               ↑                                  ↑                     ↑
develop   ─────┴──────────────────────────────────┴─────────────────────┴──►
               │              ↑         ↑
feature/*  ────┘──────────────┘         │
                                        │
release/*                    ───────────┘
```

```bash
# Start a new feature
git checkout develop
git checkout -b feature/payment

# Finish feature — merge back into develop
git checkout develop
git merge feature/payment
git branch -d feature/payment

# Start a release
git checkout -b release/1.0 develop

# Finish release — merge into main and develop
git checkout main
git merge release/1.0
git tag -a v1.0 -m "Version 1.0"
git checkout develop
git merge release/1.0

# Emergency hotfix
git checkout -b hotfix/1.0.1 main
# fix bug, then:
git checkout main
git merge hotfix/1.0.1
git checkout develop
git merge hotfix/1.0.1
```

---

### 13.4 🍴 Forking Workflow

**Best for:** Open-source projects. Every contributor has their own server-side fork.

```
Upstream Repo ──────────────────────────────────────────────────────►
      │                                        ↑ Pull Request
      │ fork                                   │
      ▼                                        │
 Your Fork (origin) ◄── git push ── Local Repo ─────────────────────►
```

---

## 14. 📦 Git Stash

Git Stash **temporarily saves uncommitted changes** so you can switch context (e.g., switch branches) without committing incomplete work.

### 14.1 Basic Stash Commands

```bash
git stash               # Stash current changes (tracked files only)
git stash -u            # Also stash untracked files
git stash -m "message"  # Stash with a descriptive name
```

### 14.2 View Stashes

```bash
git stash list
# Output: stash@{0}: On main: WIP - login form
#         stash@{1}: On feature: WIP - dashboard
```

### 14.3 Apply Stash

```bash
git stash apply           # Apply most recent stash (keeps it in list)
git stash apply stash@{2} # Apply a specific stash
git stash pop             # Apply most recent stash AND remove it from list
```

### 14.4 Remove Stash

```bash
git stash drop            # Remove the most recent stash
git stash drop stash@{1}  # Remove a specific stash
git stash clear           # Remove all stashes
```

### 💡 Use Case Example

```bash
# You're mid-feature and need to fix a bug on main urgently:
git stash                   # Save your work-in-progress
git checkout main
git checkout -b hotfix/bug  # Fix the bug
# ... fix and commit ...
git checkout feature/login
git stash pop               # Restore your work
```

---

## 15. 🏷️ Git Tags

Tags mark **specific points in history** — typically used for version releases (v1.0, v2.0).

### Types of Tags

| Type | Description |
|------|-------------|
| 🪶 **Lightweight** | Just a name pointing to a commit. No extra metadata. |
| 📋 **Annotated** | Full object with tagger name, date, message. Recommended for releases. |

### 15.1 Create Tags

```bash
# Lightweight tag:
git tag v1.0

# Annotated tag (recommended):
git tag -a v1.0 -m "First stable release"

# Tag a specific (past) commit:
git tag -a v0.9 <commit-hash> -m "Beta release"
```

### 15.2 View Tags

```bash
git tag               # List all tags
git tag -l "v1.*"     # Filter tags by pattern
git show v1.0         # Show tag details and commit info
```

### 15.3 Push Tags to Remote

```bash
git push origin v1.0       # Push a specific tag
git push origin --tags     # Push all tags
```

### 15.4 Delete Tags

```bash
git tag -d v1.0                    # Delete local tag
git push origin --delete v1.0      # Delete remote tag
```

---

## 16. 🔍 Git Diff

`git diff` compares changes between commits, branches, files, or the working directory and staging area.

### 16.1 Basic Diff

```bash
git diff                        # Unstaged changes vs last commit
git diff --staged               # Staged changes vs last commit
git diff HEAD                   # All changes (staged + unstaged) vs last commit
```

### 16.2 Compare Branches

```bash
git diff branch1 branch2              # All differences between two branches
git diff main..feature/login          # Changes in feature not in main
git diff main...feature/login         # Changes since branches diverged
```

### 16.3 Compare Commits

```bash
git diff <commit1> <commit2>          # Between two specific commits
git diff HEAD~1 HEAD                  # Last commit vs previous
```

### 16.4 Diff a Specific File

```bash
git diff <file-name>                  # Changes in one file
git diff branch1 branch2 -- <file>    # File diff across branches
```

### 16.5 Useful Output Options

```bash
git diff --stat                  # Summary (files + lines changed)
git diff --name-only             # Only show changed filenames
git diff --word-diff             # Show word-level differences
```

> 💡 **Tip:** Use `git diff --stat` before opening a PR to quickly review what you've changed.

---

## 17. 🍒 Git Cherry-Pick

Cherry-pick applies a **specific commit from one branch to another** without merging the entire branch.

### 17.1 Cherry-Pick a Single Commit

```bash
git cherry-pick <commit-hash>
```

### 17.2 Cherry-Pick Multiple Commits

```bash
git cherry-pick <commit1> <commit2>         # Specific commits
git cherry-pick <commit1>..<commit2>         # A range of commits
```

### 17.3 Cherry-Pick Without Auto-Commit

```bash
git cherry-pick <commit-hash> --no-commit   # Stage changes without committing
```

### 💡 Use Case

```bash
# Bug was fixed on 'develop', but you need it on 'main' NOW:
git log develop --oneline     # Find the fix commit hash
git checkout main
git cherry-pick a1b2c3d       # Apply just that fix
```

> ⚠️ Cherry-picking creates a **new commit** with a different hash. Useful for targeted fixes, but can cause confusion if overused.

---

## 18. 📜 Git Log — Advanced

### 18.1 Basic Log Options

```bash
git log                          # Full detailed log
git log --oneline                # One line per commit
git log --oneline --graph        # With ASCII branch graph
git log --oneline --graph --all  # All branches visualized
git log --decorate               # Show branch/tag names
```

### 18.2 Filter Log Output

```bash
git log --author="John"          # Commits by a specific author
git log --since="2024-01-01"     # Commits after a date
git log --until="2024-12-31"     # Commits before a date
git log --grep="fix"             # Commits with "fix" in the message
git log -n 5                     # Last 5 commits only
```

### 18.3 Log for a Specific File

```bash
git log -- <file-name>           # Commits that changed a file
git log -p -- <file-name>        # With full diff for each commit
```

### 18.4 ⭐ Power Command

```bash
git log --oneline --graph --all --decorate
```

> This single command gives you the **full picture** of your entire repository's branch history in a compact visual format.

---

## 19. 🔑 Git Aliases

Aliases let you create shortcuts for frequently used Git commands.

### 19.1 Create Aliases

```bash
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.cm commit
git config --global alias.st status
git config --global alias.lg "log --oneline --graph --all --decorate"
```

### 19.2 Use Aliases

```bash
git co main          # Instead of: git checkout main
git br               # Instead of: git branch
git cm -m "msg"      # Instead of: git commit -m "msg"
git st               # Instead of: git status
git lg               # Beautiful log in one command!
```

### 19.3 View & Remove Aliases

```bash
git config --global --list | grep alias     # View all aliases
git config --global --unset alias.co        # Remove an alias
```

> 💡 Aliases are stored in `~/.gitconfig` and can also be edited directly there.

---

## 20. 🪝 Git Hooks

Git Hooks are **scripts that run automatically** at certain points in the Git lifecycle. They are used for enforcing code quality, automating tasks, and CI/CD integration.

### 20.1 Hook Location

```bash
.git/hooks/          # Local hooks (not tracked by Git)
```

### 20.2 Common Hooks

| Hook | ⏱️ When It Runs | 🔧 Common Use |
|------|----------------|--------------|
| `pre-commit` | Before a commit is created | Run linters, formatters |
| `commit-msg` | After commit message is entered | Enforce message format |
| `post-commit` | After commit is created | Notifications, logging |
| `pre-push` | Before `git push` | Run test suite |
| `post-merge` | After a merge completes | Install dependencies |
| `pre-rebase` | Before rebasing | Safety checks |

### 20.3 Creating a Hook

```bash
# Create a pre-commit hook:
nano .git/hooks/pre-commit

# Make it executable:
chmod +x .git/hooks/pre-commit
```

### 20.4 Example: pre-commit Hook

```bash
#!/bin/sh
# Run tests before every commit
npm test
if [ $? -ne 0 ]; then
  echo "❌ Tests failed. Commit aborted."
  exit 1
fi
echo "✅ Tests passed."
```

> 💡 Use **Husky** (for Node.js projects) to manage and share hooks across a team via `package.json`.

---

## 21. 📎 Git Submodules

Submodules allow you to **include one Git repository inside another**. Useful when your project depends on an external library or shared component that lives in its own repo.

### 21.1 Add a Submodule

```bash
git submodule add <repo-url>
git submodule add <repo-url> <path>   # Add to a specific path
```

### 21.2 Initialize & Update Submodules

```bash
# After cloning a repo with submodules:
git submodule init
git submodule update

# Or in one command:
git submodule update --init --recursive
```

### 21.3 Clone a Repo with Submodules

```bash
git clone --recurse-submodules <repo-url>
```

### 21.4 Update Submodules to Latest

```bash
git submodule update --remote
```

> ⚠️ Submodules add complexity. Make sure your team understands how they work before using them.

---

## 22. 🧹 Git Clean

`git clean` removes **untracked files** from your working directory.

### 22.1 Dry Run (Preview What Will Be Deleted)

```bash
git clean -n            # Show what would be removed (no actual deletion)
git clean -nd           # Include directories in preview
```

### 22.2 Delete Untracked Files

```bash
git clean -f            # Delete untracked files
git clean -fd           # Delete untracked files AND directories
git clean -fX           # Delete only ignored files
git clean -fx           # Delete all untracked + ignored files
```

> ⚠️ **Warning:** `git clean -f` permanently deletes files. Always run `git clean -n` first to preview.

---

## 23. 🐛 Git Bisect

Git Bisect uses **binary search** to find the exact commit that introduced a bug. Instead of manually checking each commit, Git narrows it down in O(log n) steps.

### 23.1 Start Bisect

```bash
git bisect start
git bisect bad              # Mark current commit as broken
git bisect good <commit>    # Mark a known-good commit
```

Git will now checkout a commit halfway between good and bad for you to test.

### 23.2 During Bisect — Mark Each Commit

```bash
git bisect good    # If this commit is fine
git bisect bad     # If this commit has the bug
```

Git continues narrowing down until it identifies the **first bad commit**.

### 23.3 End Bisect

```bash
git bisect reset   # Return to original HEAD
```

### 💡 Example Workflow

```bash
git bisect start
git bisect bad                    # Current version is broken
git bisect good v1.0              # v1.0 was working fine

# Git checks out a commit halfway — you test it
# Repeat: git bisect good / git bisect bad
# Git prints: "a1b2c3d is the first bad commit"

git bisect reset                  # Done! Back to original state
```

---

## 24. 🙈 Git Ignore

A `.gitignore` file tells Git which files and directories to **exclude from tracking**.

### 24.1 Create and Commit a .gitignore

```bash
touch .gitignore
git add .gitignore
git commit -m "Add .gitignore"
```

### 24.2 Common .gitignore Patterns

```gitignore
# 📄 Specific file
myfile.txt
secrets.json

# 🔠 All files with an extension
*.log
*.mov
*.class
*.pyc

# 📁 Directories
node_modules/
build/
dist/
__pycache__/

# 🔐 Environment and secrets
.env
.env.local
.env.production

# 💻 OS files
.DS_Store
Thumbs.db

# 🛠️ IDE files
.vscode/
.idea/
*.swp
```

### 24.3 Untrack a Previously Tracked File

```bash
git rm --cached <file-name>    # Untrack without deleting locally
git commit -m "Stop tracking <file>"
```

> 📝 Add files to `.gitignore` **before** committing them. If already tracked, use `git rm --cached`.

---

## 25. 🔬 Git Cat-File

`git cat-file` is a low-level command for inspecting objects in Git's internal database.

### Git's Internal Object Model

```
📦 Commit
    └── 📂 Tree  (directory snapshot)
          ├── 📄 Blob  (file content)
          ├── 📄 Blob  (file content)
          └── 📂 Tree  (subdirectory)
                └── 📄 Blob  (file content)
```

| Object | Description |
|--------|-------------|
| 📦 **Commit** | Root node; points to a tree and stores metadata (author, message, parent) |
| 📂 **Tree** | Represents a directory; contains pointers to blobs and other trees |
| 📄 **Blob** | Leaf node; stores the actual raw file content |

### 25.1 Commands

```bash
git cat-file -t <object-hash>    # Show object type (commit/tree/blob)
git cat-file -p <object-hash>    # Show object content
git cat-file -s <object-hash>    # Show object size in bytes
```

### 25.2 Example Workflow

```bash
git log --oneline                    # Get a commit hash
git cat-file -p <commit-hash>        # → tree hash, parent, author, message
git cat-file -p <tree-hash>          # → list of blobs and sub-trees
git cat-file -p <blob-hash>          # → raw file content
```

---

## 26. 🧠 Git Internals (Advanced)

### 26.1 📁 The `.git` Folder Structure

When you run `git init`, Git creates a `.git/` directory:

```
.git/
├── HEAD            → Points to the current branch (e.g., refs/heads/main)
├── config          → Local repository configuration
├── objects/        → All Git objects (commits, trees, blobs)
│   ├── pack/       → Packed objects for efficiency
│   └── info/
├── refs/
│   ├── heads/      → Branch pointers (refs/heads/main, etc.)
│   └── tags/       → Tag pointers
├── hooks/          → Git hook scripts
├── index           → The staging area (binary file)
└── COMMIT_EDITMSG  → Last commit message
```

### 26.2 🔑 Git Objects & SHA-1 Hashing

Every object in Git (commit, tree, blob) is stored by its **SHA-1 hash** — a 40-character hex string derived from the content. This ensures integrity: the same content always produces the same hash.

```bash
# Compute the SHA-1 hash Git would assign to a file:
git hash-object <file-name>

# Write an object to the database:
git hash-object -w <file-name>
```

### 26.3 👉 The HEAD Pointer

`HEAD` is a special file in `.git/HEAD` that points to the **current branch reference**.

```bash
cat .git/HEAD
# Output: ref: refs/heads/main

# In detached HEAD state (points directly to a commit):
# Output: a1b2c3d4e5f6...
```

### 26.4 🔗 Refs (References)

Refs are human-readable names pointing to specific commits.

```bash
# View all refs:
git show-ref

# Branch refs:
cat .git/refs/heads/main       # SHA of the latest commit on main

# Tag refs:
cat .git/refs/tags/v1.0
```

---

## 27. 🔗 Git Upstream

**Upstream** refers to the remote repository your local branch tracks — typically the original repo from which you cloned.

### 27.1 Set Upstream for a Branch

```bash
git push --set-upstream origin <branch-name>
# Shorthand:
git push -u origin <branch-name>
```

### 27.2 Check Upstream Branch

```bash
git branch -vv
# Output: * main a1b2c3d [origin/main] Last commit message
```

### 27.3 Fetch Changes from Upstream

Downloads changes **without** merging them into your local branch.

```bash
git fetch upstream
```

### 27.4 Pull Changes from Upstream

Fetches and merges changes from the upstream branch.

```bash
git pull upstream <branch-name>
```

### 27.5 Push Changes to Your Fork

```bash
git push origin main
```

### 🔄 Fork Workflow Diagram

```
📦 Original Repo (upstream)
        │
        │  🍴 fork (GitHub UI)
        ▼
📦 Your Fork (origin)  ◄──── git push origin main ◄───┐
        │                                               │
        │  git clone                                    │
        ▼                                               │
💻 Local Repository ──── work + commit ────────────────┘
```

---

## 28. ⚙️ Git Config Levels

Git configuration works in three levels, each overriding the one above it:

| Level | 🎯 Scope | 📄 File Location |
|-------|---------|----------------|
| `--system` | All users on the machine | `/etc/gitconfig` |
| `--global` | Current user (all repos) | `~/.gitconfig` |
| `--local` | Current repository only | `.git/config` |

### 28.1 Set Config at Each Level

```bash
git config --system core.editor "vim"       # System-wide
git config --global user.name "Your Name"   # Your user
git config --local user.email "work@co.com" # This repo only
```

### 28.2 View Config with Origins

```bash
git config --list --show-origin
# Shows each setting AND which file it comes from
```

### 28.3 Edit Config File Directly

```bash
git config --global --edit    # Opens ~/.gitconfig in your editor
git config --local --edit     # Opens .git/config in your editor
```

---

## 29. 🔁 Pull Request Workflow

A **Pull Request (PR)** is the standard way to contribute code to a shared repository. It enables code review, discussion, and controlled merging.

### 29.1 Complete PR Workflow

```
1. 🍴 Fork the Repository      → GitHub: click "Fork"
2. 📥 Clone Your Fork          → git clone <your-fork-url>
3. 🌿 Create a Branch          → git checkout -b feature/my-feature
4. ✏️  Make Changes & Commit    → git add . && git commit -m "feat: add feature"
5. 📤 Push to Your Fork        → git push origin feature/my-feature
6. 🔁 Open a Pull Request      → GitHub: "Compare & pull request"
7. 👀 Code Review              → Team reviews, comments, requests changes
8. ✅ Approval & Merge         → PR merged into main branch
9. 🧹 Clean Up                 → Delete the feature branch
```

### 29.2 Commands

```bash
# Step 2: Clone
git clone <your-fork-url>
cd <project-folder>

# Step 3: Branch
git checkout -b feature/my-feature

# Step 4: Commit
git add .
git commit -m "feat: add my feature"

# Step 5: Push
git push origin feature/my-feature

# Step 9: Clean up after merge
git checkout main
git pull upstream main                       # Sync with original repo
git branch -d feature/my-feature
git push origin --delete feature/my-feature
```

### 29.3 Keeping Your Fork in Sync

```bash
# Add the original repo as upstream (one-time setup):
git remote add upstream <original-repo-url>

# Sync your fork:
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

### 29.4 ✅ PR Best Practices

| ✅ Do | ❌ Avoid |
|-------|---------|
| Keep PRs small and focused | Giant PRs with 50+ files changed |
| Write a clear PR description | Empty or vague descriptions |
| Reference related issues | Opening PRs to unrelated branches |
| Respond to review comments promptly | Ignoring reviewer feedback |
| Test your code before opening | Pushing broken or untested code |

---

## 30. ⚡ Quick Reference Cheat Sheet

### 🛠️ Setup

| Command | Description |
|---------|-------------|
| `git init` | Initialize a new local repository |
| `git clone <url>` | Clone a remote repository |
| `git config --global user.name "Name"` | Set global username |
| `git config --global user.email "email"` | Set global email |
| `git config --list` | View all configuration |

### 📝 Everyday Commands

| Command | Description |
|---------|-------------|
| `git status` | Show working directory status |
| `git add <file>` | Stage a specific file |
| `git add .` | Stage all changes |
| `git commit -m "msg"` | Commit staged changes |
| `git commit --amend` | Edit the last commit |
| `git diff` | Show unstaged changes |
| `git diff --staged` | Show staged changes |

### 🌿 Branching

| Command | Description |
|---------|-------------|
| `git branch` | List local branches |
| `git branch <n>` | Create a new branch |
| `git checkout -b <n>` | Create and switch to a branch |
| `git switch <n>` | Switch to a branch (modern) |
| `git merge <n>` | Merge a branch into current |
| `git branch -d <n>` | Delete a branch (safe) |
| `git rebase <branch>` | Rebase current branch onto another |
| `git cherry-pick <hash>` | Apply a specific commit |

### 🌐 Remote

| Command | Description |
|---------|-------------|
| `git remote -v` | List remote connections |
| `git remote add origin <url>` | Add a remote |
| `git fetch origin` | Fetch changes (no merge) |
| `git pull origin <branch>` | Pull and merge remote changes |
| `git push origin <branch>` | Push local changes to remote |
| `git push -u origin <branch>` | Push and set upstream |

### ↩️ Undoing Changes

| Command | Description |
|---------|-------------|
| `git restore <file>` | Discard working directory changes |
| `git restore --staged <file>` | Unstage a file |
| `git reset --soft HEAD~1` | Undo commit, keep staged |
| `git reset --mixed HEAD~1` | Undo commit, keep in working dir |
| `git reset --hard HEAD~1` | ⚠️ Undo commit, discard all changes |
| `git revert <hash>` | New commit that safely undoes a previous one |

### 📦 Stash

| Command | Description |
|---------|-------------|
| `git stash` | Temporarily save uncommitted changes |
| `git stash -u` | Stash including untracked files |
| `git stash list` | View all stashes |
| `git stash pop` | Restore and remove most recent stash |
| `git stash apply` | Restore stash (keep in list) |
| `git stash drop` | Delete a stash |
| `git stash clear` | Delete all stashes |

### 🏷️ Tags

| Command | Description |
|---------|-------------|
| `git tag` | List all tags |
| `git tag v1.0` | Create a lightweight tag |
| `git tag -a v1.0 -m "msg"` | Create an annotated tag |
| `git push origin v1.0` | Push a tag to remote |
| `git push origin --tags` | Push all tags |
| `git tag -d v1.0` | Delete a local tag |

### 🔍 Inspection & Debugging

| Command | Description |
|---------|-------------|
| `git log --oneline --graph --all` | Visual branch history |
| `git log --author="name"` | Filter commits by author |
| `git diff branch1 branch2` | Compare two branches |
| `git bisect start` | Start binary search for a bug |
| `git blame <file>` | Show who changed each line |
| `git show <hash>` | Show a specific commit's details |
| `git clean -n` | Preview untracked file removal |
| `git clean -fd` | Remove untracked files and folders |

---

> 💡 **Pro Tip:** When in doubt, `git status` is your best friend — it tells you exactly where you are and what to do next.

> 🌟 **Golden Rule:** Commit early, commit often. Small, focused commits make your history readable and debugging much easier.

---

*📘 Made with ❤️ for developers learning Git — from zero to production-ready workflows.*
