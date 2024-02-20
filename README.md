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
    * [SAST report](#sast-report)



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
    
         cd OC-project-12-epic-events-crm-main
2. Install project dependencies with:

        pipenv install
3. To activate the virtual environment created by `pipenv` run:

        pipenv shell

##### Option 2: Using venv and pip

1. Move to the root folder with:

         cd OC-project-12-epic-events-crm-main
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

### CRUD operations with CLI

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

[Go to the top](#epic-events-crm)

### Linting

[Go to the top](#epic-events-crm)

### Logging

[Go to the top](#epic-events-crm)

### SAST report

[Go to the top](#epic-events-crm)