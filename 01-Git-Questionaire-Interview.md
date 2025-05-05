<br>
1. Git-Rebase is performed on which Branch ?
<br>Ans :- On Local Branch to Master

<br><br>
2. How does git recognize that if a file is normal file or an executable file ?
<br>Ans :- Git does track whether a file is executable through the core.fileMode setting, so if you want to check if a file is marked as executable in the Git repository (i.e., it has been committed with execute permissions), you can use git ls-files with -s (show the staged contents):

        git ls-files --stage <file_name>
        git ls-files --stage script.py

Output for Executable :-     100755 1234567890abcdef1234567890abcdef12345678 0       script.py
Output for non-Executable :- 100644
Also, while running command git commit -am "Commit-on-02",  it mentions the permission of the file.
Also, if we run chmod to any file, then also, the file will be marked as modified in git status.
For Directory, it will be create mode 160000. But git will not commit empty directory.

<br>
3. Commit in Git ?
<br>Ans :- Commit is a snapshot of changes made in a repo. Each commit has info of when the changes were made, what changes were made, who made the changes and a commit message.
To check commit history :- git log

<br><br>
4. How to rollback to specific commit ?
<br>Ans :-
<br>Method I : git revert -> New commit is created. New commit is called revert commit. Suppose, we have total 5 commit c1, c2, c3, c4, c5. If we revert to commit ID - c3, then new commit wil be created same as commit c3.
<br>Method II : git reset  -> Delete the commit history. No new commit is created. Suppose, we have total 5 commit c1, c2, c3, c4, c5. If we reset to commit ID - c3, then commit history of c4, c5 will be deleted. Used only when we want some specific commits to be deleted from commit history.

<br><br>
5. When to use git stash ?
<br>Ans :- Git stash is used to temporarily save changes made in a repo without commit them.
<br>This allows you to switch to another branches without losing current changes.

<br><br>
6. Difference between Git Merge and git rebase ?
<br>Ans :- <br>
git merge -> New commit is created (merge commit). Used in Public Branches. To merge changes between Dev branch and main branch, git merge is used.<br>
git rebase -> No new commit is created. To merge changes between different Private branches to avoid unnecessary extra commit IDs.

<br><br>
7. How to jump back to previous commit in different setup of Github.
<br>Ans :- Open your terminal: Navigate to the repository where you want to revert to a previous commit.
List your commits: Use git log to see the history of commits. This will show you the commit hashes you can revert to.

   	git log
Checkout the commit: Use the commit hash to checkout the specific commit you want to revert to.

	git checkout <commit-hash>
If you want to create a new branch from that commit, you can use:
	
 	git checkout -b <new-branch-name> <commit-hash>

<br><br>
8. Which Git Strategy you have used in organization ?
<br>Ans :- In our organization, we primarily use the **Gitflow workflow** strategy. This strategy is well-suited for managing large projects with multiple developers and ensures a structured approach to version control. Here’s how we implement it:

**Main Branches:**
Main (or master) branch: This is the stable branch where the production-ready code resides. Only thoroughly tested and approved changes are merged here.
develop branch: This branch is used for integrating features and is the base for all feature branches. It contains the latest delivered development changes for the next release.
**Supporting Branches:**

**Feature branches:** These branches are created from develop and are used to develop new features. Once a feature is complete, it is merged back into develop.

**Release branches:** When we are ready to prepare a new production release, a release branch is created from develop. This branch allows for final bug fixes and preparation for release.

**Hotfix branches:** These branches are created from main to address critical issues found in production. Once the hotfix is complete, it is merged back into both main and develop.

**Branching and Merging:**
Feature branches are merged into develop using pull requests (PRs) after code review.
Release branches are merged into main and develop once the release is ready.
Hotfix branches are merged into main and develop after the fix is applied.

**Continuous Integration/Continuous Deployment (CI/CD):**
We use CI/CD pipelines to automate testing and deployment. Every commit to develop triggers automated tests, and successful builds are deployed to staging environments.
Merges into main trigger deployments to production.
