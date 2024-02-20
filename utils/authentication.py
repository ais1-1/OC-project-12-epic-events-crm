import os
import logging
import datetime
import pytz
import json
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.core.management import call_command
from rich.prompt import Confirm

from .interface.console_style import console


User = get_user_model()

ABSOLUTE_PATH_TO_TOKEN_FILE = (
    str(settings.BASE_DIR) + "/" + str(settings.TOKEN_FILENAME) + ".json"
)


def read_token(token_file=ABSOLUTE_PATH_TO_TOKEN_FILE) -> dict:
    """Get token from credential json file"""
    # checks if file exists
    if os.path.isfile(token_file) is False:
        logging.warning("Token not found.")
        return None

    with open(token_file, "r", encoding="utf-8") as json_file:
        loaded_data = json.load(json_file)

    return loaded_data


def authorized_header(test_token=None, token_file=ABSOLUTE_PATH_TO_TOKEN_FILE) -> dict:
    """
    Returns header for authentication
    Args:
    test_token (str) - token for test purpose
    token_file (str) - path to token stored json file

    Returns:
    headers (dict) - authorized header
    access_token (dict) - auth data (email, token)

    """
    access_token = read_token(token_file)

    if access_token and validate_token(access_token, test_token):

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Token {access_token['token']}",
        }
        return headers, access_token
    else:
        console.print(
            "We couldn't process your request as you are not logged in.",
            style="warning",
        )
        exit()


def validate_token(credentials, test_token=None):
    """
    Validate token for authorization

    Args:
    credentials (dict) - auth data containing token to validate
    test_token (str) - token for test purpose only

    Returns:
    True (bool) if token is not expired and
    the token of the logging in user is present in the token file
    """
    if test_token is not None:
        token = test_token
    else:
        token = Token.objects.get(user=User.objects.get(email=credentials["email"]))
    utc_now = datetime.datetime.utcnow()
    utc_now = utc_now.replace(tzinfo=pytz.utc)
    if str(token) is not credentials[
        "token"
    ] and token.created < utc_now - datetime.timedelta(hours=settings.EXPIRE_TOKEN):

        console.print(
            "Your token has been expired. Please login again...", style="warning"
        )
        login_again()
    elif str(token) != credentials["token"]:
        console.print("Please renew your token by logging in again...", style="warning")
        login_again()
    else:
        return True


def login_again():
    if Confirm.ask("Do you want to [i]login[/i]?", default=True):
        call_command("login")
        exit()
    else:
        console.print("[b]OK. Bye[/b] :wave:")
        exit()
