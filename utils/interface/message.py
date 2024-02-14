import time
from uuid import UUID
from decimal import Decimal
from django.core.management import call_command
from rich.prompt import Confirm, Prompt, FloatPrompt, InvalidResponse
from django.core.validators import validate_email, DecimalValidator
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rich.progress import track

from contracts.models import Contract
from clients.models import Client
from .console_style import console, draw_subtitle
from teams.models import MANAGEMENT, SALES, SUPPORT, Team
from utils.date_time import validate_date_input, create_date


def show_invalid():
    console.print("Invalid request :sad: Please try again...", style="warning")


def show_error():
    console.print(
        "Oops! An error occurred. Sorry for the inconvenience.", style="error"
    )
    show_commands_and_help_texts()


def show_commands_and_help_texts():
    draw_subtitle("Useful commands")
    console.print("Here are the valid commands that you can use", style="info")
    console.print("For user related info:", style="info")
    call_command("user", "--help")


def ask_for_user_re_input():
    if Confirm.ask("Do you want to retry?", default=True):
        return ""
    else:
        console.print("[b]OK. Bye[/b] :wave:")
        exit()


def prompt_for_email_with_validation(
    current_email: str = "", update_data: bool = False, text: str = "user"
):
    if update_data:
        change_email = prompt_for_bool("Do you want to update email?")
        if not change_email:
            return current_email

    email = ""
    while email.strip() == "":
        email = Prompt.ask(f"[green]Enter {text} email[/green]")
        try:
            validate_email(email)
            return email
        except ValidationError as e:
            console.print(f"[prompt.invalid]{str(e)}")
            email = ask_for_user_re_input()


def prompt_for_password_with_validation(
    current_password: str = "", update_data: bool = False
):
    if update_data:
        change_password = prompt_for_bool("Do you want to change the password?")
        if not change_password:
            return current_password

    password = ""
    while password.strip() == "":
        password = Prompt.ask("[green]Enter password[/green]", password=True)
        try:
            validate_password(password)
            return password
        except ValidationError as e:
            console.print(f"[prompt.invalid]{str(e)}")
            password = ""


def prompt_for_required_string(
    field_name: str, current_text: str = "", update_data: bool = False
):
    if update_data:
        change_text = prompt_for_bool(f"Do you want to make changes to {field_name}?")
        if not change_text:
            return current_text

    text = ""
    while text.strip() == "":
        text = Prompt.ask(f"[green]Enter {field_name}[/green]")

    return text


def prompt_for_role_id(current_team: int = 0, update_data: bool = False):
    if update_data:
        change_team = prompt_for_bool("Do you want to change the team?")
        if not change_team:
            return current_team
    team_name = Prompt.ask(
        "[green]Enter user's team name[/green]",
        choices=[f"{MANAGEMENT}", f"{SALES}", f"{SUPPORT}"],
        default=f"{SUPPORT}",
    )
    role_id = Team.objects.get(name=team_name).id
    return role_id


def prompt_for_date(field_name: str, current_date="", update_data=False):

    retry = True
    while retry:
        if Confirm.ask(
            f"[green]Do you want to enter the {field_name}[/green]", default=True
        ):
            year = Prompt.ask("[green]Year (YYYY)[/green]")
            month = Prompt.ask(
                "[green]Month (MM)[/green]",
            )
            day = Prompt.ask(
                "[green]Day (DD)[/green]",
            )
            if validate_date_input(year, month, day):
                retry = False
                return create_date(year, month, day)
            else:
                retry = True
        else:
            retry = False
            if update_data:
                return current_date.strftime("%Y-%m-%d")
            return None


def prompt_for_bool(text: str):
    if Confirm.ask(f"[green]{text}[/green]", default=True):
        return True
    else:
        return False


def validate_uuid(uuid_to_test, version=4):
    """
    Check if uuid_to_test is a valid UUID.

    Params:
    uuid_to_test : str
    version : {1, 2, 3, 4}

    Returns:
    `True` if uuid_to_test is a valid UUID, otherwise `False`.

    """

    try:
        uuid_obj = UUID(uuid_to_test, version=version)
        contract = Contract.objects.get(id=str(uuid_obj))
    except (ValueError, Contract.DoesNotExist):
        console.print("[prompt.invalid] Invalid id. Please verify the contract id.")
        # Show progress bar
        for i in track(
            range(5), description="[green1]Collecting the list of contracts...[/green1]"
        ):
            time.sleep(0.1)  # Simulate work being done
        call_command("contract", "--list")
        return False, None
    return str(uuid_obj) == uuid_to_test, contract


def prompt_for_contract_id():

    contract_id = ""

    while contract_id.strip() == "":

        contract_id = Prompt.ask("[green]Enter contract id[/green]")
        is_valid, contract = validate_uuid(contract_id)
        if is_valid:
            return contract
        else:
            contract_id = ask_for_user_re_input()


def prompt_for_client_from_email():
    email = ""
    while email.strip() == "":
        email = Prompt.ask("[green]Enter the client's email[/green]")
        try:
            validate_email(email)
            client = Client.objects.get(email=email)
            return client
        except (ValidationError, Client.DoesNotExist):
            console.print(
                "[prompt.invalid]Invalid email. Please verify the client's email."
            )
            # Show progress bar
            for i in track(
                range(5),
                description="[green1]Collecting the list of clients...[/green1]",
            ):
                time.sleep(0.1)  # Simulate work being done
            call_command("client", "--list")
            email = ask_for_user_re_input()


def prompt_for_decimal_value(
    field_name: str, default_value=None, update_data: bool = False, current_amount=None
):
    if update_data:
        change_amount = prompt_for_bool(f"Do you want to update {field_name}?")
        if not change_amount:
            return current_amount

    amount = ""

    while amount.strip() == "":
        try:
            amount = FloatPrompt.ask(
                f"[green]Enter the {field_name}[/green]", default=default_value
            )
            # convert to decimal
            console.print(
                "The amount will be stored with two decimal places", style="info"
            )
            amount = Decimal(amount).quantize(Decimal("1.00"))
            validate_decimal = DecimalValidator(max_digits=12, decimal_places=2)
            validate_decimal(amount)
            return amount
        except (InvalidResponse, ValidationError) as e:
            console.print(f"[prompt.invalid]{str(e)}")
            amount = ask_for_user_re_input()
