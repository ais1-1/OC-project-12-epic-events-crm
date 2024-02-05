import getpass
import requests
import json
from django.core.management.base import BaseCommand
from django.urls import reverse
from django.conf import settings

AUTH_URL = settings.BASE_URL.strip("/") + reverse("obtain_token")
ABSOLUTE_PATH_TO_TOKEN_FILE = (
    str(settings.BASE_DIR) + "/" + str(settings.TOKEN_FILENAME) + ".json"
)


def request_get_token():
    """
    Generate token on request.
    Returns dict containing credentials and token value.
    """
    email = ""
    password = ""

    while email.strip() == "" or password.strip() == "":
        print("Epic events crm")
        email = input("Enter email:")
        password = getpass.getpass("Enter password:")

    auth_data = {"email": email, "password": password, "token": None}
    response = requests.post(url=AUTH_URL, data=auth_data, timeout=5000)

    if response.status_code != 200:
        print("Authentication impossible")
        print(f"response status code: {response.status_code}")
        print(f"response status text: {response.text}")
        return auth_data

    auth_data["token"] = response.json().get("data").get("token")

    return auth_data


def write_token(auth_data):
    """Writes credentials (email, password and token) with empty password to the json file"""

    # removes password from data to be written
    write_data = auth_data
    write_data["password"] = ""

    with open(ABSOLUTE_PATH_TO_TOKEN_FILE, "w", encoding="utf-8") as json_file:
        json.dump(auth_data, json_file, indent=4)


class Command(BaseCommand):
    def handle(self, *args, **options):
        """Handles 'login' command"""

        auth_data = request_get_token()
        if auth_data["token"] is not None:
            print(f"You have logged in, welcome {auth_data['email']}")
            write_token(auth_data)
        else:
            print("Something went wrong... Please try again!")
