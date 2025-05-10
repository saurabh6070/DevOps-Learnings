Problem Statement 3. Based on what you have learnt in the class, do the following steps: <br>
a. Create a Git working directory, with the following branches: <br>
● Develop <br>
● F1 <br>
● f2 <br>
b. In the master branch, commit main.txt file <br>
c. Put develop.txt in develop branch, f1.txt and f2.txt in f1 and f2 respectively <br>
d. Push all these branches to GitHub <br>
e. On local delete f2 branch <br>
f. Delete the same branch on GitHub as well <br>
<br><br><br>



**Solution :-**

**Commands for the solution :**

    cd git3/
    git init
    git status
    ls -a
    git branch develop
    ls
    touch test.txt
    ls
    git branch develop
    git commit test.txt -am "Adding test.txt to master"
    ls
    git add test.txt 
    git commit -m "Adding test.txt to master"
    git branch develop
    git branch f1
    git branch f2
    git branch
    touch main.txt
    git add main.txt
    git commit -m "Add main.txt in master branch"
    git checkout develop
    touch develop.txt
    git add develop.txt
    git commit -m "Add develop.txt in develop branch"
    git checkout f1
    touch f1.txt
    git add f1.txt
    git commit -m "Add f1.txt in F1 branch"
    git checkout f2
    touch f2.txt
    git add f2.txt
    git commit -m "Add f2.txt in f2 branch"
    git remote add origin https://github.com/saurabh6070/Assignment3.git
    git branch
    git checkout master
    git branch
    git push -u origin master
    git push -u origin develop
    git push -u origin f1
    git push -u origin f2
    git checkout master
    git branch
    git branch -d f2
    git branch
    git push origin --delete f2
