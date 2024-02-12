import requests
from django.conf import settings
from django.urls import reverse
from django.contrib.auth import get_user_model


from utils.authentication import authorized_header
from utils.interface.message import show_invalid, ask_for_user_re_input
from utils.interface.console_style import console

User = get_user_model()


def get_absolute_url(endpoint: str):
    absolute_url = settings.BASE_URL.strip("/") + reverse(endpoint)
    return absolute_url


def request_response_data(
    root_url: str,
    operation: str,
    request_data: dict = None,
    object_id: int = None,
    filter: str = None,
):

    absolute_url = root_url

    if object_id:
        absolute_url = absolute_url + str(object_id) + "/"

    headers, auth_data = authorized_header()

    if operation == "read":
        response = requests.get(url=absolute_url, headers=headers, timeout=5000)

    elif operation == "create":
        response = requests.post(
            url=absolute_url, json=request_data, headers=headers, timeout=5000
        )

    elif operation == "delete":
        # force object id to be specified
        if object_id is None:
            return show_invalid()
        response = requests.delete(
            url=absolute_url, json=request_data, headers=headers, timeout=5000
        )

    elif operation == "update":
        response = requests.patch(
            url=absolute_url, json=request_data, headers=headers, timeout=5000
        )
    else:
        return show_invalid()

    return response, auth_data


def validate_user_email_input(user_input: str):
    try:
        user = User.objects.get(email=user_input)
        user_input_invalid = False
        return user, user_input_invalid
    except User.DoesNotExist:
        console.print("[prompt.invalid] We cannot find a user with this email!")
        empty_user_input = ask_for_user_re_input()
        user_input_invalid = True
        return empty_user_input, user_input_invalid
