import requests
import logging
from django.conf import settings
from django.urls import reverse
from django.contrib.auth import get_user_model

from clients.models import Client
from utils.authentication import authorized_header, ABSOLUTE_PATH_TO_TOKEN_FILE
from utils.interface.message import show_invalid, ask_for_user_re_input
from utils.interface.console_style import console

User = get_user_model()


def get_connected_user(test_token=None, token_file=ABSOLUTE_PATH_TO_TOKEN_FILE):
    """Returns authenticated user"""
    header, auth_data = authorized_header(test_token, token_file)
    connected_user_email = auth_data["email"]
    user = User.objects.get(email=connected_user_email)
    return user


def get_absolute_url(endpoint: str):
    absolute_url = settings.BASE_URL.strip("/") + reverse(endpoint)
    return absolute_url


def request_response_data(
    root_url: str,
    operation: str,
    request_data: dict = None,
    object_id: int = None,
    filter: str = None,
    client=None,
    test_token=None,
    token_file=ABSOLUTE_PATH_TO_TOKEN_FILE,
):
    """Request response for each commands.

    Args:
    root_url (str) - base url for the request
    operation (str) - operation to perform (read, create, delete and update)
    request_data (dict) - data to pass to the request
    object_id (int) - id of the object for read, delete and update
    filter (str) - endpoint of custom actions
    client (test client) - only for test purpose
    test_token (str) - token for test purpose
    token_file (str) - path to json file with token

    Returns:
    response (HttpResponse)
    auth_data (dict) - data from the json file

    """

    absolute_url = root_url

    if object_id:
        absolute_url = absolute_url + str(object_id) + "/"

    if filter:
        absolute_url = absolute_url + filter + "/"

    headers, auth_data = authorized_header(test_token=test_token, token_file=token_file)

    if operation == "read":
        if client:
            response = client.get(
                absolute_url, headers=headers, timeout=5000, format="json"
            )
        else:
            response = requests.get(url=absolute_url, headers=headers, timeout=5000)

    elif operation == "create":
        if client:
            response = client.post(
                absolute_url, request_data, headers=headers, timeout=5000, format="json"
            )

        else:
            response = requests.post(
                url=absolute_url, json=request_data, headers=headers, timeout=5000
            )

    elif operation == "delete":
        # force object id to be specified
        if object_id is None:
            return show_invalid()
        if client:
            response = client.delete(
                absolute_url, request_data, headers=headers, timeout=5000, format="json"
            )
        else:
            response = requests.delete(
                url=absolute_url, json=request_data, headers=headers, timeout=5000
            )

    elif operation == "update":
        if client:
            response = client.patch(
                absolute_url, request_data, headers=headers, timeout=5000, format="json"
            )
        else:
            response = requests.patch(
                url=absolute_url, json=request_data, headers=headers, timeout=5000
            )
    else:
        logging.warning("Invalid operation.")
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


def validate_client_email_input(user_input: str):
    try:
        client = Client.objects.get(email=user_input)
        user_input_invalid = False
        return client, user_input_invalid
    except Client.DoesNotExist:
        console.print("[prompt.invalid] We cannot find a client with this email!")
        empty_user_input = ask_for_user_re_input()
        user_input_invalid = True
        return empty_user_input, user_input_invalid
