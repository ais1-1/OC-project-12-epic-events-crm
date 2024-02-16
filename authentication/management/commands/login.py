import requests
import json
import time
from functools import partial
from rich.progress import track
from django_rich.management import RichCommand
from rich.console import Console
from rich.prompt import Prompt
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.urls import reverse
from django.conf import settings

from utils.interface.console_style import (
    console,
    custom_theme,
    draw_title,
    draw_subtitle,
)
from utils.authentication import ABSOLUTE_PATH_TO_TOKEN_FILE
from utils.interface.message import show_commands_and_help_texts


def request_get_token(email="", password="", client=None):
    """
    Generate token on request.
    Returns dict containing credentials and token value.
    """

    draw_title()
    draw_subtitle("Login")

    if email.strip() != "":

        try:
            validate_email(email)
        except ValidationError as e:
            console.print(f"[prompt.invalid]{str(e)}")
            email = ""

    if password.strip() != "":
        try:
            validate_password(password)
        except ValidationError as e:
            console.print(f"[prompt.invalid]{str(e)}")
            password = ""

    while email.strip() == "":
        email = Prompt.ask("[green]Enter your email[/green]")
        try:
            validate_email(email)
        except ValidationError as e:
            console.print(f"[prompt.invalid]{str(e)}")
            email = ""

    while password.strip() == "":  # pragma: no cover
        password = Prompt.ask("[green]Enter password[/green]", password=True)
        try:
            validate_password(password)
        except ValidationError as e:
            console.print(f"[prompt.invalid]{str(e)}")
            password = ""

    # token not None for test
    auth_data = {"email": email, "password": password, "token": ""}

    # For test
    if client:
        url = reverse("obtain_token")
        response = client.post(url, data=auth_data, timeout=5000)
    else:
        response = requests.post(
            url=settings.BASE_URL.strip("/") + reverse("obtain_token"),
            data=auth_data,
            timeout=5000,
        )

    # Show progress bar
    for i in track(range(100), description="Processing your request..."):
        time.sleep(0.01)  # Simulate work being done

    if response.status_code != 200:
        response_dict = response.json()
        console.print("Authentication impossible:warning:", style="error")
        console.print(f"response status code: {response.status_code}", style="info")
        console.print(f"response status text: {response_dict['message']}", style="info")
        return auth_data

    auth_data["token"] = response.json().get("data").get("token")

    return auth_data


def write_token(auth_data, token_file=ABSOLUTE_PATH_TO_TOKEN_FILE):
    """Writes credentials (email, password and token) with empty password to the json file"""

    # removes password from data to be written
    write_data = auth_data
    write_data["password"] = ""

    with open(token_file, "w", encoding="utf-8") as json_file:
        json.dump(auth_data, json_file, indent=4)


class Command(RichCommand):  # pragma: no cover

    make_rich_console = partial(Console, theme=custom_theme)

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument("--email", help="Provide the email to authenticate.")
        parser.add_argument("--password", help="Provide your password to authenticate.")

    def handle(self, *args, **options):
        """Handles 'login' command"""

        if options["email"]:
            email = options["email"]
        else:
            email = ""

        if options["password"]:
            password = options["password"]
            self.console.print(
                "It is highly recommended to not to give your password in options.",
                style="warning",
            )
        else:
            password = ""

        auth_data = request_get_token(email, password)
        if auth_data["token"] is not None:
            self.console.print(
                "You have successfully logged in with the email "
                + f"[bold blue]{auth_data['email']}[/bold blue] :smile:",
                style="success",
            )
            write_token(auth_data)
            # Show progress bar
            for i in track(range(100), description="Collecting useful commands..."):
                time.sleep(0.01)  # Simulate work being done
            show_commands_and_help_texts()
        else:
            self.console.print(
                "Something went wrong... Please try again!", style="warning"
            )
