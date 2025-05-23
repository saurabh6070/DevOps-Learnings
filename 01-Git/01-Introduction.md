**Version Control System**

A version control system (VCS) is a tool that helps manage changes to source code over time, allowing multiple developers to collaborate efficiently. It tracks revisions, enabling you to revert to previous versions and maintain a history of changes.
<br>

Types of Version Conrtol System :- Centralised VCS & Distributed VCS.
<br>

| Feature                         | CVCS                                      | DVCS                                      |
|---------------------------------|-------------------------------------------|-------------------------------------------|
| **Architecture**                | Centralized                               | Distributed                               |
| **Repository Location**         | Single central repository                 | Multiple repositories (local and remote)  |
| **Access**                      | Requires network access to central server | Can work offline with local repository    |
| **Commit History**              | Stored on central server                  | Stored locally and can be pushed to remote|
| **Collaboration**               | Changes are shared via central server     | Changes can be shared directly between developers|
| **Backup**                      | Single point of failure                   | Multiple copies of the repository         |
| **Performance**                 | Slower due to network dependency          | Faster due to local operations            |
| **Branching and Merging**       | More complex and less flexible            | Easier and more flexible                  |
| **Conflict Resolution**         | Handled on central server                 | Handled locally before pushing            |
| **Security**                    | Centralized control                       | Decentralized control                     |
| **Scalability**                 | Limited by central server capacity        | Highly scalable due to distributed nature |
| **Examples**                    | SVN, CVS                                  | Git, Mercurial                            |



<br><br>





**What is Git?**

Git is a distributed version control system that allows multiple developers to work on a project simultaneously. It keeps track of changes made to files and directories, enabling you to revert to previous versions if needed.

<br>

**Basic Terminologies**

**Repository (Repo):** A directory where Git stores all the files and their history.

**Commit:** A snapshot of your changes. Each commit has a unique ID and a message describing the changes.

**Branch:** A separate line of development. The default branch is usually called main or master.

**Merge:** Combining changes from different branches.

**Remote:** A version of your repository hosted on the internet or network (e.g., GitHub).
<br><br>



**Basic Commands**

1. Setting Up Git
  Install Git:


   On Windows: Download and install Git from git-scm.com.

   On macOS: Use Homebrew: brew install git.

   On Linux: Use your package manager: sudo apt-get install git.
To check Git Version :

        git --version


2. Configure Git:
   
        git config --global user.name "Your Name"
        git config --global user.email "your.email@example.com
        git config --global core.editor "vi"
        git config --list

3. Git Commands :
   

   3.1 Repository Commands

       3.1.1 Initialize a new repository:
             git init
     
       3.1.2 Clone an existing repository:
             git clone <repository-url>
           
       3.1.3 Forking an existing repository:
             git init
     

   3.2 Working with Files

       3.2.1 Check the status of your repository:
       git status

       3.2.2 Add files to the staging area:
       git add <file-name>
       git add .  

       3.2.3 Commit changes:
       git commit -m "Your commit message

       3.2.4 View commit history:
       git log
     



    3.3 Branching and Merging
  
        3.3.1 Create a new branch:
        git branch <branch-name>

        3.3.2 Switch to a branch:
        git checkout <branch-name

        3.3.3 Merge a branch into the current branch (If merge happens before any changes in Master since the branching is created. Then in the output of merge command, it will mention Fast-Forward merge. Fast forward merge is the basic merge with no conflict.) :
        git merge <branch-name>

        3.3.4 Deleting a Branch
        git branch -d br100

        3.3.5 3-way Merge/ Merge Conflict (If a master has created one branch br1, and at the time branch is merging into Master branch, some changes already in Master branch as well.)
        mkdir my_Git_Project
        cd my_Git_Project/
        git init
        echo "initial content" > file.txt
        git add file.txt
        git commit -m "Initial commit on main"
        git branch
        git checkout -d feature
        git branch
        ls														# Output :- file.txt
        echo "Feature branch changes" >> file.txt
        cat file.txt
        git commit -am "added changes to the feature branch"
        git checkout master
        echo "Master branch content" >> file.txt
        git branch
        git merge feature master 								## Conflict, and need to fix before merge
        ls
        cat file.txt											## shows content of both branches.
        git status
        git add file.txt
        git commit -m "Fix the conflict"
        cat file.txt


    3.4 Working with Remotes
  
        3.4.1 Add a remote repository:
        git remote add origin <repository-url>

        3.4.2 Push changes to a remote repository::
        git push origin <branch-name>

        3.4.3 Pull changes from a remote repository:
        git pull origin <branch-name>


    3.5 Git Restore
  
        3.5.1 Discard changes in the working directory
        git restore example.txt

        3.5.2 Restore a file from a specific commit. If you want to restore a file to its state in a specific commit, you can use:
        git restore --source <commit> <file>
        
        3.5.3 Restore all files in the working directory
        git restore .
       
        3.5.4 Examples

        echo "Adding second line in Python Code" >> myapp.py
        git status 								## file myapp.py is modified.
        git restore myapp.py
        git status
        cat myapp.py

        echo "Adding second line in Python Code" >> myapp.py
        git status 								## file myapp.py is modified.
        git add myapp.py
        git restore --staged myapp.py
        git status


   **3.6 Git Reset**
   <br>
        The git reset command is a powerful tool in Git for undoing changes and manipulating the commit history.
        **git reset --soft <commit>**

        Types of Git Reset
   
        **3.6.1 Soft Reset (--soft) : ** Moves the HEAD to the specified commit but keeps the changes in the staging area
        git reset --soft HEAD~1

        **3.6.2 Mixed Reset (--mixed) : **  Moves the HEAD to the specified commit and resets the staging area, but keeps the changes in the working directory.
        git reset --mixed HEAD~1

       ** 3.6.3 Hard Reset (--hard) : ** Moves the HEAD to the specified commit and resets both the staging area and the working directory to match the specified commit.
        git reset --hard HEAD~1

