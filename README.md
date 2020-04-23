# Profit Analysis App
This is a Python 3.7 application to analyse real time oil prices of West Texas Intermediate (WTI) oil in order to make predictions about the price of WTI oil the next day. It compares the profit made against outgoing costs for the current and subsequent day. It advises the user whether it would be more profitable to dock today or tomorrow.

## Clone repository:
Clone this repository using the following command.

```
cd profit-analysis-app
```

Once you have cloned down this repository using `git clone` cd into the app directory eg.

```
cd profit-analysis-app
```

The dependancies can be installed through one of two methods, pipenv or the requirments.txt file, detailed instructions can be found below. It is recomended that you use pipenv but if pipenv is not functioning use the requirments.txt file.

## Installation via Pipenv:
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

If the installation via pipenv is not possible, install requirments using the requirements file by running the following command.

```
pip install -r requirements.txt
```

## Running the application

Once the dependacies have been downloaded the application can be run using the following command.

```
python main.py
```

