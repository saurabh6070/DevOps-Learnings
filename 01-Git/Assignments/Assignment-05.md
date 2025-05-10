Problem Statement 5. Based on what you have learnt in the class, do the following steps: <br>
a. Create a Git Flow workflow architecture on Git  <br>
b. Create all the required branches  <br>
c. Starting from the feature branch, push the branch to the master, following the architecture  <br>
d. Push a urgent.txt on master using hotfix 

 <br> <br>
**Solution :-** <br>

**Commands for the solution :** <br>

    mkdir git5
    cd git5/
    git init
    ls -a
    touch test.txt
    git add test.txt 
    git commit -m "Adding test file to master branch"
    git status
    git branch
    git checkout -b develop
    git checkout -b feature1
    git branch
    touch feature1.txt
    echo "Content for feature1.txt" > feature1.txt 
    touch feature1.txt
    echo "Content for feature1.txt" > feature1.txt 
    git add feature1.txt
    git commit -m "Implement feature 1"
    git checkout develop
    git merge feature1
    git remote add origin https://github.com/saurabh6070/Assignment5.git
    git push -u origin master
    git checkout -b hotfix
    touch urgent.txt
    echo "This is an urgent fix." > urgent.txt
    git add urgent.txt
    git commit -m "Add urgent fix"
    git checkout master
    git merge hotfix
    git push origin master
    ls
