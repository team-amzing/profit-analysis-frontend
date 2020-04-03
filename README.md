# Profit Analysis App
This is a Python 3.7 application to analyse real time oil prices of West Texas Intermediate (WTI) oil in order to make predictions about the price of WTI oil the next day. It compares the profit made against outgoing costs for the current and subsequent day. It advises the user whether it would be more profitable to dock today or tomorrow.

## Installation via Pipenv:
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

This project used the black auto formatter which can be run on git commit along with flake8 if you install pre-commit. To do this run the following in your terminal from within your virtual environment.

```
pre-commit install
```

Now pre-commit hooks should run on `git commit`.

## Installation via requirements.txt:

To install requirments using the requirments file run the following command:

```
pip install -r requirements.txt
```
