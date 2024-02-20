"""
Create an .env file with a randomly generated secret key and
pre-configured environment variables. See file
.env.dist for the example.

The pre-configured environment variable names are:

# Pipenv variables
# Name of the virtualenv
- PIPENV_CUSTOM_VENV_NAME (default=epicevents-env)
# Create virtualenv inside project directory
- PIPENV_VENV_IN_PROJECT (default=1)

# Django variables
- DEBUG (default=True)
- SECRET_KEY
- ALLOWED_HOSTS (default=localhost and 127.0.0.1)
# Base url
- BASE_URL (default=http://127.0.0.1:8000/)
# File name to store json token
- TOKEN_FILENAME
# Sentry api key
- SENTRY_DSN

# Database info
# Name of the database
-DB_NAME
# Username to connect to the database
- DB_USER
# Password for the user
- DB_PASSWORD
# Host as in the server address
- DB_HOST
# Expose the port in the server address
- DB_PORT (default=3306)


The generated .env file must be configured with appropriate values
for each environment variable before use.

Example of use :

    1. Run this script to generate an .env file.
    2. Configure environment variable values
       in the generated .env file.
    3. Use the .env file to configure
       the environment of your epiceventscrm application.

.. note::
    The generated .env file should not be shared publicly
    because it contains sensitive information.

"""

from django.core.management.utils import get_random_secret_key

# Environment variables list
env_variable_names = [
    "PIPENV_CUSTOM_VENV_NAME",
    "PIPENV_VENV_IN_PROJECT",
    "DEBUG",
    "SECRET_KEY",
    "ALLOWED_HOSTS",
    "BASE_URL",
    "DB_HOST",
    "DB_PORT",
    "TOKEN_FILENAME",
    "SENTRY_DSN",
    "DB_NAME",
    "DB_USER",
    "DB_PASSWORD",
]

pipenv_custom_venv_name = "epicevents-env"
pipenv_venv_in_project = 1
# Generate a random secret key
secret_key = get_random_secret_key()
debug = True
db_port = 3306
allowed_hosts = "localhost 127.0.0.1"
db_host = "localhost"
base_url = "http://127.0.0.1:8000/"

# Open .env to write
try:
    with open(".env", "w") as f:
        f.write(f"PIPENV_CUSTOM_VENV_NAME={pipenv_custom_venv_name}\n")
        f.write(f"PIPENV_VENV_IN_PROJECT={pipenv_venv_in_project}")
        f.write(f"DEBUG={debug}\n")
        f.write(f"SECRET_KEY={secret_key}\n")
        f.write(f"ALLOWED_HOSTS={allowed_hosts}\n")
        f.write(f"BASE_URL={base_url}")
        f.write(f"DB_HOST={db_host}")
        f.write(f"DB_PORT={db_port}\n")
        for env_var in env_variable_names[8:]:
            f.write(f"{env_var}=\n")
except IOError as e:
    print(f"Couldn't write to file ({e})")
else:
    print(".env file has created successfully!")
