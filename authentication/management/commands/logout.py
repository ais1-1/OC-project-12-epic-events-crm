import os
import requests
from functools import partial
from django_rich.management import RichCommand
from rich.console import Console
from django.conf import settings
from django.urls import reverse

from utils.authentication import ABSOLUTE_PATH_TO_TOKEN_FILE, authorized_header
from utils.interface.console_style import custom_theme, draw_title, draw_subtitle

LOGOUT_URL = settings.BASE_URL.strip("/") + reverse("logout")


def request_logout():
    """Logs out the current user"""
    draw_title()
    draw_subtitle("Logout")
    headers = authorized_header()
    if os.path.isfile(ABSOLUTE_PATH_TO_TOKEN_FILE) is True:
        # Delete the credentials file
        os.remove(ABSOLUTE_PATH_TO_TOKEN_FILE)

    response = requests.post(url=LOGOUT_URL, headers=headers, timeout=5000)
    return response


class Command(RichCommand):
    make_rich_console = partial(Console, theme=custom_theme)

    def handle(self, *args, **options):
        """Handles 'logout' command"""
        result = request_logout()
        if result.status_code == 200:
            self.console.print("You have successfully logged out.", style="success")
        else:
            self.console.print("Please try again!", style="warning")
