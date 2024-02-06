import pytest
import secrets
from rest_framework.test import APIClient
from django.urls import reverse
from django.conf import settings

from clients.models import Client
from teams.models import Team
from contracts.models import Contract

AUTH_URL = settings.BASE_URL.strip("/") + reverse("obtain_token")
LOGOUT_URL = settings.BASE_URL.strip("/") + reverse("logout")
ABSOLUTE_PATH_TO_TOKEN_FILE = (
    str(settings.BASE_DIR) + "/" + str(settings.TOKEN_FILENAME) + ".json"
)


@pytest.fixture(autouse=True)
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def superuser(django_user_model):
    user = django_user_model.objects.create_superuser(
        email=f"{secrets.token_hex(10)}@{secrets.token_hex(10)}.com",
        password=secrets.token_hex(10),
        first_name=secrets.token_hex(10),
        last_name=secrets.token_hex(10),
    )
    return user


@pytest.fixture
def sales_user(django_user_model):
    user = django_user_model.objects.create_user(
        email=f"{secrets.token_hex(10)}@{secrets.token_hex(10)}.com",
        password=secrets.token_hex(10),
        first_name=secrets.token_hex(10),
        last_name=secrets.token_hex(10),
        role=Team.get_sales_team(),
    )
    return user


@pytest.fixture
def support_user(django_user_model):
    user = django_user_model.objects.create_user(
        email=f"{secrets.token_hex(10)}@{secrets.token_hex(10)}.com",
        password=secrets.token_hex(10),
        first_name=secrets.token_hex(10),
        last_name=secrets.token_hex(10),
        role=Team.get_support_team(),
    )
    return user


@pytest.fixture
def client(sales_user):
    client = Client.objects.create(
        email=f"{secrets.token_hex(10)}@{secrets.token_hex(10)}.com",
        first_name=secrets.token_hex(10),
        last_name=secrets.token_hex(10),
        sales_contact=sales_user,
    )
    return client


@pytest.fixture
def client_without_contact():
    client = Client.objects.create(
        email=f"{secrets.token_hex(10)}@{secrets.token_hex(10)}.com",
        first_name=secrets.token_hex(10),
        last_name=secrets.token_hex(10),
    )
    return client


@pytest.fixture
def signed_contract(client):
    contract = Contract.objects.create(total_amount=1500, signed=True, client=client)
    return contract


@pytest.fixture
def unsigned_contract_without_contact(client_without_contact):
    contract = Contract.objects.create(
        total_amount=1500, signed=False, client=client_without_contact
    )
    return contract


@pytest.fixture
def unsigned_contract_without_client(sales_user):
    contract = Contract.objects.create(
        total_amount=1500, signed=False, sales_contact=sales_user
    )
    return contract


def get_token_auth_client(api_client, user):
    LOGIN_URL = reverse("obtain_token")

    password = secrets.token_hex(10)
    user.set_password(password)
    user.save()
    data = {
        "email": user.email,
        "password": password,
    }
    response = api_client.post(LOGIN_URL, data, timeout=5000)
    token = response.json().get("data").get("token")
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

    return api_client


@pytest.fixture
def sales_user_authenticated_client(api_client, sales_user):
    api_client = get_token_auth_client(api_client, sales_user)
    return api_client


@pytest.fixture
def superuser_authenticated_client(api_client, superuser):
    api_client = get_token_auth_client(api_client, superuser)
    return api_client
