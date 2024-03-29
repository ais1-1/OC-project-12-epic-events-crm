import os
import pytest
import io
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status

from teams.models import Team
from events.models import Event
from contracts.models import Contract
from .interface import console_style, message
from .authentication import ABSOLUTE_PATH_TO_TOKEN_FILE, read_token, authorized_header
from . import common
from .date_time import validate_date_input, validate_time_input, create_date

User = get_user_model()


class TestInterface:

    def test_prompt_for_date(self, capsys, monkeypatch):
        year = "2024"
        month = "2"
        day = "1"
        field_name = "test field"
        responses = iter(["y", year, month, day])
        monkeypatch.setattr("builtins.input", lambda: next(responses))
        result = message.prompt_for_date(field_name=field_name)
        capture = capsys.readouterr()

        assert f"want to enter the {field_name}" in capture.out
        assert result == f"{year}-0{month}-0{day}"

    def test_prompt_for_date_include_time(self, capsys, monkeypatch):
        year = "2024"
        month = "2"
        day = "1"
        hour = "14"
        minute = "2"
        field_name = "test field"
        responses = iter(["y", year, month, day, hour, minute])
        monkeypatch.setattr("builtins.input", lambda: next(responses))
        result = message.prompt_for_date(field_name=field_name, include_time=True)
        capture = capsys.readouterr()

        assert f"want to enter the {field_name}" in capture.out
        assert result == f"{year}-0{month}-0{day} {hour}:0{minute}"

    def test_prompt_for_date_invalid_date(self, capsys, monkeypatch):
        year = "2024"
        month = "2"
        day = "30"
        day2 = "2"
        field_name = "test field"
        responses = iter(["y", year, month, day, "y", year, month, day2])
        monkeypatch.setattr("builtins.input", lambda: next(responses))

        result = message.prompt_for_date(field_name=field_name, required=True)
        capture = capsys.readouterr()

        assert f"want to enter the {field_name}" in capture.out
        assert result == f"{year}-0{month}-0{day2}"

    def test_prompt_for_date_not_required(self, capsys, monkeypatch):
        field_name = "test field"
        monkeypatch.setattr("sys.stdin", io.StringIO("n"))

        result = message.prompt_for_date(field_name=field_name)
        capture = capsys.readouterr()

        assert f"want to enter the {field_name}" in capture.out
        assert result is None

    def test_prompt_for_date_required(self, capsys, monkeypatch):
        year = "2024"
        month = "2"
        day2 = "2"
        field_name = "test field"
        responses = iter(["n", "y", "y", year, month, day2, "\n"])
        monkeypatch.setattr("builtins.input", lambda: next(responses))
        result = message.prompt_for_date(field_name=field_name, required=True)
        capture = capsys.readouterr()

        assert f"want to enter the {field_name}" in capture.out
        assert "This field is required to continue" in capture.out
        assert result == f"{year}-0{month}-0{day2}"

    def test_prompt_for_decimal_value(self, capsys, monkeypatch):
        invalid_input = "0123456789101112"
        valid_input = "12"
        field_name = "test field"
        responses = iter([invalid_input, "y", valid_input])
        monkeypatch.setattr("builtins.input", lambda: next(responses))
        result = message.prompt_for_decimal_value(field_name=field_name)
        capture = capsys.readouterr()
        assert result == 12.00
        assert f"Enter the {field_name}" in capture.out
        assert "Ensure that there are no more than 12 digits" in capture.out
        assert "retry" in capture.out

    def test_prompt_for_decimal_value_update(self, capsys, monkeypatch):
        field_name = "test field"
        current_amount = 13.00
        monkeypatch.setattr("sys.stdin", io.StringIO("n"))
        result = message.prompt_for_decimal_value(
            field_name=field_name, update_data=True, current_amount=current_amount
        )
        capture = capsys.readouterr()
        assert result == current_amount
        assert f"want to update {field_name}" in capture.out

    def test_prompt_for_decimal_value_default(self, capsys, monkeypatch):
        field_name = "test field"
        default = 20.00
        monkeypatch.setattr("sys.stdin", io.StringIO("\n"))
        result = message.prompt_for_decimal_value(
            field_name=field_name, default_value=default
        )
        capture = capsys.readouterr()
        assert result == default
        assert f"{default}" in capture.out
        assert f"the {field_name}" in capture.out

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
        with pytest.raises(SystemExit):
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

    @pytest.mark.django_db
    def test_prompt_for_role_id(self, capsys, monkeypatch):
        valid_input = "SUPPORT"
        invalid_input = "sup"
        responses = iter([invalid_input, valid_input])
        monkeypatch.setattr("builtins.input", lambda: next(responses))
        role_id = message.prompt_for_role_id()
        capture = capsys.readouterr()
        assert "Enter user's team name" in capture.out
        assert "Please select one of the available options" in capture.out
        assert role_id == Team.get_support_team().id

    def test_prompt_for_role_id_update(self, capsys, monkeypatch):
        monkeypatch.setattr("sys.stdin", io.StringIO("n"))
        role_id = message.prompt_for_role_id(current_team=1, update_data=True)
        capture = capsys.readouterr()
        assert "Do you want to change the team?" in capture.out
        assert role_id == 1

    def test_prompt_for_bool(self, capsys, monkeypatch):
        text = "Prompt for bool?"
        responses = iter(["y", "n"])
        monkeypatch.setattr("builtins.input", lambda: next(responses))
        result1 = message.prompt_for_bool(text)
        capture1 = capsys.readouterr()
        result2 = message.prompt_for_bool(text)
        capture2 = capsys.readouterr()
        assert result1 is True
        assert text in capture1.out
        assert result2 is False
        assert text in capture2.out

    @pytest.mark.django_db
    def test_validate_uuid(self, signed_contract):
        contract_id_str = str(signed_contract.id)
        valid, contract = message.validate_uuid(contract_id_str)
        assert valid is True
        assert contract == signed_contract

    def test_prompt_for_contract_id(self, capsys, monkeypatch, signed_contract):
        monkeypatch.setattr("sys.stdin", io.StringIO(str(signed_contract.id)))
        result = message.prompt_for_contract_id()
        capture = capsys.readouterr()
        assert result == signed_contract
        assert "Enter contract id" in capture.out

    def test_prompt_for_client_from_email(self, capsys, monkeypatch, epic_client):
        monkeypatch.setattr("sys.stdin", io.StringIO(epic_client.email))
        result = message.prompt_for_client_from_email()
        capture = capsys.readouterr()
        assert result == epic_client
        assert "Enter the client's email" in capture.out

    def test_prompt_for_event_id(self, capsys, monkeypatch, event):
        monkeypatch.setattr("sys.stdin", io.StringIO(str(event.id)))
        result = message.prompt_for_event_id()
        capture = capsys.readouterr()
        assert result == event
        assert "Enter the event's id" in capture.out

    def test_prompt_for_positive_integer(self, capsys, monkeypatch):
        invalid_input = "-12"
        valid_input = "10"
        field_name = "test field"
        responses = iter([invalid_input, "y", valid_input])
        monkeypatch.setattr("builtins.input", lambda: next(responses))
        result = message.prompt_for_positive_integer(field_name=field_name)
        capture = capsys.readouterr()
        assert result == int(valid_input)
        assert f"Enter the {field_name}" in capture.out
        assert f"Invalid {field_name}" in capture.out
        assert "retry" in capture.out

    def test_prompt_for_positive_integer_update(self, capsys, monkeypatch):
        field_name = "Update test"
        current_value = 10
        monkeypatch.setattr("sys.stdin", io.StringIO("n"))
        result = message.prompt_for_positive_integer(
            field_name=field_name, current_value=current_value, update_data=True
        )
        capture = capsys.readouterr()
        assert result == current_value
        assert f"want to update {field_name}" in capture.out

    def test_prompt_for_event_status(self, capsys, monkeypatch):
        # List of tuple
        event_status_choices_tup = list(Event.EVENT_STATUS)
        # Using map for 0 index
        event_status_choices = list(map(lambda x: x[0], event_status_choices_tup))
        invalid_input = "status"
        valid_input = event_status_choices[0]
        responses = iter([invalid_input, valid_input])
        monkeypatch.setattr("builtins.input", lambda: next(responses))
        result = message.prompt_for_event_status()
        capture = capsys.readouterr()
        assert result == valid_input
        assert "Enter event status" in capture.out
        assert valid_input in capture.out
        assert valid_input == "PLANNED"
        assert "one of the available options" in capture.out

    def test_prompt_for_event_status_update(self, capsys, monkeypatch):
        monkeypatch.setattr("sys.stdin", io.StringIO("n"))
        result = message.prompt_for_event_status(
            current_status="COMPLETED", update_data=True
        )
        capture = capsys.readouterr()
        assert result == "COMPLETED"
        assert "change the status" in capture.out

    def test_prompt_for_support_contract_id(self, capsys, monkeypatch, support_user):
        invalid_input = "email"
        valid_input = support_user.email
        responses = iter([invalid_input, valid_input])
        monkeypatch.setattr("builtins.input", lambda: next(responses))
        result = message.prompt_for_support_contract_id()
        capture = capsys.readouterr()

        assert result == support_user.id
        assert "one of the available options" in capture.out
        assert "Enter the support contact email" in capture.out
        assert support_user.email in capture.out

    def test_prompt_for_support_contract_id_update(
        self, capsys, monkeypatch, support_user
    ):
        monkeypatch.setattr("sys.stdin", io.StringIO("n"))
        result = message.prompt_for_support_contract_id(
            update_data=True, current_id=support_user.id
        )
        capture = capsys.readouterr()
        assert result == support_user.id
        assert "change the support team contact" in capture.out

    def test_prompt_for_event_contract_id(self, capsys, event, signed_contract):
        contract_id_choices = list(
            Contract.objects.filter(signed=True)
            .filter(event__isnull=True)
            .values_list("id", flat=True)
        )
        with pytest.raises(SystemExit):
            message.prompt_for_event_contract_id()
        capture = capsys.readouterr()

        assert "All the existing contracts have a connected" in capture.out
        assert len(contract_id_choices) == 0


