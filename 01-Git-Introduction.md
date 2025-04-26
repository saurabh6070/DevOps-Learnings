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

        3.3.3 Merge a branch into the current branch:
        git merge <branch-name>



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
