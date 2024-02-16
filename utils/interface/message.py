import time
from uuid import UUID
from decimal import Decimal
from django.core.management import call_command
from rich.prompt import Confirm, Prompt, FloatPrompt, InvalidResponse, IntPrompt
from django.core.validators import validate_email, DecimalValidator
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rich.progress import track
from django.contrib.auth import get_user_model
from rich import box
from rich.table import Table
from rich.padding import Padding
from django.core.management.base import CommandError

from contracts.models import Contract
from clients.models import Client
from events.models import Event
from .console_style import console, draw_subtitle
from teams.models import MANAGEMENT, SALES, SUPPORT, Team
from utils.date_time import validate_date_input, create_date, validate_time_input

User = get_user_model()


def show_invalid():
    console.print("Invalid request :sad: Please try again...", style="warning")


def show_error():
    console.print(
        "Oops! An error occurred. Sorry for the inconvenience.", style="error"
    )
    show_commands_and_help_texts()


def show_commands_and_help_texts():
    draw_subtitle("Quick start")
    table = Table(
        title=Padding("Useful commands", (1, 1, 0, 1), style="bold"),
        box=box.HORIZONTALS,
        show_lines=True,
    )
    table.add_column("Command", justify="center", style="cyan1", no_wrap=True)
    table.add_column("Usage", justify="right", style="orchid1", no_wrap=True)
    table.add_column("Optional arguments", justify="left", style="green1")
    table.add_row(
        "login",
        "python manage.py login",
        "--email <email>, --password <password>, --help",
    )
    table.add_row("logout", "python manage.py logout", "--help")
    table.add_row(
        "user",
        "python manage.py user",
        "--list, --detail, --create, --update, --delete, --help",
    )
    table.add_row(
        "client",
        "python manage.py client",
        "--list, --detail, --create, --update, --delete, --help",
    )
    table.add_row(
        "contract",
        "python manage.py contract",
        "--list, --detail, --create, --update, --delete, "
        + "--unsigned, --signed, --unpaid, --own, --withoutevent, --help",
    )
    table.add_row(
        "event",
        "python manage.py event",
        "--list, --detail, --create, --update, --delete, --own, --withoutsupport, --help",
    )

    console.print(table)


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

    MAX_TRIES = 3
    count = 0
    p1, p2 = 1, 2  # To make them initially mismatch.
    password_validated = False
    while (
        p1 != p2 or not password_validated
    ) and count < MAX_TRIES:  # pragma: no cover
        p1 = Prompt.ask("[green]Enter password[/green]", password=True)
        p2 = Prompt.ask("[green]Enter password (again)[/green]", password=True)
        if p1 != p2:
            console.print("Passwords do not match. Please try again.", style="warning")
            count += 1
            # Don't validate passwords that don't match.
            continue
        try:
            validate_password(p2)
            password_validated = True
            return p2
        except ValidationError as err:
            console.print(f"[prompt.invalid]{str(err)}")
            count += 1

    if count == MAX_TRIES:
        raise CommandError("Aborting password change after %s attempts" % (count))


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


def prompt_for_date(
    field_name: str,
    current_date="",
    update_data=False,
    include_time: bool = False,
    required: bool = False,
):

    retry = True
    while retry:
        if Confirm.ask(
            f"[green]Do you want to enter the {field_name}[/green]", default=True
        ):
            year = IntPrompt.ask("[green]Year (YYYY)[/green]")
            month = IntPrompt.ask(
                "[green]Month (MM)[/green]",
            )
            day = IntPrompt.ask(
                "[green]Day (DD)[/green]",
            )
            if include_time:
                hour = IntPrompt.ask(
                    "[green]Hour (HH)[/green]",
                )
                minute = IntPrompt.ask(
                    "[green]Minute (mm)[/green]",
                )
            if (
                include_time
                and validate_date_input(year, month, day)
                and validate_time_input(hour, minute)
            ):
                retry = False
                return create_date(year, month, day, hour, minute)
            elif validate_date_input(year, month, day) and not include_time:
                retry = False
                return create_date(year, month, day)
            else:
                retry = True
        else:
            if required and not update_data:
                console.print(
                    "This field is required to continue the process.", style="bold red1"
                )
                empty_string = ask_for_user_re_input()
                if empty_string == "":
                    retry = True
            elif not required:
                retry = False
                return None
            if update_data:
                return current_date.strftime("%Y-%m-%d")
            elif update_data and include_time:
                return current_date.strftime("%Y-%m-%d %HH:%MM")


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


