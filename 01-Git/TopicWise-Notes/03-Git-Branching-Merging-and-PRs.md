# Branching, Merging, and Pull Requests

> Adapted from [01-Introduction.md](../01-Introduction.md)

This note preserves the original content on branching strategies, merging, and contributor workflows.

## 1. Branching Basics

Branching is one of Git’s most powerful features because it allows multiple streams of work to exist independently. This is essential for feature development, experimentation, and safe collaboration in team environments.

```bash
git branch <branch-name>
git checkout <branch-name>
git switch <branch-name>
git checkout -b <branch-name>
git switch -c <branch-name>
```

## 2. Listing and Deleting Branches

```bash
git branch
git branch -a
git branch -v
git branch -d <branch-name>
git branch -D <branch-name>
```

## 3. Fast-Forward Merge

When the base branch has not changed since the feature branch started, Git can merge by moving the branch pointer forward. This is the simplest and cleanest merge path.

```bash
git merge <branch-name>
```

## 4. Three-Way Merge and Merge Conflicts

When both branches have changed, Git must compare the common ancestor with both versions before combining them. This is called a three-way merge, and it may require human intervention when the same lines were edited differently.

When both the current branch and the base branch have new commits, Git may need a three-way merge.

```bash
# Example flow
mkdir my_Git_Project && cd my_Git_Project
git init
echo "initial content" > file.txt
git add file.txt
git commit -m "Initial commit on main"

git checkout -b feature
echo "Feature branch changes" >> file.txt
git commit -am "Added changes to feature branch"

git checkout master
echo "Master branch content" >> file.txt
git commit -am "Changes on master"

git merge feature
```

If conflicts appear, resolve the conflicting markers, then:

```bash
git add file.txt
git commit -m "Resolved merge conflict"
```

## 5. Working with Remotes

A remote is the shared version of the repository that others can access. Working with remotes allows local changes to be pushed, fetched, and synchronized across machines and teams.

```bash
git remote add origin <repository-url>
git remote -v
git push origin <branch-name>
git push -u origin <branch-name>
git pull origin <branch-name>
git fetch origin
git fetch --all
```

## 6. Pull Request Workflow

Pull requests are the standard way to propose changes in modern Git workflows. They provide a review process where teammates can inspect, discuss, and approve changes before merging them into the main branch.

```text
1. Fork the repository
2. Clone your fork
3. Create a branch
4. Commit changes
5. Push to your fork
6. Open a Pull Request
7. Review and merge
```

## 7. Workflow Strategies

Different project sizes and team structures require different Git workflow models. Choosing the right workflow helps reduce merge conflicts, improve collaboration, and make releases more predictable.

### Centralized Workflow

Best for small teams.

### Feature Branch Workflow

Best for most teams.

### Git Flow

Structured branching model for release management.

### Forking Workflow

Best for open-source projects.
