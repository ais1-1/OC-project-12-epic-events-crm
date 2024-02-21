# Epic Events CRM

## Contents

1. [Project description](#project-description)
2. [Local development](#local-development)
    * [Clone repository and install dependencies](#clone-repository-and-install-dependencies)
    * [Create MariaDB database](#create-mariadb-database)
    * [Setup environment variables: .env file](#setup-environment-variables-env-file)
    * [Migrate database and load data](#migrate-database-load-data)
    * [ERD of the database](#erd-of-the-database)
    * [Class diagrams of the application](#class-diagrams-of-the-application)
    * [Run the application](#run-the-application)
3. [User guide](#user-guide)
    * [Admin site](#admin-site)
    * [CRUD operations with CLI](#crud-operations-with-cli)
    * [Tests and coverage](#tests-and-coverage)
    * [Linting](#linting)
    * [Logging](#logging)
    * [Security and SAST report](#security-and-sast-report)



## Project description

This project is a secure internal Customer Relationship Management command line application developed for Epic Events. It is to help the employees collect and process data from customers and their events.

The detailed specifications can be read in `docs/specifications_fr.pdf` (in French).

## Local development
[Go to the top](#epic-events-crm)

### Clone repository and install dependencies

#### Clone repository

        git clone https://github.com/ais1-1/OC-project-12-epic-events-crm.git

#### Install dependencies
##### Option 1: With pipenv

For this method, it is necessary to have pipenv already installed on your python installation. If pipenv is not already installed on your computer, refer to [the official documentation](https://pipenv.pypa.io/en/latest/installation/).

1. Move to the root folder with:
    
         cd path/to/OC-project-12-epic-events-crm-main
2. Install project dependencies with:

        pipenv install
3. To activate the virtual environment created by `pipenv` run:

        pipenv shell

##### Option 2: Using venv and pip

1. Move to the root folder with:

         cd path/to/OC-project-12-epic-events-crm-main
2. Create a virtual environment for the project with ` py -m venv env` on windows or `python3 -m venv env` on macos or linux.
3. Activate the virtual environment with `env\Scripts\activate` on windows or `source env/bin/activate` on macos or linux.
4. Install project dependencies with:

        pip install -r requirements.txt

[Go to the top](#epic-events-crm)

### Create MariaDB database

1. Install MariaDB in your system:

    * For Linux distributions, if you don't have an official distribution package for MariaDB choose your distribution and download from the [official website](https://mariadb.com/downloads/).
    * For Windows, follow [the link](https://mariadb.com/kb/en/installing-mariadb-msi-packages-on-windows/).
    * For macOS, follow [this link](https://mariadb.com/kb/en/installing-mariadb-on-macos-using-homebrew/).

2. Start the MariaDB server:
    * Linux: https://mariadb.com/kb/en/systemd/
    * Windows: https://mariadb.com/kb/en/running-mariadb-from-the-build-directory/#starting-mariadbd-after-build-on-windows
    * macOS: https://mariadb.com/kb/en/launchd/

3. Connect to MariaDB with your credentials:

       mysql -u root -p

    If you don't have a password [set one](https://mariadb.com/kb/en/set-password/)

4. Once connected, you will be inside the MariaDB console, create the database with a name:

       CREATE DATABASE <db_name>;
    
    Check if the database is created by referring to the list of all the databases:

        SHOW DATABASES;

5. Create a user for the database and grant all privileges (it is better to not to use the root user for security reasons):

        CREATE USER 'username'@localhost IDENTIFIED BY 'password';
        GRANT ALL PRIVILEGES ON db_name.* TO 'username'@'localhost';
        # Grant privileges for test database too (pytest creates a database)
        GRANT ALL PRIVILEGES ON test_db_name.* TO 'username'@'localhost';
        FLUSH PRIVILEGES;

6. Authenticate as the above user and use the database:

        USE db_name;

7. Quit the console:

        exit;

[Go to the top](#epic-events-crm)

### Setup environment variables: `.env` file

Environment variables are used to store sensitive values. They should be stored in the `.env` file.

There are two options for creating the `.env` file:

* Using the `.env.dist` file

    Rename the `.env.dist` file in the project root to `.env`.

* Using the `create_env_file.py` script

    Run the script with the following command to create the `.env` file with some default values:

        python create_env_file.py

Once the `.env` file is created, open it with a text editor and add the correct values ​​for each variable.

[Go to the top](#epic-events-crm)

### Migrate database and load data

* To migrate, run:

     python manage.py migrate 

Note that the three user teams (management, sales, support) are automatically created. See the second migration file in `teams/migrations`

* Load the database with the sql file in the project:

        mysql -u username -p db_name < epiceventsdb.sql

[Go to the top](#epic-events-crm)

### ERD of the database
#### Detailed Entity Relationship Diagram
![ERD db](/docs/img/epiceventscrm_erd.png)

#### ERD excluding the tables from frameworks
![Reduced ERD db](/docs/img/epiceventscrm_reduced_erd.png)

[Go to the top](#epic-events-crm)

### Class diagrams of the application

![class diagrams](/docs/img/epiceventscrm_class_diagram.png) 

[Go to the top](#epic-events-crm)

### Run the application

Run the server with:

        python manage.py runserver

[Go to the top](#epic-events-crm)

## User guide

### Admin site

The admin site is available at `http://127.0.0.1:8000/epiccrmadmin/`. Admin site access is granted to managers and superusers.

The manager can use the admin site to do any of the CRUD operations on any model (except the deletion of three major `Team` instances, which are blocked).

[Go to the top](#epic-events-crm)

### CRUD operations with CLI

#### Note that permissions are limited in each case. Refer `docs/specifications_fr.pdf` for the details. 
To test permissions see [the postman workspace](https://www.postman.com/ais1-1/workspace/epiceventscrm-p12/collection/)

First you need to activate the virtual environment (refer [Install dependencies](#install-dependencies)) and then run the application (refer [Run the application](#run-the-application)).

#### Main commands to use the application

| Command | Usage | Optional arguments|
| :------:|--------:|:---------------|
|`login`| `python manage.py login`|`--email <email>`, `--password <password>`, `--help`|
|`logout`| `python manage.py logout` |`--help` |
|`user`| `python manage.py user`|`--list` , `--detail` , `--create` , `--update` , `--delete` , `--help` |
|`client`|`python manage.py client`| `--list` , `--detail` , `--create` , `--update` , `--delete` , `--help`|
|`contract`|`python manage.py contract`|`--list` , `--detail` , `--create` , `--update` , `--delete` , `--unsigned` , `--signed` , `--unpaid` , `--own` , `--withoutevent` , `--help`|
|`event`|`python manage.py event`|`--list` , `--detail` , `--create` , `--update` , `--delete` , `--own` , `--withoutsupport` , `--help`|

One can use the `--help` option of each command to see a detailed explanation.

Arguments for the basic CRUD operations are:

* `--list` - show the list of all the objects
* `--detail` - show the details of an object
* `--create` - create an object
* `--delete` - delete an object
* `--update` - update an object

#### Authentication

* One can authenticate using the following command:

        python manage.py login

    This will ask for user's email and password. The login process creates a json file with user's email and token.

    The token expiration time is set using the variable `EXPIRE_TOKEN` inside `settings.py`.

    A successful login will be like this:

    ![Successful login](/docs/img/screenshot_login.png)

* One can logout using:

        python manage.py logout

    This will remove the token file from your system.

[Go to the top](#epic-events-crm)

### Tests and coverage

#### Tests

The project uses the `pytest` and `django-pytest` modules for testing. The tests corresponding to each application reside in the corresponding folder with the name `tests.py`.

The pytest configuration can be seen in the `setup.cfg` file under the `[tool:pytest]` line.

Run tests using the following commands:


        # Move to root folder
        cd path/to/OC-project-12-epic-events-crm-main
        # Activate virtual environment
        pipenv shell
        # Run the test
        pytest

Note that if you are using a non-privileged user for the database, you should grant privileges for test_database too (refer [Create MariaDB database](#create-mariadb-database)).

#### Coverage

The project uses `Coverage.py` and `pytest-cov` for better reading of coverage report.

Coverage configuration, such as files to exclude, is in the `setup.cfg` file under `[coverage:run]`.

To view the coverage report:

        # Move to root folder
        cd path/to/OC-project-12-epic-events-crm-main
        # Activate virtual environment
        pipenv shell
        coverage report -m

To view the report with a test report:

        pytest --cov=.

The current coverage is at 93%:

![Coverage report](/docs/img/screenshot_2024-02-21_coverage_report.png)

[Go to the top](#epic-events-crm)

### Linting

The project uses `flake8` and `black` modules for linting. `Flake8` has been configured to allow a maximum code line length of up to 99 characters. And it will not check in the migrations and virtual environment folders. Refer to the `setup.cfg` file under `[flake8]` for more details.

Linting can be done using the following commands:

        # Move to root folder
        cd path/to/OC-project-12-epic-events-crm-main
        # Activate virtual environment
        pipenv shell
        # Run flake8
        flake8

Currently, there are no errors, so you will not see anything on the terminal.

[Go to the top](#epic-events-crm)

### Logging

This project uses **Sentry** and the `logging` module for error handling. To use **Sentry** and be able to use monitoring, [create an account on Sentry](https://sentry.io/signup/).

#### Configuration for Sentry

* Login to Sentry
* Create a new project
* Choose a platform for the project, in our case Django.
* Choose a team for your project, then click on: *Create a project*

Once the project is created, you can retrieve the `SENTRY_DSN` key in `Project Settings > Client Keys (DSN)` to integrate into the `.env` file.

Once all these steps have been completed and the local server has started, you will be able to view the application activity on Sentry.

To test Sentry logging, uncomment the function `trigger_error` in `epiceventscrm/urls.py` and also the `sentry-debug` endpoint inside `urlpatterns` list in the same file. Then navigate to the end point using a web browser, you can see a `ZeroDivisionError`. Check the project's page in Sentry, you should see the same issue there.

#### Configuration for the module `logging`

To complete error handling by inserting appropriate logs into the code, this project uses Python's `logging` module. It is supported by Sentry with the `sentry-sdk` module installed. These logs should be placed in strategic places in the code, such as critical functions, `try/except` blocks and data validation points. Logs are also used to alert to certain actions in this project, like creating or updating a user, signing a contract etc.

Here is a code snippet from the project (`authentication/management/commands/user.py`) where Sentry will give you an alert on user creation:

        if status.is_success(response.status_code):
                logging.info(
                    f"User creation, email: {response_dict['email']}",
                    extra={"action by": auth_data["email"]},
                )



[Go to the top](#epic-events-crm)

### Security and SAST report

This project does its best to integrate **OWASP** guidance to improve its security. You can see various implementations according to the [Django Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Django_Security_Cheat_Sheet.html#django-security-cheat-sheet) and [DRF Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Django_REST_Framework_Cheat_Sheet.html#django-rest-framework-drf-cheat-sheet).

This project includes a static analysis security tool (SAST), `Bandit`. It is recommended by **OWASP** to check security risks (refer [OWASP cheat sheet on SAST tools](https://cheatsheetseries.owasp.org/cheatsheets/Django_REST_Framework_Cheat_Sheet.html#sast-tools)).

To create a report using `bandit` and store it to a file named `sast_report.txt`, use the following command inside the root folder:

        bandit -r . > sast_report.txt

Configurations for the module can be seen inside `.bandit` file. Here is the resume of the current report:


        Run metrics:
                Total issues (by severity):
                        Undefined: 0
                        Low: 6
                        Medium: 0
                        High: 0
                Total issues (by confidence):
                        Undefined: 0
                        Low: 0
                        Medium: 6
                        High: 0
        Files skipped (0):


[Go to the top](#epic-events-crm)