def prompt_for_event_id():

    event_id = ""
    while event_id.strip() == "":
        event_id = IntPrompt.ask("[green]Enter the event's id[/green]")
        try:
            event = Event.objects.get(id=event_id)
            return event
        except Event.DoesNotExist:
            console.print(
                "[prompt.invalid]Invalid event id. Please verify the event's id."
            )
            # Show progress bar
            for i in track(
                range(5),
                description="[green1]Collecting the list of events...[/green1]",
            ):
                time.sleep(0.1)  # Simulate work being done
            call_command("event", "--list")
            event_id = ask_for_user_re_input()


def prompt_for_positive_integer(
    field_name: str, current_value: int = 0, update_data: bool = False
):
    if update_data:
        change_value = prompt_for_bool(f"Do you want to update {field_name}?")
        if not change_value:
            return current_value

    integer = ""

    while integer.strip() == "":
        integer = IntPrompt.ask(f"[green]Enter the {field_name}[/green]")
        if integer >= 0:
            return integer
        else:
            console.print(f"[prompt.invalid] Invalid {field_name}.")
            integer = ask_for_user_re_input()


def prompt_for_event_contract_id():

    contract_id_choices = []

    for contract in (
        Contract.objects.filter(signed=True)
        .filter(event__isnull=True)
        .values_list("id", flat=True)
    ):
        contract_id_choices.append(str(contract))

    contract_id = ""

    while contract_id.strip() == "":

        if len(contract_id_choices) != 0:
            console.print(
                "Here is the list of signed contracts without an associated event.",
                style="info",
            )
            call_command("contract", "--withoutevent")
            contract_id = Prompt.ask(
                "[green]Enter contract id[/green]",
                choices=contract_id_choices,
                show_choices=False,
            )
        else:
            console.print(
                "All the existing contracts have a connected event.", style="info"
            )
            console.print(
                "To create a new event, first you need a signed contract",
                style="warning",
            )
            contract_id = ""
            exit()

    return contract_id


def prompt_for_support_contract_id(update_data: bool = False, current_id: int = 0):

    if update_data:
        change_contact = prompt_for_bool(
            "Do you want to change the support team contact?"
        )
        if not change_contact:
            return current_id

    support_contact_choices = User.objects.filter(
        role=Team.get_support_team()
    ).values_list("email", flat=True)

    support_contact_email = ""

    while support_contact_email.strip() == "":
        console.print("Here is the list of support team members.", style="info")
        for contact in support_contact_choices:
            console.print(contact)
        support_contact_email = Prompt.ask(
            "[green]Enter the support contact email[/green]",
            choices=support_contact_choices,
            show_choices=False,
        )
    support_contact_id = User.objects.get(email=support_contact_email).id

    return support_contact_id


def prompt_for_event_status(current_status: str = "", update_data: bool = False):
    if update_data:
        change_status = prompt_for_bool("Do you want to change the status?")
        if not change_status:
            return current_status

    # List of tuple
    event_status_choices_tup = list(Event.EVENT_STATUS)
    # Using map for 0 index
    event_status_choices = list(map(lambda x: x[0], event_status_choices_tup))

    event_status = Prompt.ask(
        "[green]Enter event status[/green]",
        choices=event_status_choices,
        default=event_status_choices[0],
    )
    return event_status
