import os
import pytest
import io
from django.conf import settings
from django.urls import reverse
from django.contrib.auth import get_user_model

""" from authentication.management.commands import login """
from .interface import console_style, message
from .authentication import ABSOLUTE_PATH_TO_TOKEN_FILE, read_token, authorized_header
from .common import validate_user_email_input, get_absolute_url
from .date_time import validate_date_input, validate_time_input, create_date

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

    def test_ask_for_user_re_input(self, capsys, monkeypatch):
        responses = iter(["y", "n"])
        monkeypatch.setattr("builtins.input", lambda: next(responses))
        # Answers y
        output1 = message.ask_for_user_re_input()
        captured1 = capsys.readouterr()
        # Answers 'n'
        with pytest.raises(SystemExit):
            message.ask_for_user_re_input()
        captured2 = capsys.readouterr()
        assert "Do you want to retry" in captured1.out
        assert "Do you want to retry" in captured2.out
        assert output1 == ""
        assert "OK. Bye" in captured2.out

    def test_prompt_for_email_with_validation_not_update_data(
        self, capsys, monkeypatch
    ):
        valid_email = "validemail@test.com"
        invalid_email_input = "invalidemail"
        responses = iter([valid_email, invalid_email_input, "n"])
        monkeypatch.setattr("builtins.input", lambda: next(responses))
        output1 = message.prompt_for_email_with_validation()
        with pytest.raises(SystemExit):
            message.prompt_for_email_with_validation()
        capture = capsys.readouterr()

        assert output1 == valid_email
        assert "Enter a valid email" in capture.out
        assert "Do you want to retry" in capture.out

    def test_prompt_for_email_with_validation_update_data(self, capsys, monkeypatch):
        valid_email = "validemail@test.com"
        monkeypatch.setattr("sys.stdin", io.StringIO("n"))
        output1 = message.prompt_for_email_with_validation(
            current_email=valid_email, update_data=True, text="test"
        )
        capture = capsys.readouterr()

        assert output1 == valid_email
        assert "Do you want to update" in capture.out

    def test_prompt_for_password_with_validation_update_data(self, capsys, monkeypatch):
        valid_password = "testsecret123"
        monkeypatch.setattr("sys.stdin", io.StringIO("n"))
        output1 = message.prompt_for_password_with_validation(
            current_password=valid_password, update_data=True
        )
        capture = capsys.readouterr()

        assert output1 == valid_password
        assert "Do you want to change the password" in capture.out

    def test_prompt_for_required_string(self, capsys, monkeypatch):
        field_name = "test field"
        field_value = "test value"
        monkeypatch.setattr("sys.stdin", io.StringIO(field_value))
        output = message.prompt_for_required_string(field_name)
        capture = capsys.readouterr()

        assert output == field_value
        assert f"Enter {field_name}" in capture.out

    def test_prompt_for_required_string_update_data(self, capsys, monkeypatch):
        field_name = "test field"
        field_value = "test value"
        monkeypatch.setattr("sys.stdin", io.StringIO("n"))
        output = message.prompt_for_required_string(
            field_name, current_text=field_value, update_data=True
        )
        capture = capsys.readouterr()

        assert output == field_value
        assert f"changes to {field_name}" in capture.out


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


class TestDateTime:

    def test_validate_date_input_with_invalid_year(self, capsys):
        negative_year = -1
        year_in_nineteenth_century = 1800
        month = 2
        day = 1
        result1 = validate_date_input(negative_year, month, day)
        captured1 = capsys.readouterr()
        result2 = validate_date_input(year_in_nineteenth_century, month, day)
        captured2 = capsys.readouterr()
        assert result1 is False
        assert result2 is False
        assert "Year is invalid" in captured1.out
        assert "Year is invalid" in captured2.out

    def test_validate_date_input_with_invalid_month(self, capsys):
        year = 2024
        month1 = 0
        month2 = 24
        day = 1
        result1 = validate_date_input(year, month1, day)
        captured1 = capsys.readouterr()
        result2 = validate_date_input(year, month2, day)
        captured2 = capsys.readouterr()
        assert result1 is False
        assert result2 is False
        assert "Month is invalid" in captured1.out
        assert "Month is invalid" in captured2.out

    def test_validate_date_input_with_invalid_day(self, capsys):
        year = 2025
        month1 = 2
        day1 = 29
        month2 = 1
        day2 = 32
        result1 = validate_date_input(year, month1, day1)
        captured1 = capsys.readouterr()
        result2 = validate_date_input(year, month2, day2)
        captured2 = capsys.readouterr()
        assert result1 is False
        assert result2 is False
        assert "Day is invalid" in captured1.out
        assert "Day is invalid" in captured2.out

    def test_validate_date_input_with_valid_args(self):
        year = 2024
        month = 4
        day = 4
        result = validate_date_input(year, month, day)
        assert result is True

    def test_validate_time_input(self):
        hour = 14
        minute = 42
        result = validate_time_input(hour, minute)
        assert result is True

    def test_validate_time_input_invalid(self, capsys):
        hour1 = 25
        minute1 = 14
        hour2 = 12
        minute2 = 62
        result1 = validate_time_input(hour1, minute1)
        captured1 = capsys.readouterr()
        result2 = validate_time_input(hour2, minute2)
        captured2 = capsys.readouterr()
        assert result1 is False
        assert result2 is False
        assert "Hour is invalid" in captured1.out
        assert "Minute is invalid" in captured2.out

    def test_create_date_valid(self):
        year = 2024
        month = 1
        day = 2
        hour = 4
        minute = 5
        result = create_date(year, month, day, hour, minute)
        assert result == f"{year}-0{month}-0{day} 0{hour}:0{minute}"

    def test_create_date_without_time(self):
        year = 2025
        month = 2
        day = 5
        result = create_date(year, month, day)
        assert result == f"{year}-0{month}-0{day}"
