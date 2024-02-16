import os
import requests
from functools import partial
from django_rich.management import RichCommand
from rich.console import Console
from django.conf import settings
from django.urls import reverse

from utils.authentication import ABSOLUTE_PATH_TO_TOKEN_FILE, authorized_header
from utils.interface.console_style import custom_theme, draw_title, draw_subtitle


def request_logout(
    token_file=ABSOLUTE_PATH_TO_TOKEN_FILE, client=None, test_token=None
):
    """Logs out the current user"""
    draw_title()
    draw_subtitle("Logout")
    headers, auth_data = authorized_header(test_token, token_file)
    if os.path.isfile(token_file) is True:
        # Delete the credentials file
        os.remove(token_file)

    # For test
    if client:
        url = reverse("logout")
        response = client.post(url, headers=headers, timeout=5000)
    else:
        response = requests.post(
            url=settings.BASE_URL.strip("/") + reverse("logout"),
            headers=headers,
            timeout=5000,
        )
    return response


class Command(RichCommand):  # pragma: no cover
    make_rich_console = partial(Console, theme=custom_theme)

    def handle(self, *args, **options):
        """Handles 'logout' command"""
        result = request_logout()
        if result.status_code == 200:
            self.console.print("You have successfully logged out.", style="success")
        else:
            self.console.print("Please try again!", style="warning")
