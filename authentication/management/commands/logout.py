import os
import requests
import json
from django.core.management.base import BaseCommand
from django.conf import settings
from django.urls import reverse

from .login import ABSOLUTE_PATH_TO_TOKEN_FILE

LOGOUT_URL = settings.BASE_URL.strip("/") + reverse("logout")


def read_token() -> dict:
    """Get token from credential json file"""
    # checks if file exists
    if os.path.isfile(ABSOLUTE_PATH_TO_TOKEN_FILE) is False:
        return None

    with open(ABSOLUTE_PATH_TO_TOKEN_FILE, "r", encoding="utf-8") as json_file:
        loaded_data = json.load(json_file)

    return loaded_data


def request_logout():
    """Logs out the current user"""
    access_token = read_token()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Token {access_token['token']}",
    }
    # Delete the credentials file
    os.remove(ABSOLUTE_PATH_TO_TOKEN_FILE)

    response = requests.post(url=LOGOUT_URL, headers=headers, timeout=5000)
    return response


class Command(BaseCommand):
    def handle(self, *args, **options):
        """Handles 'logout' command"""
        result = request_logout()
        if result.status_code == 200:
            print("You have logged out.")
        else:
            print("Something went wrong, you have not logged out!")
