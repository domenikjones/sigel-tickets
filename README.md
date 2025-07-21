# Coding Challenge

## Create Trello ticket and Slack message for internal ticket system

### Introduction and project setup

To setup the project, create a virtualenv and install the dependencies with poetry

```shell
$ pip install -U poetry
$ poetry install
```

Or install the dependencies with pip directly

```shell
$ pip install -r requirements.txt
```

### Django Commands

#### Initialize database

To setup an admin user and a test ticket, use the command `init_db` to bootstrap initial state.
The initial username is `admin` and the password `AdminAdmin`.

```shell
$ python manage.py init_db
```

#### Synchronize trello labels from the target board

```shell
$ python manage.py sync_trello_labels
```
