Problem Statement 4. Based on what you have learnt in the class, do the following steps: <br>
a. Put master.txt on master branch, stage and commit  <br>
b. Create 3 branches: public 1, public 2 and private  <br>
c. Put public1.txt on public 1 branch, stage and commit  <br>
d. Merge public 1 on master branch  <br>
e. Merge public 2 on master branch  <br>
6. Edit master.txt on private branch, stage and commit  <br>
g. Now update branch public 1 and public 2 with new master code in private  <br>
h. Also update new master code on master  <br>
i. Finally update all the code on the private branch
 <br> <br> <br>

**Solution :-**   <br>

**Commands for the solution :**  <br>

    mkdir git4
    cd git4/
    git init
    ls -a
    touch master.txt
    git add master.txt
    git commit -m "Add master.txt on master branch"
    git branch
    git branch public1
    git branch public2
    git branch private
    git checkout public1
    touch public1.txt
    git add public1.txt
    git commit -m "Add public1.txt on public1 branch"
    git checkout master
    git merge public1
    git checkout public2
    git checkout master
    git merge public2
    git checkout private
    echo "Updated master.txt file" >> master.txt
    git status
    git add master.txt 
