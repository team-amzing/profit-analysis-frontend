# Profit Analysis App
This application analyses real time oil prices of West Texas Intermediate (WTI) oil in order to make
predictions about the price of WTI oil the next day. It compares the profit made against outgoing
costs for the current and subsequent day. It advises the user whether it would be more profitable to
dock today or tomorrow.

The project is written in Python 3.7.

## Installation
Once you have cloned down this repository using `git clone` cd into the app directory eg.

```
cd profit-analysis-app
```

The project uses pipenv to manage project and development packages. To install these requirements run

```
pipenv install --dev
```

To initialise the virtual environment run

```
pipenv shell
```

To exit the virtual environment use `exit` and to see where you virtual environment is located run
`pipenv --venv` which may be useful when setting up your project interpreter in your IDE.
