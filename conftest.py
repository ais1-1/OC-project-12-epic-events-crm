import pytest
import secrets
import datetime
from rest_framework.test import APIClient
from django.urls import reverse
from django.utils.timezone import make_aware

from clients.models import Client
from teams.models import Team
from contracts.models import Contract
from events.models import Event
from authentication.management.commands.login import request_get_token, write_token


@pytest.fixture(autouse=True)
def api_client():
    client = APIClient()
    return client


@pytest.fixture(autouse=True)
def test_token_file(settings):
    settings.TOKEN_FILENAME = "testsecret.json"
    return settings.TOKEN_FILENAME


@pytest.fixture
def superuser(django_user_model):
    user = django_user_model.objects.create_superuser(
        email="manager@epicevents.com",
        password="bépo1234",
        first_name=secrets.token_hex(10),
        last_name=secrets.token_hex(10),
    )
    return user


@pytest.fixture
def superuser_cli_authenticated(superuser, api_client, test_token_file):
    password = "bépo1234"
    auth_data = request_get_token(
        email=superuser.email, password=password, client=api_client
    )
    write_token(auth_data, test_token_file)
    return auth_data


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
def sales_user2(django_user_model):
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
def epic_client(sales_user):
    client = Client.objects.create(
        email=f"{secrets.token_hex(10)}@{secrets.token_hex(10)}.com",
        first_name=secrets.token_hex(10),
        last_name=secrets.token_hex(10),
        sales_contact=sales_user,
    )
    return client


@pytest.fixture
def epic_client2(sales_user2):
    client = Client.objects.create(
        email=f"{secrets.token_hex(10)}@{secrets.token_hex(10)}.com",
        first_name=secrets.token_hex(10),
        last_name=secrets.token_hex(10),
        sales_contact=sales_user2,
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
def signed_contract(epic_client):
    contract = Contract.objects.create(
        total_amount=1500, signed=True, client=epic_client
    )
    return contract


@pytest.fixture
def unsigned_contract(epic_client):
    contract = Contract.objects.create(
        total_amount=1500, signed=False, client=epic_client
    )
    return contract


@pytest.fixture
def unpaid_contract(epic_client):
    contract = Contract.objects.create(
        total_amount=1500, amount_due=100, signed=False, client=epic_client
    )
    return contract


@pytest.fixture
def signed_contract2(epic_client2):
    contract = Contract.objects.create(
        total_amount=1500, amount_due=100.00, signed=True, client=epic_client2
    )
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


@pytest.fixture
def event(signed_contract, support_user):
    event = Event.objects.create(
        name=secrets.token_hex(10),
        start_date=make_aware(datetime.datetime(2024, 3, 8)),
        end_date=make_aware(datetime.datetime(2024, 3, 10)),
        contract=signed_contract,
        support_contact=support_user,
    )
    return event


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
def sales_user2_authenticated_client(api_client, sales_user2):
    api_client = get_token_auth_client(api_client, sales_user2)
    return api_client


@pytest.fixture
def support_user_authenticated_client(api_client, support_user):
    api_client = get_token_auth_client(api_client, support_user)
    return api_client


@pytest.fixture
def superuser_authenticated_client(api_client, superuser):
    api_client = get_token_auth_client(api_client, superuser)
    return api_client