class TestAuthentication:

    def setup_method(self):
        settings.TOKEN_FILENAME = "testsecret"

    def test_read_token_with_file_not_exist(self):
        if os.path.isfile(ABSOLUTE_PATH_TO_TOKEN_FILE) is True:
            os.remove(ABSOLUTE_PATH_TO_TOKEN_FILE)
        expected = None
        output = read_token()
        assert expected == output

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
        result_user, result_invalidity = common.validate_user_email_input(
            str(sales_user.email)
        )

        expected_user = sales_user
        expected_invalidity = False

        assert result_user == expected_user
        assert result_invalidity == expected_invalidity

    def test_validate_user_email_input_invalid_input(self, capsys, monkeypatch):
        monkeypatch.setattr("sys.stdin", io.StringIO("n"))
        with pytest.raises(SystemExit):
            result_user, result_invalidity = common.validate_user_email_input(
                "unknown@testexample.com"
            )

        capture = capsys.readouterr()

        assert "We cannot find a user with this email" in capture.out
        assert "Bye" in capture.out

    def test_validate_client_email_input_valid_input(self, epic_client):
        result_user, result_invalidity = common.validate_client_email_input(
            str(epic_client.email)
        )

        expected_user = epic_client
        expected_invalidity = False

        assert result_user == expected_user
        assert result_invalidity == expected_invalidity

    def test_validate_client_email_input_invalid_input(self, capsys, monkeypatch):
        monkeypatch.setattr("sys.stdin", io.StringIO("n"))
        with pytest.raises(SystemExit):
            result_user, result_invalidity = common.validate_client_email_input(
                "unknown@testexample.com"
            )

        capture = capsys.readouterr()

        assert "We cannot find a client with this email" in capture.out
        assert "Bye" in capture.out

    def test_get_absolute_url(self):
        url = common.get_absolute_url("logout")
        expected = settings.BASE_URL.strip("/") + reverse("logout")
        assert url == expected

    def test_get_connected_user(
        self,
        settings,
        superuser,
        superuser_cli_authenticated,
        api_client,
        test_token_file,
    ):

        user = common.get_connected_user(
            token_file=str(settings.BASE_DIR) + "/" + test_token_file,
            test_token=Token.objects.get(user=superuser),
        )
        assert user == superuser
        assert superuser_cli_authenticated["email"] == superuser.email

    def test_request_response_data_read(
        self,
        settings,
        test_token_file,
        superuser,
        api_client,
        superuser_cli_authenticated,
    ):
        assert superuser_cli_authenticated["email"] == superuser.email
        response, auth_data = common.request_response_data(
            reverse("users-list"),
            "read",
            client=api_client,
            token_file=str(settings.BASE_DIR) + "/" + test_token_file,
            test_token=Token.objects.get(user=superuser),
        )

        assert auth_data["email"] == superuser_cli_authenticated["email"]
        assert response.status_code == status.HTTP_200_OK

    def test_request_response_data_create(
        self,
        settings,
        test_token_file,
        superuser,
        api_client,
        superuser_cli_authenticated,
    ):
        assert superuser_cli_authenticated["email"] == superuser.email
        data = {
            "email": "test@example.com",
            "password": "bépoooé456",
            "first_name": "firsttestname",
            "last_name": "lasttestname",
            "role": Team.get_sales_team().id,
        }
        response, auth_data = common.request_response_data(
            reverse("users-list"),
            "create",
            request_data=data,
            client=api_client,
            token_file=str(settings.BASE_DIR) + "/" + test_token_file,
            test_token=Token.objects.get(user=superuser),
        )

        assert auth_data["email"] == superuser_cli_authenticated["email"]
        assert response.status_code == status.HTTP_201_CREATED

    def test_request_response_data_delete(
        self,
        settings,
        test_token_file,
        superuser,
        sales_user2,
        api_client,
        superuser_cli_authenticated,
    ):
        assert superuser_cli_authenticated["email"] == superuser.email
        sales_user_id = sales_user2.id
        response, auth_data = common.request_response_data(
            reverse("users-list"),
            "delete",
            object_id=sales_user_id,
            client=api_client,
            token_file=str(settings.BASE_DIR) + "/" + test_token_file,
            test_token=Token.objects.get(user=superuser),
        )
        with pytest.raises(User.DoesNotExist):
            User.objects.get(id=sales_user_id)

        assert auth_data["email"] == superuser_cli_authenticated["email"]
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_request_response_data_delete_no_object_id(
        self,
        capsys,
        settings,
        test_token_file,
        superuser,
        api_client,
        superuser_cli_authenticated,
    ):
        assert superuser_cli_authenticated["email"] == superuser.email
        with pytest.raises(SystemExit):
            response, auth_data = common.request_response_data(
                reverse("users-list"),
                "delete",
                client=api_client,
                token_file=str(settings.BASE_DIR) + "/" + test_token_file,
                test_token=Token.objects.get(user=superuser),
            )
        capture = capsys.readouterr()

        assert "Invalid request" in capture.out

    def test_request_response_data_update(
        self,
        settings,
        test_token_file,
        superuser,
        sales_user2,
        api_client,
        superuser_cli_authenticated,
    ):
        assert superuser_cli_authenticated["email"] == superuser.email
        sales_user_id = sales_user2.id
        data = {
            "last_name": "Updater",
        }
        response, auth_data = common.request_response_data(
            reverse("users-list"),
            "update",
            request_data=data,
            object_id=sales_user_id,
            client=api_client,
            token_file=str(settings.BASE_DIR) + "/" + test_token_file,
            test_token=Token.objects.get(user=superuser),
        )

        assert auth_data["email"] == superuser_cli_authenticated["email"]
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["last_name"] == "Updater"

    def test_request_response_data_invalid(
        self,
        capsys,
        settings,
        test_token_file,
        superuser,
        api_client,
        superuser_cli_authenticated,
    ):
        assert superuser_cli_authenticated["email"] == superuser.email
        with pytest.raises(SystemExit):
            response, auth_data = common.request_response_data(
                reverse("users-list"),
                "invalid",
                client=api_client,
                token_file=str(settings.BASE_DIR) + "/" + test_token_file,
                test_token=Token.objects.get(user=superuser),
            )

        capture = capsys.readouterr()

        assert "Invalid request" in capture.out


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
