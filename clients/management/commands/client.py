from functools import partial
from django_rich.management import RichCommand
from rich.console import Console
from rest_framework import status
from rich.prompt import Prompt


from utils.common import (
    get_absolute_url,
    request_response_data,
    validate_client_email_input,
)
from utils.interface.console_style import (
    custom_theme,
    table_with_title_nd_id_column,
    draw_title,
)
from utils.interface.message import (
    prompt_for_email_with_validation,
    prompt_for_required_string,
)

CLIENTS_URL = get_absolute_url("clients-list")


class Command(RichCommand):
    make_rich_console = partial(Console, theme=custom_theme)

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            "-l", "--list", action="store_true", help="Show list of all the clients."
        )
        parser.add_argument(
            "-det",
            "--detail",
            action="store_true",
            help="Read detailed info for a client.",
        )
        parser.add_argument(
            "-c", "--create", action="store_true", help="Create a new client."
        )
        parser.add_argument(
            "-u",
            "--update",
            action="store_true",
            help="Update certain information of a client.",
        )
        parser.add_argument(
            "--delete", action="store_true", help="Delete a client from the database."
        )

    def handle(self, *args, **options):
        """Handles 'client' command"""

        if options["list"]:
            response, auth_data = request_response_data(CLIENTS_URL, "read")
            response_dict = response.json()

            if status.is_success(response.status_code):
                table = table_with_title_nd_id_column("Clients list")
                table.add_column("Full name", style="orchid1")
                table.add_column("Email", no_wrap=True, style="green1")
                table.add_column("Company", style="yellow1")
                table.add_column("Phone", style="cyan1")
                table.add_column("Sales contact", style="red1")
                for client in response_dict["results"]:
                    full_name = client["full_name"]
                    if not full_name:
                        full_name = "Unknown"
                    table.add_row(
                        str(client["id"]),
                        full_name,
                        client["email"],
                        client["company"],
                        client["phone"],
                        client["sales_contact_name"],
                    )
                draw_title(auth_data["email"])
                self.console.print(table)
            elif response.status_code == status.HTTP_403_FORBIDDEN:
                self.console.print(response_dict["detail"], style="forbidden")
            else:
                for data in response_dict:
                    self.console.print(
                        f"[red1]{data}[/red1]: {response_dict[data][0]}",
                        style="warning",
                    )

        elif options["detail"]:
            user_input_invalid = True

            while user_input_invalid:
                client_email = Prompt.ask("[green]Email of the client[/green]")
                client, user_input_invalid = validate_client_email_input(client_email)

            response, auth_data = request_response_data(
                CLIENTS_URL, "read", object_id=int(client.id)
            )
            response_dict = response.json()

            if status.is_success(response.status_code):
                table = table_with_title_nd_id_column("Clients list")
                table.add_column("Full name", style="orchid1")
                table.add_column("Email", no_wrap=True, style="green1")
                table.add_column("Company", style="yellow1")
                table.add_column("Phone", style="cyan1")
                table.add_column("Sales contact", style="red1")
                table.add_column("Note", style="blue1")
                table.add_column("Updated date", no_wrap=True, style="yellow2")
                table.add_column("Created date", no_wrap=True, style="royal_blue1")

                full_name = response_dict["full_name"]
                if not full_name:
                    full_name = "Unknown"
                table.add_row(
                    str(response_dict["id"]),
                    full_name,
                    response_dict["email"],
                    response_dict["company"],
                    response_dict["phone"],
                    f"{response_dict['sales_contact_name']}\n"
                    + f"[yellow1]{response_dict['sales_contact_email']}[/yellow1]",
                    response_dict["note"],
                    str(response_dict["updated_date"]),
                    str(response_dict["created_date"]),
                )
                draw_title(auth_data["email"])
                self.console.print(table)
            elif response.status_code == status.HTTP_403_FORBIDDEN:
                self.console.print(response_dict["detail"], style="forbidden")
            else:
                for data in response_dict:
                    self.console.print(
                        f"[red1]{data}[/red1]: {response_dict[data][0]}",
                        style="warning",
                    )

        elif options["create"]:

            client_email = prompt_for_email_with_validation(text="client")
            client_last_name = prompt_for_required_string("last name").upper()
            client_first_name = prompt_for_required_string("first name").capitalize()
            client_phone = Prompt.ask("[green]Enter phone number[/green]")
            client_company = Prompt.ask(
                "[green]Enter the name of client's company[/green]"
            )
            note = Prompt.ask("[green]Note[/green]")

            client_dict = {
                "email": client_email,
                "last_name": client_last_name,
                "first_name": client_first_name,
                "phone": client_phone,
                "company": client_company,
                "note": note,
            }

            response, auth_data = request_response_data(
                CLIENTS_URL, "create", request_data=client_dict
            )
            response_dict = response.json()

            if status.is_success(response.status_code):
                table = table_with_title_nd_id_column("Your new client's detail")
                table.add_column("Full name", style="orchid1")
                table.add_column("Email", no_wrap=True, style="green1")
                table.add_column("Phone", style="yellow1")
                table.add_column("Company", style="cyan1")
                table.add_column("Sales contact", style="red1")
                table.add_column("Note", style="blue1")
                table.add_column("Updated date", no_wrap=True, style="yellow2")
                table.add_column("Created date", no_wrap=True, style="royal_blue1")

                full_name = response_dict["full_name"]
                if not full_name:
                    full_name = "Unknown"
                table.add_row(
                    str(response_dict["id"]),
                    full_name,
                    response_dict["email"],
                    response_dict["phone"],
                    str(response_dict["company"]),
                    f"{response_dict['sales_contact_name']}\n"
                    + f"[yellow1]{response_dict['sales_contact_email']}[/yellow1]",
                    response_dict["note"],
                    str(response_dict["updated_date"]),
                    str(response_dict["created_date"]),
                )
                draw_title(auth_data["email"])
                self.console.print(table)
            elif response.status_code == status.HTTP_403_FORBIDDEN:
                self.console.print(response_dict["detail"], style="forbidden")
            else:
                for data in response_dict:
                    self.console.print(
                        f"[red1]{data}[/red1]: {response_dict[data][0]}",
                        style="warning",
                    )

        elif options["delete"]:

            user_input_invalid = True

            while user_input_invalid:
                client_email = Prompt.ask("[green]Email of the client[/green]")
                client, user_input_invalid = validate_client_email_input(client_email)

            response, auth_data = request_response_data(
                CLIENTS_URL, "delete", object_id=int(client.id)
            )

            if status.is_success(response.status_code):
                draw_title(auth_data["email"])
                self.console.print(
                    "The client is successfully deleted from the database.",
                    style="success",
                )
            elif response.status_code == status.HTTP_403_FORBIDDEN:
                response_dict = response.json()
                self.console.print(response_dict["detail"], style="forbidden")
            else:
                response_dict = response.json()
                for data in response_dict:
                    self.console.print(
                        f"[red1]{data}[/red1]: {response_dict[data][0]}",
                        style="warning",
                    )

        elif options["update"]:
            user_input_invalid = True

            while user_input_invalid:
                client_email = Prompt.ask(
                    "[green]Current email of the client to be modified[/green]"
                )
                client, user_input_invalid = validate_client_email_input(client_email)

            client_email = prompt_for_email_with_validation(
                current_email=client_email, update_data=True, text="client"
            )
            client_last_name = prompt_for_required_string(
                "last name", current_text=client.last_name, update_data=True
            ).upper()
            client_first_name = prompt_for_required_string(
                "first name", current_text=client.first_name, update_data=True
            ).capitalize()
            client_phone = prompt_for_required_string(
                "phone number", current_text=client.phone, update_data=True
            )
            client_company = prompt_for_required_string(
                "company name", current_text=client.company, update_data=True
            )
            note = prompt_for_required_string(
                "note", current_text=client.note, update_data=True
            )

            client_dict = {
                "email": client_email,
                "last_name": client_last_name,
                "first_name": client_first_name,
                "phone": client_phone,
                "company": client_company,
                "note": note,
            }

            response, auth_data = request_response_data(
                CLIENTS_URL, "update", request_data=client_dict, object_id=client.id
            )
            response_dict = response.json()

            if status.is_success(response.status_code):
                table = table_with_title_nd_id_column("Your new client's detail")
                table.add_column("Full name", style="orchid1")
                table.add_column("Email", no_wrap=True, style="green1")
                table.add_column("Phone", style="yellow1")
                table.add_column("Company", style="cyan1")
                table.add_column("Sales contact", style="red1")
                table.add_column("Note", style="blue1")
                table.add_column("Updated date", no_wrap=True, style="yellow2")
                table.add_column("Created date", no_wrap=True, style="royal_blue1")

                full_name = response_dict["full_name"]
                if not full_name:
                    full_name = "Unknown"
                table.add_row(
                    str(response_dict["id"]),
                    full_name,
                    response_dict["email"],
                    response_dict["phone"],
                    str(response_dict["company"]),
                    f"{response_dict['sales_contact_name']}\n"
                    + f"[yellow1]{response_dict['sales_contact_email']}[/yellow1]",
                    response_dict["note"],
                    str(response_dict["updated_date"]),
                    str(response_dict["created_date"]),
                )
                draw_title(auth_data["email"])
                self.console.print(table)
            elif response.status_code == status.HTTP_403_FORBIDDEN:
                self.console.print(response_dict["detail"], style="forbidden")
