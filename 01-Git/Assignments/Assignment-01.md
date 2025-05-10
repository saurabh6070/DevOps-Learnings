Problem Statement 1 . Based on what you have learnt in the class, do the following steps: 
a. Create a new folder 
b. Put the following files in the folder 
● Code.txt ● Log.txt ● Output.txt 
c. Stage the Code.txt and Output.txt files 
d. Commit them 
e. And finally push them to GitHub




Solution :-

**Commands for the solution : **

    mkdir -p git1
    cd git1/
    touch code.txt log.txt output.txt
    git init
    ls -a
    git add code.txt output.txt 
    git status
    git commit -m "Add code.txt output.txt in commit-1" 
    git remote add origin https://github.com/saurabh6070/Assignment1.git
    git branch
    git push -u origin master
    git status


** Note :- To store credentials temporarily for one hour, run following commands and then only one time fillin the username/ password :-**

    git config --global credential.helper cache
    git config --global credential.helper 'cache --timeout=3600'  # 1 hour


**Snippets :- **

