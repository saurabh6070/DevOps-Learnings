Problem Statement 2. Based on what you have learnt in the class, do the following steps:
1. Create a Git working directory with feature1.txt and feature2.txt in the master branch 
2. Create 3 branches develop, feature1 and feature2 
3. In develop branch create develop.txt, do not stage or commit it 
4. Stash this file and check out to feature1 branch 
5. Create new.txt file in feature1 branch, stage and commit this file 
6. Checkout to develop, unstash this file and commit 


**Solution :-**

**Commands for the solution :**

    mkdir git2
    cd git2/
    git init
    ls -a
    touch feature1.txt feature2.txt
    git add feature1.txt feature2.txt
    git commit -m "Adding feature1.txt and feature2.txt files in the master branch"
    git status
    git branch
    git branch develop
    git branch feature1
    git branch feature2
    git checkout develop
    touch develop.txt
    git status
    git stash push -m "Stash develop.txt"
    git status
    git checkout feature1
    touch new.txt
    git add new.txt
    git commit -m "Add new.txt in feature1 branch"
    git checkout develop
    git stash pop
    git status
    git add develop.txt
    git commit -m "Add develop.txt in develop branch"
    git status


**Stashing in Git allows temporarily save changes in working directory without committing them. This is useful when switching branches or perform other tasks but don’t want commit current changes yet.**
