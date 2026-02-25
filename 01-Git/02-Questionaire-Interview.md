# 🎯 Git Interview Questions & Answers

> 💼 A comprehensive collection of Git interview questions — from beginner to advanced — covering real-world scenarios asked in top tech companies in 2025.

---

## 📌 Table of Contents

| Level | Topics |
|-------|--------|
| 🟢 [Beginner](#-beginner-questions) | Q1–Q10: Fundamentals, basic commands, commits |
| 🟡 [Intermediate](#-intermediate-questions) | Q11–Q22: Branching, merge vs rebase, stash, reset |
| 🔴 [Advanced](#-advanced-questions) | Q23–Q35: Internals, CI/CD, workflows, real scenarios |
| 🏢 [Scenario-Based](#-scenario-based--hr-questions) | Q36–Q45: "What would you do if...", org workflow |

---

## 🟢 Beginner Questions

---

### Q1. 📌 What is Git? How is it different from other VCS?

**Ans:**
Git is a **free, open-source Distributed Version Control System (DVCS)** created by **Linus Torvalds in 2005**. It tracks changes in source code, supports collaboration between multiple developers, and allows reverting to previous versions.

**Key differences from other VCS (e.g., SVN):**

| Feature | Git (DVCS) | SVN (CVCS) |
|---------|-----------|------------|
| Repository | Every developer has a full local copy | Single central repository |
| Offline work | ✅ Full offline capability | ❌ Needs network for most ops |
| Branching | Lightweight, fast | Slower, more complex |
| Speed | ⚡ Fast (local ops) | 🐢 Slower (server-dependent) |
| Backup | Every clone is a backup | Single point of failure |

---

### Q2. 🗂️ What is a Repository in Git?

**Ans:**
A **repository (repo)** is the directory where Git stores all project files and their complete history. It contains:
- All committed files and folders
- The entire commit history
- Branch information
- A hidden `.git/` folder with all metadata

```bash
git init        # Create a new local repo
git clone <url> # Copy an existing remote repo
```

---

### Q3. 📸 What is a Commit in Git?

**Ans:**
A **commit** is a snapshot of changes made in a repository at a specific point in time. Each commit contains:

- 🕐 **When** — timestamp of the change
- 👤 **Who** — author name and email
- 📝 **What** — the actual file changes
- 💬 **Message** — description of the change
- 🔑 **Unique ID** — a SHA-1 hash (e.g., `a1b2c3d`)

```bash
git commit -m "Add login functionality"

# View commit history:
git log
git log --oneline
```

---

### Q4. 🔑 What is the difference between `git pull` and `git fetch`?

**Ans:**

| Command | What it does |
|---------|-------------|
| `git fetch` | Downloads changes from remote **without** merging into your branch |
| `git pull` | Downloads **AND** automatically merges changes into your current branch |

`git pull` = `git fetch` + `git merge`

```bash
git fetch origin         # Download, but don't merge
git pull origin main     # Download and merge immediately
```

> 💡 **Best practice:** Use `git fetch` first to review what changed, then `git merge` manually. This gives you more control.

---

### Q5. 🌿 What is a Branch in Git? Why do we use it?

**Ans:**
A **branch** is an independent line of development. It allows developers to work on features, bug fixes, or experiments **in isolation** without affecting the main codebase.

```bash
git branch feature/login      # Create branch
git checkout -b feature/login  # Create and switch
git branch -a                  # List all branches
git branch -d feature/login    # Delete branch
```

**Why use branches?**
- ✅ Parallel development without conflicts
- ✅ Safe experimentation
- ✅ Clean code reviews via Pull Requests
- ✅ Easy rollback if something breaks

---

### Q6. 🙈 What is `.gitignore`? When and why is it used?

**Ans:**
`.gitignore` is a file that tells Git **which files and folders to exclude** from version control tracking.

**Common use cases:**

```gitignore
node_modules/      # Dependencies (huge, auto-generated)
.env               # Secrets and API keys
*.log              # Log files
build/             # Compiled output
.DS_Store          # macOS system file
```

```bash
touch .gitignore
git add .gitignore
git commit -m "Add .gitignore"
```

> ⚠️ **Important:** If a file was already committed, add it to `.gitignore` AND run `git rm --cached <file>` to untrack it.

---

### Q7. 🔍 What is the difference between `git clone` and `git fork`?

**Ans:**

| | `git clone` | Fork |
|--|------------|------|
| **What it does** | Creates a local copy of any repo | Creates your own copy on GitHub/GitLab |
| **Where** | On your local machine | On the remote server |
| **Use case** | Working locally on any repo | Contributing to someone else's project |
| **Connection** | Linked to original remote | Linked to your own remote copy |

```bash
# Clone (any repo to local):
git clone https://github.com/user/repo.git

# After forking on GitHub, clone your fork:
git clone https://github.com/YOUR-USERNAME/repo.git
```

---

### Q8. 📂 Explain the three areas/stages in Git.

**Ans:**
Git has three main stages a file can exist in:

```
Working Directory  ──git add──►  Staging Area  ──git commit──►  Repository
  (Untracked /                    (Index)                       (Committed)
   Modified)
```

| Stage | Description |
|-------|-------------|
| 🗂️ **Working Directory** | Where you edit files on your local machine |
| 🎭 **Staging Area (Index)** | Where you prepare/select changes before committing |
| 📦 **Repository (.git)** | Where committed snapshots are permanently stored |

---

### Q9. ❓ What is `HEAD` in Git?

**Ans:**
`HEAD` is a **special pointer** that points to the **current commit** in your active branch. It tells Git "this is where you are right now."

```bash
cat .git/HEAD
# Output: ref: refs/heads/main  ← pointing to main branch

# Detached HEAD: HEAD points directly to a commit (not a branch)
git checkout a1b2c3d    # Now in detached HEAD state
```

> ⚠️ In **detached HEAD** state, any commits you make won't belong to any branch and can be lost. Always create a branch if you plan to commit.

---

### Q10. 🔗 What is `origin` in Git?

**Ans:**
`origin` is the **default name** Git gives to the remote repository when you clone or add a remote. It's simply an alias for the remote URL.

```bash
git remote add origin https://github.com/user/repo.git
git remote -v
# Output: origin  https://github.com/user/repo.git (fetch)
#         origin  https://github.com/user/repo.git (push)

git push origin main    # Push to the remote named "origin"
```

You can rename it or have multiple remotes (e.g., `upstream` for the original repo when working with forks).

---

## 🟡 Intermediate Questions

---

### Q11. 📌 On which branch is `git rebase` performed?

**Ans:**
`git rebase` is performed **on a local/feature branch** to re-apply its commits on top of another branch (usually `master`/`main`).

```bash
git checkout feature/login
git rebase master          # Reapply feature commits on top of master
```

**What it does:**
- Takes commits from your feature branch
- Temporarily removes them
- Updates your branch to match master
- Re-applies your commits on top — resulting in a **linear history**

> ✅ Use rebase on **private/local branches** only. Never rebase shared public branches.

---

### Q12. 🔀 What is the difference between `git merge` and `git rebase`?

**Ans:**

| | `git merge` | `git rebase` |
|--|------------|--------------|
| **New commit?** | ✅ Yes — creates a merge commit | ❌ No — rewrites commit history |
| **History** | Non-linear (preserves branch history) | Linear (clean, straight history) |
| **Best for** | 🌐 Public/shared branches | 🔒 Local/private branches |
| **Safety** | ✅ Safe — never rewrites history | ⚠️ Risky on shared branches |
| **Use case** | Merging `develop` into `main` | Cleaning up feature branch commits |

```bash
# Merge:
git checkout main
git merge feature/login          # Creates a merge commit

# Rebase:
git checkout feature/login
git rebase main                  # Reapplies commits on top of main
```

> 💡 **Golden rule:** "Rebase locally, merge publicly."

---

### Q13. 🔄 What are the three types of `git reset`?

**Ans:**

| Type | HEAD | Staging Area | Working Directory | Use Case |
|------|------|:------------:|:-----------------:|---------|
| `--soft` | ✅ Moves | Unchanged | Unchanged | Undo commit, keep changes staged |
| `--mixed` | ✅ Moves | 🔄 Reset | Unchanged | Undo commit + unstage, keep files |
| `--hard` | ✅ Moves | 🔄 Reset | 🔄 Reset | ⚠️ Discard everything completely |

```bash
git reset --soft HEAD~1    # Undo last commit, keep changes staged
git reset --mixed HEAD~1   # Undo last commit, unstage changes
git reset --hard HEAD~1    # ⚠️ Undo last commit, DELETE all changes
```

> ⚠️ Never use `git reset --hard` on commits already pushed to a remote shared branch.

---

### Q14. ↩️ How do you rollback to a specific commit?

**Ans:**

**Method 1 — `git revert` (Safe, creates new commit):**

```bash
git log --oneline          # Find the commit hash
git revert <commit-hash>   # Creates a new "undo" commit
```

Best for: **Public/shared branches** — preserves history, safe for teams.

**Method 2 — `git reset` (Destructive, deletes history):**

```bash
git reset --hard <commit-hash>   # Resets to that commit, deletes newer ones
```

Best for: **Local/private branches** only — history is permanently rewritten.

**Method 3 — `git checkout` (Temporary, read-only):**

```bash
git checkout <commit-hash>               # View old state (detached HEAD)
git checkout -b hotfix/old-state <hash>  # Create new branch from old commit
```

---

### Q15. ⏳ When should you use `git stash`?

**Ans:**
`git stash` **temporarily saves uncommitted changes** without creating a commit, allowing you to switch branches or pull updates without losing work in progress.

**Use cases:**
- 🚨 Urgent bug fix needed while mid-feature development
- 🔀 Need to switch to another branch quickly
- 📥 Want to pull latest changes before committing your work

```bash
git stash                   # Save current WIP
git checkout main           # Switch to another branch
# Fix bug, commit, come back
git checkout feature/login
git stash pop               # Restore your WIP

git stash list              # View all stashes
git stash apply stash@{1}   # Apply a specific stash
git stash drop              # Delete the most recent stash
```

---

### Q16. 🤔 What is the difference between `git revert` and `git reset`?

**Ans:**

| | `git revert` | `git reset` |
|--|-------------|------------|
| **History** | ✅ Preserved (adds new commit) | ❌ Rewritten (removes commits) |
| **New commit?** | Yes — a "revert commit" | No |
| **Safe for teams?** | ✅ Yes | ⚠️ No (shared branches) |
| **Use when** | Undoing public/shared commits | Cleaning up local history |

**Example scenario:**
Suppose you have commits: `c1 → c2 → c3 → c4 → c5`

- `git revert c3` → Creates `c6` that undoes c3's changes. History: `c1 → c2 → c3 → c4 → c5 → c6`
- `git reset --hard c3` → History becomes: `c1 → c2 → c3` (c4, c5 are **deleted**)

---

### Q17. 🍒 What is `git cherry-pick`?

**Ans:**
`git cherry-pick` applies a **specific commit from one branch to another** — without merging the entire branch.

```bash
git log develop --oneline       # Find the commit hash you want
git checkout main
git cherry-pick a1b2c3d          # Apply that specific commit to main
```

**Use case:**
- A bug was fixed on `develop` but needs to go to `main` immediately
- You want only one specific feature commit, not the full branch

> ⚠️ Cherry-picking creates a **new commit** with a different SHA. Overusing it can create duplicate commits and confuse history.

---

### Q18. 🏷️ What are Git Tags? Difference between lightweight and annotated?

**Ans:**
Tags mark **specific important points** in history — commonly used for version releases.

| Type | Description | Command |
|------|-------------|---------|
| 🪶 **Lightweight** | Just a pointer to a commit. No metadata. | `git tag v1.0` |
| 📋 **Annotated** | Full object: tagger, date, message, GPG signature | `git tag -a v1.0 -m "First release"` |

```bash
git tag -a v1.0 -m "Production release 1.0"
git push origin v1.0          # Push specific tag
git push origin --tags         # Push all tags
git tag -d v1.0               # Delete local tag
```

> ✅ **Always use annotated tags for releases** — they carry more information and can be signed.

---

### Q19. 📁 How does Git track whether a file is executable?

**Ans:**
Git tracks executable permissions via its internal file mode:

| Mode | Meaning |
|------|---------|
| `100644` | Normal (non-executable) file |
| `100755` | Executable file |
| `160000` | Gitlink (submodule) |

```bash
# Check file mode:
git ls-files --stage <file_name>
git ls-files --stage script.py

# Output for executable:     100755 <hash> 0  script.py
# Output for non-executable: 100644 <hash> 0  script.py
```

This is controlled by the `core.fileMode` Git setting. If you `chmod +x` a file, Git will detect the permission change and show the file as **modified** in `git status`.

> 📝 Git will **not** commit an empty directory.

---

### Q20. ⚠️ What is a Merge Conflict and how do you resolve it?

**Ans:**
A **merge conflict** occurs when two branches modify the **same lines** of the same file, and Git can't automatically determine which version to keep.

**When it happens:**
- 3-way merges where both branches changed the same code
- Rebasing with conflicting commits

**Conflict markers in the file:**

```
<<<<<<< HEAD
your changes on current branch
=======
incoming changes from other branch
>>>>>>> feature/login
```

**Resolution steps:**

```bash
git merge feature/login       # Conflict occurs
git status                    # Shows conflicted files

# 1. Open the conflicted file and manually resolve it
# 2. Remove all conflict markers (<<<, ===, >>>)
# 3. Keep the correct final code

git add <resolved-file>
git commit -m "Resolve merge conflict in login module"
```

> 💡 Use tools like **VS Code**, **IntelliJ**, or `git mergetool` for a visual conflict resolution experience.

---

### Q21. 🔍 What is `git diff`? Explain its variants.

**Ans:**
`git diff` shows differences between various states of your repository.

```bash
git diff                           # Unstaged changes vs last commit
git diff --staged                  # Staged changes vs last commit
git diff HEAD                      # All changes vs last commit

git diff branch1 branch2           # Compare two branches
git diff <commit1> <commit2>       # Compare two commits
git diff HEAD~1 HEAD               # Last two commits

git diff --stat                    # Summary of changes (file + line count)
git diff --name-only               # Only filenames that changed
```

> 💡 Always run `git diff --staged` before committing to review exactly what you're about to commit.

---

### Q22. 📜 How do you view commit history in Git?

**Ans:**

```bash
git log                            # Full detailed history
git log --oneline                  # Compact one-line per commit
git log --oneline --graph          # ASCII branch graph
git log --oneline --graph --all    # All branches visualized
git log --author="John"            # Filter by author
git log --since="2024-01-01"       # Commits after a date
git log --grep="bugfix"            # Search commit messages
git log -p -- <file>               # Changes to a specific file

# ⭐ Best all-in-one view:
git log --oneline --graph --all --decorate
```

---

## 🔴 Advanced Questions

---

### Q23. 🧠 Explain Git's internal object model.

**Ans:**
Git stores data as an **inverted tree** of objects, each identified by a SHA-1 hash:

```
📦 Commit Object
    └── 📂 Tree Object  (snapshot of directory)
          ├── 📄 Blob Object  (file content)
          ├── 📄 Blob Object
          └── 📂 Tree Object  (subdirectory)
                └── 📄 Blob Object
```

| Object | Purpose |
|--------|---------|
| **Commit** | Metadata: author, message, timestamp, pointer to tree + parent commit |
| **Tree** | Represents a directory; lists blobs and sub-trees |
| **Blob** | Raw file content (no filename — that's stored in the tree) |
| **Tag** | Annotated tag object pointing to a commit |

```bash
git cat-file -t <hash>    # Show type: commit / tree / blob
git cat-file -p <hash>    # Show content
git hash-object <file>    # Compute SHA-1 of a file
```

---

### Q24. 🔁 What is an Interactive Rebase? When would you use it?

**Ans:**
Interactive rebase (`git rebase -i`) lets you **edit, reorder, squash, or drop commits** before pushing them.

```bash
git rebase -i HEAD~4    # Interactively edit last 4 commits
```

**Options in the editor:**

| Command | Action |
|---------|--------|
| `pick` | Keep commit as-is |
| `reword` | Change commit message |
| `squash` | Merge into previous commit |
| `fixup` | Merge silently (discard message) |
| `drop` | Delete the commit |
| `edit` | Pause to amend the commit |

**Common use cases:**
- 🧹 Clean up messy "WIP" commits before opening a PR
- 📝 Fix typos in commit messages
- 🗜️ Squash 10 small commits into 1 meaningful commit
- 🗑️ Remove a commit that accidentally included secrets

---

### Q25. ⚡ What is `git reflog`? When is it useful?

**Ans:**
`git reflog` records **every movement of HEAD** — even after resets, rebases, or deleted branches. It's your **safety net** for recovering "lost" commits.

```bash
git reflog
# Output:
# a1b2c3d HEAD@{0}: commit: Add login feature
# e4f5g6h HEAD@{1}: reset: moving to HEAD~2
# i7j8k9l HEAD@{2}: commit: Fix typo

# Recover a commit you accidentally reset:
git checkout HEAD@{2}              # Inspect it
git checkout -b recovery-branch    # Save it to a new branch
```

> 💡 By default, reflog entries are kept for **90 days**. This is your emergency undo button.

---

### Q26. 🔒 What is `git push --force` vs `git push --force-with-lease`?

**Ans:**

| | `--force` | `--force-with-lease` |
|--|-----------|---------------------|
| **What it does** | Overwrites remote branch completely | Overwrites only if no one else has pushed since your last fetch |
| **Risk** | ⚠️ Can overwrite teammates' work | ✅ Safer — fails if remote has new commits |
| **Use case** | Never on shared branches | After rebasing a feature branch |

```bash
git push --force origin feature/login              # ⚠️ Dangerous
git push --force-with-lease origin feature/login   # ✅ Safer
```

> ✅ **Always prefer `--force-with-lease`** over `--force` when you must force-push (e.g., after an interactive rebase).

---

### Q27. 🔎 What is `git bisect`? How does it work?

**Ans:**
`git bisect` uses **binary search** to find the exact commit that introduced a bug. It's far faster than checking commits one by one.

```bash
git bisect start
git bisect bad                   # Current HEAD is broken
git bisect good v1.0             # v1.0 was working

# Git checks out a middle commit for you to test
# Test the behavior, then mark it:
git bisect good    # OR
git bisect bad

# Repeat until Git identifies: "a1b2c3d is the first bad commit"
git bisect reset   # Return to original state
```

**Why it's powerful:** For 1,000 commits, you'd normally check all 1,000. With bisect, you find the bad commit in just **~10 steps** (log₂ 1000 ≈ 10).

---

### Q28. 🎣 What are Git Hooks? Give real examples.

**Ans:**
Git Hooks are **scripts that run automatically** at specific Git events. They live in `.git/hooks/` and are not committed to the repo by default.

```bash
.git/hooks/pre-commit       # Runs before every commit
.git/hooks/commit-msg       # Runs after commit message is entered
.git/hooks/pre-push         # Runs before git push
.git/hooks/post-merge       # Runs after a merge
```

**Real-world examples:**

```bash
# pre-commit: Block commits with debug code
#!/bin/sh
if grep -r "console.log\|debugger" src/; then
  echo "❌ Remove debug statements before committing!"
  exit 1
fi

# commit-msg: Enforce JIRA ticket format (e.g., PROJ-123: message)
#!/bin/sh
if ! grep -qE "^[A-Z]+-[0-9]+: .+" "$1"; then
  echo "❌ Commit message must start with JIRA ticket: PROJ-123: description"
  exit 1
fi
```

> 💡 Use **Husky** for Node.js projects to share hooks across teams via `package.json`.

---

### Q29. 📎 What are Git Submodules? When would you use them?

**Ans:**
Submodules allow you to **embed one Git repository inside another** as a dependency.

```bash
git submodule add https://github.com/org/shared-lib.git libs/shared
git submodule update --init --recursive    # Initialize after clone
git clone --recurse-submodules <url>       # Clone with submodules
```

**Use cases:**
- Shared utility library used across multiple projects
- External dependency you want to pin to a specific commit
- Monorepo-like setup where components have their own repos

> ⚠️ Submodules are powerful but complex. Team members must run `git submodule update` after pulling. Many teams prefer **npm packages**, **Git subtrees**, or monorepo tools instead.

---

### Q30. 🌐 What is the difference between `git pull --rebase` and `git pull`?

**Ans:**

```bash
git pull             # fetch + merge  → creates a merge commit
git pull --rebase    # fetch + rebase → linear history, no merge commit
```

**`git pull --rebase` is preferred when:**
- You want a clean, linear commit history
- Working on a feature branch and want to sync with main without extra merge commits
- Your team follows a "rebase-based" workflow

```bash
# Set rebase as default for all pulls:
git config --global pull.rebase true
```

---

### Q31. 🔐 How does Git ensure data integrity?

**Ans:**
Git uses **SHA-1 hashing** (40-character hex) to generate a unique ID for every object (commit, tree, blob). The hash is computed from the **content itself**.

- If even one byte changes, the hash changes completely
- Every commit references its parent's hash — forming a **tamper-evident chain**
- You cannot silently alter committed history without changing all subsequent hashes

```bash
git hash-object <file>           # See the SHA-1 Git would assign
git cat-file -t <hash>           # Verify object type
git fsck                         # Check repo for corruption
```

---

### Q32. 🧹 What is `git clean` and when would you use it?

**Ans:**
`git clean` removes **untracked files** (files Git doesn't know about) from the working directory.

```bash
git clean -n          # 🔍 Dry run: preview what would be deleted
git clean -f          # Delete untracked files
git clean -fd         # Delete untracked files AND directories
git clean -fX         # Delete only Git-ignored files
```

**Use cases:**
- After a build that generated junk files
- Resetting to a completely clean state
- Before switching tasks on a messy repo

> ⚠️ Always run `git clean -n` first! Deleted files cannot be recovered.

---

### Q33. ⚙️ Explain Git Config levels.

**Ans:**

| Level | Scope | Location | Override Priority |
|-------|-------|----------|-----------------|
| `--system` | All users on the machine | `/etc/gitconfig` | Lowest |
| `--global` | Current user, all repos | `~/.gitconfig` | Medium |
| `--local` | Current repo only | `.git/config` | Highest ✅ |

```bash
git config --global user.name "John"          # All repos
git config --local user.email "work@co.com"   # This repo only

git config --list --show-origin               # View all + file source
```

---

### Q34. 🔁 What is a bare repository? Where is it used?

**Ans:**
A **bare repository** contains only the Git data (`.git/` contents) with **no working directory**. It's meant for sharing — not direct editing.

```bash
git init --bare myproject.git
```

**Used for:**
- Central shared repositories on servers (like what GitHub/GitLab serves)
- CI/CD servers that only need the Git data, not the actual files
- Self-hosted Git servers

> 💡 When you `git clone` from GitHub, you're cloning from a bare repository on their servers.

---

### Q35. 🔄 What is `git stash pop` vs `git stash apply`?

**Ans:**

| Command | What it does | Stash entry after? |
|---------|-------------|-------------------|
| `git stash pop` | Applies stash + **removes** it from list | ❌ Gone |
| `git stash apply` | Applies stash + **keeps** it in list | ✅ Still there |

```bash
git stash apply stash@{0}    # Apply but keep stash (safe to re-apply)
git stash pop                # Apply and remove (clean up)
```

> ✅ Use `apply` when you're unsure and want to keep the stash as a backup. Use `pop` when you're confident.

---

## 🏢 Scenario-Based & HR Questions

---

### Q36. 🏢 Which Git strategy does your organization use?

**Ans (Sample — Gitflow):**

In our organization, we primarily use the **Gitflow workflow** for managing structured releases.

**Branch structure:**

| Branch | Purpose |
|--------|---------|
| 🔵 `main` | Production-ready code. Only thoroughly tested code merges here. |
| 🟢 `develop` | Integration branch. All features merge here first. |
| 🌱 `feature/*` | Created from `develop`. One branch per feature. |
| 🟡 `release/*` | Created from `develop` when preparing for a release. |
| 🔴 `hotfix/*` | Created from `main` for emergency production fixes. |

**Our process:**
- Feature branches merge into `develop` via **Pull Requests** after code review
- Release branches are tested, then merged into both `main` and `develop`
- Hotfixes are merged into both `main` and `develop` immediately
- Every merge to `develop` triggers **CI/CD automated tests**
- Every merge to `main` triggers a **production deployment**

---

### Q37. ❓ How do you jump back to a previous commit on GitHub?

**Ans:**

```bash
# Step 1: View commit history
git log --oneline

# Step 2: Checkout the specific commit (read-only view)
git checkout <commit-hash>

# Step 3: (Optional) Create a new branch from that commit
git checkout -b rollback/v1.2 <commit-hash>

# Step 4: Or if you want to permanently reset to that point:
git reset --hard <commit-hash>    # ⚠️ local only — history lost
git revert <commit-hash>          # ✅ safe — creates new undo commit
```

---

### Q38. 🚨 What would you do if you accidentally committed sensitive data (e.g., API keys)?

**Ans:**

> This is a **critical security scenario** — act fast!

```bash
# If NOT yet pushed:
git reset --soft HEAD~1        # Undo commit, keep changes staged
# Remove the sensitive data from the file
git commit -m "Add config without secrets"

# If already pushed:
# 1. Revoke/rotate the leaked credentials IMMEDIATELY
# 2. Remove from history using BFG Repo Cleaner (recommended):
bfg --replace-text secrets.txt
git push --force-with-lease

# OR using git filter-branch (older method):
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch secrets.env" \
  --prune-empty --tag-name-filter cat -- --all
git push --force --all
```

> ⚠️ **First priority:** Always **rotate the exposed credentials** — assume they are compromised even if you fix the history. History rewrites don't help if someone already cloned the repo.

---

### Q39. 🤔 How do you handle a situation where two developers modified the same file?

**Ans:**

```bash
# Developer A and Developer B both edited auth.js

# When Developer B tries to merge:
git merge feature/auth-b     # ← Conflict!

# Git marks the conflict in auth.js:
# <<<<<<< HEAD (Developer A's version)
# =======
# >>>>>>> feature/auth-b (Developer B's version)

# Resolution steps:
# 1. Open the file, understand both changes
# 2. Manually merge the correct final version
# 3. Remove conflict markers
git add auth.js
git commit -m "Resolve conflict in auth.js — merged both auth flows"
```

**Prevention:**
- Communicate which files each person is working on
- Keep features small and short-lived
- Regularly sync feature branches with `develop`

---

### Q40. 🤝 What is a Pull Request? Walk me through the process.

**Ans:**
A **Pull Request (PR)** is a formal request to merge code from one branch to another, enabling **code review** before merging.

**Full workflow:**

```
1. 🍴 Fork (if open-source) or create feature branch
2. ✏️  Write code + commit
3. 📤 Push branch to remote
4. 🔁 Open PR on GitHub/GitLab
5. 👀 Team reviews → comments, suggestions
6. ✅ Make requested changes, push again
7. ✅ Approval → Merge
8. 🧹 Delete feature branch
```

```bash
git checkout -b feature/payment-gateway
# ... code, commit ...
git push origin feature/payment-gateway
# → Open PR on GitHub
# → After approval:
git checkout main
git pull origin main
git branch -d feature/payment-gateway
```

---

### Q41. 💥 What is a detached HEAD state? How do you fix it?

**Ans:**
**Detached HEAD** occurs when `HEAD` points directly to a commit instead of a branch. This happens when you `git checkout <commit-hash>`.

```
Normal:    HEAD → main → commit
Detached:  HEAD → commit (no branch!)
```

Any commits made in detached HEAD state are **orphaned** and can be lost.

```bash
# Fix: Create a branch to "save" your current position
git checkout -b recovery-branch

# Or: Return to the main branch (losing detached commits)
git checkout main

# Check if you're in detached HEAD:
git status    # Shows "HEAD detached at a1b2c3d"
```

---

### Q42. 🗑️ How do you delete a remote branch?

**Ans:**

```bash
git push origin --delete <branch-name>
# OR:
git push origin :<branch-name>          # Old syntax

# Also delete locally:
git branch -d <branch-name>

# Prune stale remote-tracking references:
git remote prune origin
git fetch --prune
```

---

### Q43. 🔐 What is `git blame`? When is it useful?

**Ans:**
`git blame` shows **who last modified each line** of a file and in which commit.

```bash
git blame <file-name>
git blame -L 10,25 <file-name>     # Lines 10–25 only

# Output format:
# <hash> (Author    Date    Line#) Content
# a1b2c3d (John Doe 2024-03-01 42) const handleLogin = () => {
```

**Use cases:**
- 🔎 Finding who introduced a bug
- 📋 Understanding why code was written a certain way
- 🤝 Code review context

---

### Q44. ⚡ What is `git fetch --prune`?

**Ans:**
`git fetch --prune` downloads new remote changes **and removes stale remote-tracking references** — i.e., cleans up branches that have been deleted on the remote but still appear locally.

```bash
git fetch --prune

# Set as default:
git config --global fetch.prune true

# Or prune without fetching:
git remote prune origin
```

> 💡 Over time, as branches are merged and deleted on remote, your local repo accumulates phantom remote-tracking branches. `--prune` keeps things clean.

---

### Q45. 🎓 What best practices do you follow with Git in a team?

**Ans:**

| Practice | Why |
|----------|-----|
| ✅ Write clear, descriptive commit messages | Easy to understand history |
| ✅ Commit small, focused changes | Easier to review and revert |
| ✅ Never force-push to `main`/`develop` | Protects shared history |
| ✅ Use `--force-with-lease` instead of `--force` | Prevents overwriting teammates' work |
| ✅ Always create feature branches | Keeps `main` stable |
| ✅ Regularly sync with the base branch | Reduces merge conflicts |
| ✅ Use `.gitignore` for build artifacts and secrets | Clean repo, no leaked credentials |
| ✅ Tag releases with annotated tags | Clear version history |
| ✅ Use PRs for all changes | Enforces code review |
| ✅ Set up CI on PR creation | Auto-test before merge |
| ✅ Use `git stash` for context switching | Never lose WIP |
| ✅ Use `git reflog` to recover lost work | Safety net |

---

## 📊 Quick Comparison Summary

### git reset vs revert vs checkout

| Command | Modifies History | Creates Commit | Safe on Shared? | Use For |
|---------|:---------------:|:--------------:|:---------------:|---------|
| `git reset --hard` | ✅ Yes | No | ❌ No | Local cleanup |
| `git revert` | No | ✅ Yes | ✅ Yes | Undoing public commits |
| `git checkout` | No | No | ✅ Yes | Viewing old state |

### merge vs rebase vs cherry-pick

| Command | Creates Merge Commit | Rewrites History | Use For |
|---------|:-------------------:|:----------------:|---------|
| `git merge` | ✅ Yes | No | Public branch integration |
| `git rebase` | No | ✅ Yes | Local branch cleanup |
| `git cherry-pick` | No | Partial | Specific commit from another branch |

### fetch vs pull vs clone

| Command | Downloads | Merges | Creates Local Repo |
|---------|:---------:|:------:|:-----------------:|
| `git clone` | ✅ Full repo | No | ✅ Yes |
| `git fetch` | ✅ Changes | No | No |
| `git pull` | ✅ Changes | ✅ Yes | No |

---

> 💡 **Interview Tip:** For every Git command you mention, be ready to explain **when NOT to use it** — that shows real-world experience.

> 🌟 **Key mindset:** Git is about **protecting history** and **enabling collaboration**. Every decision (merge vs rebase, reset vs revert) is about balancing safety with cleanliness.

---

*📘 Prepared for developers appearing in tech interviews — 2025 edition.*
