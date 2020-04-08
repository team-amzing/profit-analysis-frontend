# Profit Analysis App
This is a Python 3.7 application to analyse real time oil prices of West Texas Intermediate (WTI) oil in order to make predictions about the price of WTI oil the next day. It compares the profit made against outgoing costs for the current and subsequent day. It advises the user whether it would be more profitable to dock today or tomorrow.

## Get the code
Once you have cloned down this repository using `git clone` cd into the app directory eg.

```
cd profit-analysis-frontend
```

The dependencies can be installed through one of two methods, pipenv or the requirements.txt file, detailed instructions can be found below. It is recommended that you use pipenv but if pipenv is not functioning use the requirements.txt file.

## Installation via Pipenv:
The project uses pipenv to manage project and development packages. Pipenv can be installed using pip:

```bash
pip install pipenv
```

To install requirements run:

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
Once the dependacies have been downloaded, and you are in the correct branch, the application can be run using the following command.

```
python3 main.py
```


# Please Follow these instructions to install and run the software for the demo

## Get the code
To make sure you have the latest changes, please `cd` into the app directory `profit-analysis-frontend` and from the master branch run:

```bash
git pull
```

Then to checkout the branch with the working demo, run:

```bash
git checkout scrape-html-site
```

## Install requirements
To install the dependencies either locally or within a virtual environment run:

```bash
pip install -r requirements.txt
```

## Launch the software
To launch the software in a UI please run the following, ensuring you are in the app directory `profit-analysis-frontend`:

```bash
python3 main.py
```



