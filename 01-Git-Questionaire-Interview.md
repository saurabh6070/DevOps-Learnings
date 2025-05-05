1. Git-Rebase is performed on which Branch ?
Ans :- On Local Branch to Master

<br>
2. How does git recognize that if a file is normal file or an executable file ?
<br>Ans :- Git does track whether a file is executable through the core.fileMode setting, so if you want to check if a file is marked as executable in the Git repository (i.e., it has been committed with execute permissions), you can use git ls-files with -s (show the staged contents):

        git ls-files --stage <file_name>
        git ls-files --stage script.py

Output for Executable :-            100755 1234567890abcdef1234567890abcdef12345678 0       script.py
Output for non-Executable :-   100644
Also, while running command git commit -am "Commit-on-02",  it mentions the permission of the file.
Also, if we run chmod to any file, then also, the file will be marked as modified in git status.
For Directory, it will be create mode 160000. But git will not commit empty directory.

<br>
3. Commit in Git ?
<br>Ans :- Commit is a snapshot of changes made in a repo. Each commit has info of when the changes were made, what changes were made, who made the changes and a commit message.
To check commit history :- git log

<br>
4. How to rollback to specific commit ?
<br>Ans :-
<br>Method I : git revert -> New commit is created. New commit is called revert commit. Suppose, we have total 5 commit c1, c2, c3, c4, c5. If we revert to commit ID - c3, then new commit wil be created same as commit c3.
<br>Method II : git reset  -> Delete the commit history. No new commit is created. Suppose, we have total 5 commit c1, c2, c3, c4, c5. If we reset to commit ID - c3, then commit history of c4, c5 will be deleted. Used only when we want some specific commits to be deleted from commit history.

<br>
5. When to use git stash ?
<br>Ans :- Git stash is used to temporarily save changes made in a repo without commit them.
<br>This allows you to switch to another branches without losing current changes.

<br>
6. Difference between Git Merge and git rebase ?
<br>Ans :- 	git merge -> New commit is created (merge commit). Used in Public Branches. To merge changes between Dev branch and main branch, git merge is used.
				git rebase -> No new commit is created. To merge changes between different Private branches to avoid unnecessary extra commit IDs.
