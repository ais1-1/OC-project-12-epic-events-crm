import os
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


def read_token() -> dict:
    """Get token from credential json file"""
    # checks if file exists
    if os.path.isfile(ABSOLUTE_PATH_TO_TOKEN_FILE) is False:
        return None

    with open(ABSOLUTE_PATH_TO_TOKEN_FILE, "r", encoding="utf-8") as json_file:
        loaded_data = json.load(json_file)

    return loaded_data


def authorized_header() -> dict:
    access_token = read_token()
    if access_token:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Token {access_token['token']}",
        }
        return headers
    else:
        console.print(
            "We couldn't process your request as you are not logged in.",
            style="warning",
        )


def validate_token():
    credentials = read_token()
    token = Token.objects.get(user=User.objects.get(email=credentials["email"]))
    utc_now = datetime.datetime.utcnow()
    utc_now = utc_now.replace(tzinfo=pytz.utc)
    if token is not credentials[
        "token"
    ] and token.created < utc_now - datetime.timedelta(hours=settings.EXPIRE_TOKEN):

        console.print(
            "Your token has been expired. Please login again...", style="warning"
        )
        login_again()
    elif token is not credentials["token"]:
        console.print("Please renew your token by logging in again...", style="warning")
        login_again()
    else:
        return True


def login_again():
    if Confirm.ask("Do you want to [i]login[/i]?", default=True):
        call_command("login")
    else:
        console.print("[b]OK. Bye[/b] :wave:")
        exit()