**Important Considerations :**
<br>
      
        Data Loss: Be cautious with git reset --hard as it will discard all changes in your working directory.
        History Rewriting: Using git reset can rewrite commit history, which can be problematic if you’ve already pushed commits to a remote repository. In such cases, consider using git revert instead.


  **3.7 Git Revert**
   <br>
        When you revert a commit, Git creates a new commit that applies the inverse of the changes introduced by the original commit. This means the original commit remains in the history, but its changes are effectively undone.
   
        3.7.1 Reverting a Single Commit
        git revert <commit>

        3.7.2 Reverting Multiple Commits
        git revert <commit1>..<commit2>

**Important Considerations :**
<br>

        Conflict Resolution: Reverting commits can sometimes lead to conflicts, especially if the changes being reverted are intertwined with other changes. You'll need to resolve these conflicts manually.
        Commit History: Since git revert adds new commits, the history remains intact, making it easier to track changes and understand the project's evolution.


  **3.8 Git Rebase**
   <br>
        When you rebase a branch, Git takes the commits from the current branch and re-applies them on top of another branch. This can be useful for integrating changes from one branch into another or for cleaning up the commit history.
   
        3.8.1 Interactive Rebase (-i): This command will open an editor where you can interactively rebase the last three commits.
        git rebase -i HEAD~3

        3.8.2 Regular Rebase : Re-applies commits from the current branch onto the specified base branch.
        git rebase master

**Important Considerations :**
<br>

        Conflict Resolution: Rebasing can lead to conflicts, especially if the changes being rebased overlap with changes in the base branch. You'll need to resolve these conflicts manually.
        History Rewriting: Rebasing rewrites commit history, which can be problematic if you've already pushed commits to a remote repository. In such cases, consider using git merge instead.


  **3.9 Git Ignore**
   <br>
        A .gitignore file is used in Git to specify which files and directories should be ignored by Git. This means that these files won't be tracked or included in version control.
   
        3.9.1 Git-Ignore File to add and commit.
              touch .gitignore
              git add .gitignore
              git commit .gitignore -m "Git ignore File"

        3.9.2 Add files in git ignore
              echo "myfile.txt" >> .gitignore
              echo "Line added in myfile.txt for Git-Ignore"
              echo "*.mov" >> .gitignore					     ## all files ending with mov will be ignored.
              git status
              git add .gitignore
              git commit .gitignore -m "Git ignore File commit 2nd time"

    

  **3.10 Git Cat-File**
   <br>
        A git cat-file is used to display the contents of objects in the Git database. Git's internal structure is like an **inverted tree**, where the root is the latest commit and branches are previous commits, blobs, and trees.
   <br><br>
       **Git's Inverted Tree Structure**
       <br>
          Commit Objects: These are the root nodes. Each commit points to a tree object representing the state of the repository at that point in time.
       <br>
          Tree Objects: These represent directories and contain pointers to blobs (files) and other trees (subdirectories).
       <br>
          Blob Objects: These are the leaf nodes and represent the actual file data.
   <br><br>
          Commit -> Tree -> blob1, blob2, blob3
 <br>
 
        3.10.1 Show the type of the object
              git cat-file -t <object>

        3.10.2 Show the content of the object
              git cat-file -p <object>

        Replace <object> with the SHA-1 hash of the object you want to inspect. This command is useful for examining blobs, trees, and commits in your repository.

**Usage :**

        git log
        git cat-file -p de714cd6fb   		## contains tree, parent, author
        git cat-file -p 2e9cbfefdc			## blob files for this commit
        git cat-file -p 74fa7fe7e5			## output of cat myapp.py


  **3.11 Git Upstream**
   <br>
        Upstream refers to the remote repository that your local repository is tracking. This is often the repository from which you clone your project and to which you push your changes. Understanding and managing upstream repositories is crucial for collaborating with others and keeping your local repository in sync with the remote one.
   
        3.11.1 Setting Upstream for a Branch.
              git push --set-upstream origin <branch_name>

        3.11.2 Checking Upstream Branch
              git branch -vv

        3.11.3 Fetching Changes from Upstream : fetches changes from the upstream repository without merging them into your local branch.
              git fetch upstream

        3.11.4 Pulling Changes from Upstream : fetches and merges changes from the upstream branch into your current branch.
              git pull upstream <branch_name>

        3.11.5 Push Changes to Your Fork:
              git push origin main




