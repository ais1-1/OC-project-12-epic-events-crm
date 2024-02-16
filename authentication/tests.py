import os
import pytest
import io
import secrets
import json
from django.urls import reverse, resolve
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from django.http import Http404

from authentication.management.commands.logout import request_logout
from authentication.management.commands.login import request_get_token, write_token
from teams.models import Team
from authentication.views import CustomObtainAuthTokenView


@pytest.mark.django_db
class TestAuthenticationModels:
    def test_user_str(self, superuser):
        """
        Testing if User's __str__ method is properly implemented
        """

        assert (
            str(superuser)
            == f"{superuser.id}: {superuser.full_name} ({superuser.email})"
        )

    def test_superuser_default_role(self, superuser):
        assert superuser.role == Team.get_management_team()

    def test_create_user_without_email(self, django_user_model):
        with pytest.raises(TypeError):
            self.user_without_email = django_user_model.objects.create_user(
                password=secrets.token_hex(10),
                first_name=secrets.token_hex(10),
                last_name=secrets.token_hex(10),
                role=Team.get_sales_team(),
            )

    def test_create_sales_user(self, django_user_model):
        email = f"{secrets.token_hex(10)}@{secrets.token_hex(10)}.com"
        password = secrets.token_hex(10)
        first_name = secrets.token_hex(10)
        last_name = secrets.token_hex(10)
        id = 800
        user = django_user_model.objects.create_user(
            id=id,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role=Team.get_sales_team(),
        )
        assert user.email == email
        assert str(user) == f"{id}: {last_name} {first_name} ({email})"
        assert user.role == Team.get_sales_team()


@pytest.mark.django_db
class TestLogin:

    def setup_method(self):
        self.LOGIN_URL = reverse("obtain_token")

    def test_obtain_token_url(self):
        # Get url from name
        url = self.LOGIN_URL

        assert url == "/obtain-token/"
        assert resolve(url).func, CustomObtainAuthTokenView

    def test_login_with_valid_credentials(
        self,
        sales_user,
        api_client,
    ):
        password = secrets.token_hex(10)
        sales_user.set_password(password)
        sales_user.save()
        data = {
            "email": sales_user.email,
            "password": password,
        }
        response = api_client.post(self.LOGIN_URL, data, timeout=5000)
        assert response.status_code == status.HTTP_200_OK
        assert "token" in response.data.get("data").keys()

    def test_login_with_invalid_email(
        self,
        sales_user,
        api_client,
    ):
        password = secrets.token_hex(10)
        sales_user.set_password(password)
        sales_user.save()
        email = "test@sales.com"
        data = {
            "email": email,
            "password": password,
        }
        response = api_client.post(self.LOGIN_URL, data, timeout=5000)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "We couldn't find a user with these credentials" in response.data.get(
            "message"
        )

    def test_login_without_credentials(
        self,
        api_client,
    ):
        data = {
            "email": "",
            "password": "",
        }
        response = api_client.post(self.LOGIN_URL, data, timeout=5000)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "bad request" in response.data.get("message")


@pytest.mark.django_db
class TestLogout:
    def setup_method(self):
        self.LOGOUT_URL = reverse("logout")

    def test_logout_authenticated(self, sales_user, sales_user_authenticated_client):

        response = sales_user_authenticated_client.post(self.LOGOUT_URL)

        assert response.status_code == status.HTTP_200_OK
        # Test if the token is deleted
        with pytest.raises(Http404):
            get_object_or_404(Token, user=sales_user)
        # Test if the user still exists
        assert sales_user.email is not None


@pytest.mark.django_db
class TestUserViews:
    def setup_method(self):
        self.USERS_URL = reverse("users-list")

    def test_sales_user_access(self, sales_user, sales_user_authenticated_client):
        response = sales_user_authenticated_client.get(self.USERS_URL)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_superuser_access(self, superuser, superuser_authenticated_client):
        response = superuser_authenticated_client.get(self.USERS_URL)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestAuthenticationCommands:
    LOGIN_COMMAND = "login"
    LOGOUT_COMMAND = "logout"
    USER_COMMAND = "user"

    def test_request_get_token_with_unknown_email(self, api_client):
        auth_data = request_get_token(
            email="unknown@email.co", password="blablasecret", client=api_client
        )
        assert auth_data["token"] == ""

    def test_request_get_token_with_valid_credentials(self, superuser, api_client):
        password = "bépo1234"
        auth_data = request_get_token(
            email=superuser.email, password=password, client=api_client
        )
        assert auth_data["email"] == superuser.email
        assert auth_data["token"] != ""

    def test_request_get_token_with_invalid_email(
        self, api_client, capsys, monkeypatch
    ):
        monkeypatch.setattr("sys.stdin", io.StringIO("goodemail@example.com"))
        request_get_token(email="test.com", password="bépoèts12", client=api_client)
        capture1 = capsys.readouterr()
        assert "Enter a valid email" in capture1.out

    def test_request_get_token_with_no_email(self, api_client, capsys, monkeypatch):
        # Input an empty email and then a valid one
        responses = iter(["", "emptyemailtest@example.com"])
        monkeypatch.setattr("builtins.input", lambda: next(responses))
        request_get_token(password="bépoèts12", client=api_client)
        capture1 = capsys.readouterr()
        assert "Enter a valid email" in capture1.out
        assert "Authentication impossible" in capture1.out

    def test_write_token_removes_password(self, test_token_file):
        auth_data = {
            "email": "test@example.com",
            "password": "blabla",
            "token": "tssrr",
        }
        write_token(auth_data, test_token_file)
        with open(test_token_file, "r", encoding="utf-8") as json_file:
            loaded_data = json.load(json_file)
        assert loaded_data["password"] == ""
        assert loaded_data["email"] == auth_data["email"]

    def test_request_logout_not_authenticated_user(
        self, monkeypatch, settings, superuser, test_token_file, api_client, capsys
    ):
        token, created = Token.objects.get_or_create(user=superuser)
        monkeypatch.setattr("sys.stdin", io.StringIO("n"))
        with pytest.raises(SystemExit):
            request_logout(
                str(settings.BASE_DIR) + "/" + test_token_file, api_client, token
            )
        capture = capsys.readouterr()
        assert "renew your token by logging in again" in capture.out
        assert "Do you want to" in capture.out

    def test_request_logout_valid(
        self,
        settings,
        superuser,
        superuser_cli_authenticated,
        api_client,
        test_token_file,
    ):
        assert superuser_cli_authenticated["email"] == superuser.email
        response = request_logout(
            str(settings.BASE_DIR) + "/" + test_token_file,
            api_client,
            Token.objects.get(user=superuser),
        )
        assert response.status_code == 200
        assert os.path.isfile(test_token_file) is False
