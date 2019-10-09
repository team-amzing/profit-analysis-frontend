# Cheat Sheet for Development Processes

This document is intended to be a place to outline useful engineering processes that can make working collaboratively on a project smoother and more manageable. These processes may need to change over time and this document should be updated to reflect these changes. See below for an outline of a general process for contributing to a project which has in the past proven to be helpful.

## Branching
It is good practice to checkout branches using Git when you wish to contribute to the project. Maintaining a 'healthy' tree allows us to have many people working on a project simultaneously without (hopefully) too many git nightmares!

If you have been asked to contribute some work to this project the general method you should follow is to checkout a new branch to complete your work on.

Before checking out a new branch you will want to make sure your master branch is up to date. To do this run the below command in your terminal from within the project directory.

```
git pull
```

This will pull any new changes that have been commmited to master to your local version. If there are no new changes your terminal will say `Already up to date`.

You can then checkout a new branch to begin work on. It is nice and tidy to follow a consistent convention for naming branches so try to make your branch names consistent with that below.

```
git checkout -b task/example-branch-name
```

The `-b` flag will create a new branch from master with this name. Be aware that if you do not run this command from master the new branch will be created from the branch you are currently on. Use `git branch` to see the branches you have locally, the branch you are currently on may have an `*` next to it or be highlighted in green.

You can now start your development. You may wish to use and IDE such as Pycharm (the community edition is free and can be installed via Anaconda or your package manager if using Mac or Ubuntu). Alternatively you can go old school and develop using vim in the command line.

## Using Git
So you have written some code that you want to push to your branch, if we don't commit our work others are not able to access it and there it is not stored on Git. Go back to your terminal and run

```
git status
```

This will display all of your changes on your branch. If you have not staged any changes these will appear red. You will likely be using `git status` a lot to manage the work you wish to commit.

You can also use `git diff` to see all of the unstaged changes on your branch in a vim style editor.

You may sometimes wish to only commit one file, in which case you would run

```
git add example_file.py
```

Or if you're super stoked with all of your work and wish to it all.

```
git add .
```

If you do a `git status` now you will see that `example_file.py` is green as it has been staged for commit.

Now to commit your work you will use the command `git commit`. If you use this without passing it any flags it will take you to a vim editor where you can add a commit comment. FYI Git will not let you commit work without a comment. You can use the `-m` flag shown below to add your comment and commit in one command.

```
git commit -m 'This is my example comment for my commit.'
```

## Pre-commit hooks
Since this project has pre-commit installed the black autformatter and flake8 will run when you try to commit work using `git commit`. Black will go through the files it is configured to and reformat them for you. Flake8 is a checking tool and if you get a flake8 error you will have to fix this yourself and then re-commit your work. If all your code was formatted perfectly your commit will have been successul and you can move onto the next step. If not you will need to add the new changes and run your commit statement again.

```
git status
git add .
git commit -m 'This is my example comment for my commit.'
```

If this commit is successful it is always good practice to do a quick `git status` to check nothing got left behind. It should something like `working tree clean`.

Your work is still only local and you will need to push it to Git for it to become available on GitHub.

```
git push origin task/example-branch-name
```

It is good practice to do this verbosely as you won't get into sticky situations of accidentally pushing to master.

## Pull requests
Once you are happy that your work is ready for review you can create a pull request in GitHub. If you go to the repo on GitHub it will usually prompt you to create a new pull request. You can do this also from the branches tab.

Try to add a useful description to your PR and be sure to check your branch is pointing to the correct base (this is usually master). You can create this pull request and post it in the slack channel for others to review.

Once you feel satisfied with the reviews you can click `Merge` and this will merge your branch into the base branch. Be sure to delete your branch after you have merged it to keep the working tree clean.

Now go back to your terminal and run the following to pull the changes to the master branch down and remove your branch locally.

```
git checkout master
git pull
git branch -d task/example-branch-name
```
