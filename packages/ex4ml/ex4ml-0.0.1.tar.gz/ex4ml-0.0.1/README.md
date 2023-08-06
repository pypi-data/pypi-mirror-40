# ex4ml

A toolkit for conducting machine learning experiments efficiently.

![image](https://gitlab.com/minds-mines/ex4ml/ex4ml/badges/master/pipeline.svg)
![image](https://gitlab.com/minds-mines/ex4ml/ex4ml/badges/master/coverage.svg)

## Description

The target audience of ex4ml is researchers conducting experiments in
machine learning. The goal of ex4ml is to allow you to focus on the
machine learning research while minimizing your worrying about designing
and managing experiments.

The secondary audience of ex4ml is machine learning practitioners who
want a simple way to test and compare machine learning approaches.

### Applications

ex4ml should work for experiments on the following and all combinations
of them:

* Multi-Modal / Multi-View learning
* Multiple-Instance learning
* Feature comparisons
* Feature visualizations

### Development

#### Summary

Here is the summary of what you need to do. Read on for more details.

Install everything:

```bash
pipenv install --dev
```

Run tests:

```bash
pipenv shell
python setup.py test
```

After you make changes make sure you run autopep8 to fix your code\'s
syntax and pylint to get feedback on what could be improved in your
code.

```bash
pipenv shell
autopep8 --in-place --aggressive --aggressive *.py
pylint src/ex4ml/*.py
pylint test/*.py
```

#### Pipenv

Use [pipenv](http://pipenv.readthedocs.io/en/latest/) to automatically
manage isolated, virtual environments for Python projects.

Install/upgrade `pipenv` via the command line.

```bash
pip install --upgrade pipenv
```

To install modules or create a `Pipfile` from a `requirements.txt` file:

```bash
pipenv install
```

To install dev-modules:

```bash
pipenv install --dev
```

To install or uninstall modules respectively to or from your Python
project:

```bash
pipenv install module_name
pipenv install dev_module_name --dev
pipenv uninstall module_name
```

To manually create a `Pipfile.lock` file from the installed versions:

```bash
pipenv lock
```

To load the Python virtual environment into the shell to execute
commands or run a single command using the Python virtual environment
use the following:

```bash
pipenv shell
pipenv run command_name
```

Use `exit` to unload the Python virtual environment.

To see your project\'s dependency graph:

```bash
pipenv graph
```

#### PyScaffold

This project has been set up using PyScaffold 3.0.3. For details and
usage information on PyScaffold see <http://pyscaffold.org/>.

Use [PyScaffold](http://pyscaffold.org/en/latest/features.html) to
quickly setup and manage Python projects.

### Installation

You will need [Git](https://git-scm.com) with `user.name` and
`user.email` setup to get started.

```bash
git config --global user.name "John Doe"
git config --global user.email "john.doe@email.com"
```

Install/upgrade `setuptools` and `pyscaffold` via the command line:

```bash
pip install --upgrade setuptools
pip install --upgrade pyscaffold
```

### Testing

To execute unit tests in the `tests` directory, use:

```bash
pipenv shell
python setup.py test
```
