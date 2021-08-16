# Contributing

## Setup

Django Ninja API key uses Flit to build, package and publish the project. 

It's recommended to create and activate an virtual environment before installing the project. Simply run
```
python -m venv .venv
```
and activate the environment with
```
source .venv/bin/activate
```
Now install flit:
```
pip install flit
```
Now you are ready to install the project:
```
make install
```
Once you're you can check if all works with
```
make test
```

## Tests
Please make sure to write tests for your changes. You can run the tests with
```
make test
```
Also make sure the test coverage did not suffer with your contribution:
```
make cov
```

## Style and Linting
You can format the code with
```
make format
```
Before opening a pull request run all linters:
```
make lint
```