import os
import pytest
from django.conf import settings
from django.urls import reverse
from django.contrib.auth import get_user_model

""" from authentication.management.commands import login """
from .interface import console_style, message
from .authentication import ABSOLUTE_PATH_TO_TOKEN_FILE, read_token, authorized_header
from .common import validate_user_email_input, get_absolute_url

User = get_user_model()


class TestInterface:

    def test_draw_title(self, capsys):
        console_style.draw_title()
        captured = capsys.readouterr()
        assert "You are using Epic Events'" in captured.out

    def test_draw_title_with_auth_email(self, capsys):
        auth_email = "test@example.com"
        console_style.draw_title(auth_email)
        captured = capsys.readouterr()
        assert "You are using Epic Events'" in captured.out
        assert f"{auth_email}" in captured.out

    def test_draw_subtitle(self, capsys):
        text = "Subtitle"
        console_style.draw_subtitle(text)
        captured = capsys.readouterr()
        assert text in captured.out

    def test_table_with_title_nd_id_column(self, capsys):
        title = "TITLE"
        table = console_style.table_with_title_nd_id_column(title)
        console_style.console.print(table)
        captured = capsys.readouterr()
        assert "TITL" in captured.out
        assert "ID" in captured.out

    def test_show_invalid_message(self, capsys):
        message.show_invalid()
        captured = capsys.readouterr()
        assert "Invalid request" in captured.out

    def test_show_commands_and_help_texts(self, capsys):
        message.show_commands_and_help_texts()
        captured, error = capsys.readouterr()
        assert "Quick start" in captured

    def test_show_error_message(self, capsys):
        message.show_error()
        captured = capsys.readouterr()
        assert "An error occurred" in captured.out
        assert "Useful commands" in captured.out


class TestAuthentication:

    def setup_method(self):
        settings.TOKEN_FILENAME = "testsecret"

    def test_read_token_with_file_not_exist(self):
        if os.path.isfile(ABSOLUTE_PATH_TO_TOKEN_FILE) is True:
            os.remove(ABSOLUTE_PATH_TO_TOKEN_FILE)
        expected = None
        output = read_token()
        assert expected == output

    """ def test_read_token(self, sales_user):
        email = sales_user.email
        token = str(Token.objects.get_or_create(user=sales_user))
        auth_data = {
            "email": email,
            "password": "",
            "token": token,
        }
        login.write_token(auth_data)
        output = read_token()
        expected = auth_data
        assert expected == output """

    def test_authorized_header_with_non_authenticated(self, capsys):
        if os.path.isfile(ABSOLUTE_PATH_TO_TOKEN_FILE) is True:
            os.remove(ABSOLUTE_PATH_TO_TOKEN_FILE)
        with pytest.raises(SystemExit):
            authorized_header()
        captured = capsys.readouterr()
        assert "We couldn't process your request as" in captured.out


@pytest.mark.django_db
class TestCommon:

    def test_validate_user_email_input_valid_input(self, sales_user):
        result_user, result_invalidity = validate_user_email_input(
            str(sales_user.email)
        )

        expected_user = sales_user
        expected_invalidity = False

        assert result_user == expected_user
        assert result_invalidity == expected_invalidity

    def test_get_absolute_url(self):
        url = get_absolute_url("logout")
        expected = settings.BASE_URL.strip("/") + reverse("logout")
        assert url == expected
