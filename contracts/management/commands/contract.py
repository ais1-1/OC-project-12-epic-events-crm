import logging
from functools import partial
from django_rich.management import RichCommand
from rich.console import Console
from rest_framework import status
from rich.prompt import Confirm


from teams.models import Team
from utils.common import (
    get_absolute_url,
    request_response_data,
    get_connected_user,
)
from utils.interface.console_style import (
    custom_theme,
    table_with_title_nd_id_column,
    draw_title,
)
from utils.interface.message import (
    prompt_for_contract_id,
    prompt_for_client_from_email,
    prompt_for_decimal_value,
)

CONTRACTS_URL = get_absolute_url("contracts-list")


class Command(RichCommand):
    make_rich_console = partial(Console, theme=custom_theme)

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            "-l", "--list", action="store_true", help="Show list of all the contracts."
        )
        parser.add_argument(
            "-det",
            "--detail",
            action="store_true",
            help="Read detailed info for a contract.",
        )
        parser.add_argument(
            "-c", "--create", action="store_true", help="Create a new contract."
        )
        parser.add_argument(
            "-u",
            "--update",
            action="store_true",
            help="Update certain information of a contract.",
        )
        parser.add_argument(
            "--delete", action="store_true", help="Delete a contract from the database."
        )
        parser.add_argument(
            "--unsigned",
            action="store_true",
            help="Show list of all the contracts that are not signed.",
        )
        parser.add_argument(
            "--signed",
            action="store_true",
            help="Show list of all the contracts that are signed.",
        )
        parser.add_argument(
            "--unpaid",
            action="store_true",
            help="Show list of all the contracts that have amount due.",
        )
        parser.add_argument(
            "--own",
            action="store_true",
            help="Show list of all the contracts in which you are a contact.",
        )
        parser.add_argument(
            "--withoutevent",
            action="store_true",
            help="Show list of all the signed contracts which is not yet connected to an event.",
        )

    def handle(self, *args, **options):
        """Handles 'contract' command"""

        # Interface for read contract details is accessible by all users,
        # remaining interfaces are accessible by management team users.
        # Update interface is also accessible by sales team users.
        connected_user = get_connected_user()
        connected_user_role = connected_user.role
        permitted = False
        permitted_to_edit = False

        if connected_user_role == Team.get_management_team():
            permitted = True
            permitted_to_edit = True
        elif connected_user_role == Team.get_sales_team():
            permitted = False
            permitted_to_edit = True
            self.console.print(
                f"[bold]Note that a {connected_user_role} team member does not have permission"
                + "  to create or delete a contract.[/bold] [success]However, "
                + "you can read and edit the details of contracts.[/success]",
                style="warning",
            )
        else:
            self.console.print(
                f"[bold]Note that a {connected_user_role} team member does not have permission"
                + " to create, delete or edit a contract.[/bold] [success]However, "
                + "you can read the details of contracts.[/success]",
                style="warning",
            )
            permitted = False
            permitted_to_edit = False

        if options["list"]:
            response, auth_data = request_response_data(CONTRACTS_URL, "read")
            response_dict = response.json()

            if status.is_success(response.status_code):
                table = table_with_title_nd_id_column("Contracts list")
                table.add_column("Client", style="orchid1")
                table.add_column("Sales contact", style="green1")
                table.add_column("Total amount", style="yellow1")
                table.add_column("Amount due", style="cyan1")
                table.add_column("Signed", style="red1")
                table.add_column("Created date", no_wrap=True, style="yellow2")
                table.add_column("Updated date", no_wrap=True, style="royal_blue1")

                for contract in response_dict["results"]:

                    table.add_row(
                        str(contract["id"]),
                        f"{contract['client_name']}\n"
                        + f"[red1]{contract['client_email']}[/red1]",
                        f"{contract['sales_contact_name']}\n"
                        + f"[cyan1]{contract['sales_contact_email']}[/cyan1]",
                        contract["total_amount"],
                        contract["amount_due"],
                        str(contract["signed"]),
                        str(contract["created_date"]),
                        str(contract["updated_date"]),
                    )
                draw_title(auth_data["email"])
                self.console.print(table)
            elif response.status_code == status.HTTP_403_FORBIDDEN:
                logging.warning("Forbidden endpoint.")
                self.console.print(response_dict["detail"], style="forbidden")
            else:
                logging.warning("Something went wrong.")
                for data in response_dict:
                    self.console.print(
                        f"[red1]{data}[/red1]: {response_dict[data][0]}",
                        style="warning",
                    )

        elif options["detail"]:
            contract = prompt_for_contract_id()

            response, auth_data = request_response_data(
                CONTRACTS_URL, "read", object_id=contract.id
            )
            response_dict = response.json()

            if status.is_success(response.status_code):
                table = table_with_title_nd_id_column("Contracts list")
                table.add_column("Client", style="orchid1")
                table.add_column("Sales contact", style="green1")
                table.add_column("Total amount", style="yellow1")
                table.add_column("Amount due", style="cyan1")
                table.add_column("Signed", style="red1")
                table.add_column("Created date", no_wrap=True, style="yellow2")
                table.add_column("Updated date", no_wrap=True, style="royal_blue1")

                table.add_row(
                    str(response_dict["id"]),
                    f"{response_dict['client_name']}\n"
                    + f"[red1]{response_dict['client_email']}[/red1]",
                    f"{response_dict['sales_contact_name']}\n"
                    + f"[cyan1]{response_dict['sales_contact_email']}[/cyan1]",
                    response_dict["total_amount"],
                    response_dict["amount_due"],
                    str(response_dict["signed"]),
                    str(response_dict["created_date"]),
                    str(response_dict["updated_date"]),
                )
                draw_title(auth_data["email"])
                self.console.print(table)
            elif response.status_code == status.HTTP_403_FORBIDDEN:
                logging.warning("Forbidden endpoint.")
                self.console.print(response_dict["detail"], style="forbidden")
            else:
                logging.warning("Something went wrong.")
                for data in response_dict:
                    self.console.print(
                        f"[red1]{data}[/red1]: {response_dict[data]}",
                        style="warning",
                    )

        elif options["create"] and permitted:

            client = prompt_for_client_from_email()
            # Get input for signed value
            if Confirm.ask("[green]Is the contract signed?[/green]", default=True):
                signed = str(True)
            else:
                signed = str(False)

            total_amount = prompt_for_decimal_value(field_name="total amount")
            amount_due = prompt_for_decimal_value(
                field_name="amount due", default_value=0.00
            )

            contract_dict = {
                "client": client.id,
                "signed": signed,
                "total_amount": str(total_amount),
                "amount_due": str(amount_due),
            }

            response, auth_data = request_response_data(
                CONTRACTS_URL, "create", request_data=contract_dict
            )
            response_dict = response.json()

            if status.is_success(response.status_code):
                if signed:
                    logging.info(
                        "A signed contract creation.",
                        extra={
                            "amount due": str(amount_due),
                            "action by": auth_data["email"],
                        },
                    )
                table = table_with_title_nd_id_column("Contracts list")
                table.add_column("Client", style="orchid1")
                table.add_column("Sales contact", style="green1")
                table.add_column("Total amount", style="yellow1")
                table.add_column("Amount due", style="cyan1")
                table.add_column("Signed", style="red1")
                table.add_column("Created date", no_wrap=True, style="yellow2")
                table.add_column("Updated date", no_wrap=True, style="royal_blue1")

                table.add_row(
                    str(response_dict["id"]),
                    f"{response_dict['client_name']}\n"
                    + f"[red1]{response_dict['client_email']}[/red1]",
                    f"{response_dict['sales_contact_name']}\n"
                    + f"[cyan1]{response_dict['sales_contact_email']}[/cyan1]",
                    response_dict["total_amount"],
                    response_dict["amount_due"],
                    str(response_dict["signed"]),
                    str(response_dict["created_date"]),
                    str(response_dict["updated_date"]),
                )
                draw_title(auth_data["email"])
                self.console.print(table)
            elif response.status_code == status.HTTP_403_FORBIDDEN:
                logging.warning("Forbidden endpoint.")
                self.console.print(response_dict["detail"], style="forbidden")
            else:
                logging.warning("Something went wrong.")
                for data in response_dict:
                    self.console.print(
                        f"[red1]{data}[/red1]: {response_dict[data][0]}",
                        style="warning",
                    )

        elif options["delete"] and permitted:

            contract = prompt_for_contract_id()

            response, auth_data = request_response_data(
                CONTRACTS_URL, "delete", object_id=contract.id
            )

            if status.is_success(response.status_code):
                logging.warning("Contract deletion", extra={"user": auth_data["email"]})
                draw_title(auth_data["email"])
                self.console.print(
                    "The contract is successfully deleted from the database.",
                    style="success",
                )
            elif response.status_code == status.HTTP_403_FORBIDDEN:
                logging.warning("Forbidden endpoint.")
                response_dict = response.json()
                self.console.print(response_dict["detail"], style="forbidden")
            else:
                logging.warning("Something went wrong.")
                response_dict = response.json()
                for data in response_dict:
                    self.console.print(
                        f"[red1]{data}[/red1]: {response_dict[data]}",
                        style="warning",
                    )

        elif options["update"] and permitted_to_edit:

            contract = prompt_for_contract_id()

            contract_got_signed = False
            # Get input for signed value if contract is not signed
            if contract.signed is False:
                if Confirm.ask("[green]Is the contract signed?[/green]", default=True):
                    signed = str(True)
                    contract_got_signed = True
                else:
                    contract_got_signed = False
                    signed = str(False)
            else:
                contract_got_signed = False
                signed = str(True)

            total_amount = prompt_for_decimal_value(
                field_name="total amount",
                update_data=True,
                current_amount=contract.total_amount,
            )
            amount_due = prompt_for_decimal_value(
                field_name="amount due",
                default_value=0.00,
                update_data=True,
                current_amount=contract.amount_due,
            )

            contract_dict = {
                "signed": signed,
                "total_amount": str(total_amount),
                "amount_due": str(amount_due),
            }
            response, auth_data = request_response_data(
                CONTRACTS_URL,
                "update",
                request_data=contract_dict,
                object_id=contract.id,
            )
            response_dict = response.json()

            if status.is_success(response.status_code):
                if contract_got_signed:
                    logging.info(
                        "A contract has signed.",
                        extra={
                            "amount due": str(amount_due),
                            "action by": auth_data["email"],
                        },
                    )
                table = table_with_title_nd_id_column("Contracts list")
                table.add_column("Client", style="orchid1")
                table.add_column("Sales contact", style="green1")
                table.add_column("Total amount", style="yellow1")
                table.add_column("Amount due", style="cyan1")
                table.add_column("Signed", style="red1")
                table.add_column("Created date", no_wrap=True, style="yellow2")
                table.add_column("Updated date", no_wrap=True, style="royal_blue1")

                table.add_row(
                    str(response_dict["id"]),
                    f"{response_dict['client_name']}\n"
                    + f"[red1]{response_dict['client_email']}[/red1]",
                    f"{response_dict['sales_contact_name']}\n"
                    + f"[cyan1]{response_dict['sales_contact_email']}[/cyan1]",
                    response_dict["total_amount"],
                    response_dict["amount_due"],
                    str(response_dict["signed"]),
                    str(response_dict["created_date"]),
                    str(response_dict["updated_date"]),
                )
                draw_title(auth_data["email"])
                self.console.print(table)
            elif response.status_code == status.HTTP_403_FORBIDDEN:
                logging.warning("Forbidden endpoint.")
                self.console.print(response_dict["detail"], style="forbidden")
            else:
                logging.warning("Something went wrong.")
                for data in response_dict:
                    self.console.print(
                        f"[red1]{data}[/red1]: {response_dict[data]}",
                        style="warning",
                    )

        elif options["unsigned"]:
            response, auth_data = request_response_data(
                CONTRACTS_URL, "read", filter="unsigned"
            )

            if status.is_success(response.status_code):
                table = table_with_title_nd_id_column("Unsigned contracts list")
                table.add_column("Client", style="orchid1")
                table.add_column("Sales contact", style="green1")
                table.add_column("Total amount", style="yellow1")
                table.add_column("Amount due", style="cyan1")
                table.add_column("Signed", style="red1")
                table.add_column("Created date", no_wrap=True, style="yellow2")
                table.add_column("Updated date", no_wrap=True, style="royal_blue1")

                response_dict = response.json()

                for contract in response_dict:

                    table.add_row(
                        str(contract["id"]),
                        f"{contract['client_name']}\n"
                        + f"[red1]{contract['client_email']}[/red1]",
                        f"{contract['sales_contact_name']}\n"
                        + f"[cyan1]{contract['sales_contact_email']}[/cyan1]",
                        contract["total_amount"],
                        contract["amount_due"],
                        str(contract["signed"]),
                        str(contract["created_date"]),
                        str(contract["updated_date"]),
                    )
                draw_title(auth_data["email"])
                self.console.print(table)
            elif response.status_code == status.HTTP_404_NOT_FOUND:
                logging.warning("Not found")
                self.console.print(
                    f"{response.text}",
                    style="warning",
                )
            else:
                logging.warning("Something went wrong.")

                self.console.print(
                    f"{response.text}",
                    style="warning",
                )

        elif options["unpaid"]:
            response, auth_data = request_response_data(
                CONTRACTS_URL, "read", filter="unpaid"
            )

            if status.is_success(response.status_code):
                table = table_with_title_nd_id_column("Contracts with amount due")
                table.add_column("Client", style="orchid1")
                table.add_column("Sales contact", style="green1")
                table.add_column("Total amount", style="yellow1")
                table.add_column("Amount due", style="cyan1")
                table.add_column("Signed", style="red1")
                table.add_column("Created date", no_wrap=True, style="yellow2")
                table.add_column("Updated date", no_wrap=True, style="royal_blue1")

                response_dict = response.json()

                for contract in response_dict:

                    table.add_row(
                        str(contract["id"]),
                        f"{contract['client_name']}\n"
                        + f"[red1]{contract['client_email']}[/red1]",
                        f"{contract['sales_contact_name']}\n"
                        + f"[cyan1]{contract['sales_contact_email']}[/cyan1]",
                        contract["total_amount"],
                        contract["amount_due"],
                        str(contract["signed"]),
                        str(contract["created_date"]),
                        str(contract["updated_date"]),
                    )
                draw_title(auth_data["email"])
                self.console.print(table)
            elif response.status_code == status.HTTP_404_NOT_FOUND:
                logging.warning("Not found")
                self.console.print(
                    f"{response.text}",
                    style="warning",
                )
            else:
                logging.warning("Something went wrong.")

                self.console.print(
                    f"{response.text}",
                    style="warning",
                )

        elif options["own"]:
            response, auth_data = request_response_data(
                CONTRACTS_URL, "read", filter="own"
            )

            if status.is_success(response.status_code):
                table = table_with_title_nd_id_column("Contracts of your clients")
                table.add_column("Client", style="orchid1")
                table.add_column("Sales contact", style="green1")
                table.add_column("Total amount", style="yellow1")
                table.add_column("Amount due", style="cyan1")
                table.add_column("Signed", style="red1")
                table.add_column("Created date", no_wrap=True, style="yellow2")
                table.add_column("Updated date", no_wrap=True, style="royal_blue1")

                response_dict = response.json()

                for contract in response_dict:

                    table.add_row(
                        str(contract["id"]),
                        f"{contract['client_name']}\n"
                        + f"[red1]{contract['client_email']}[/red1]",
                        f"{contract['sales_contact_name']}\n"
                        + f"[cyan1]{contract['sales_contact_email']}[/cyan1]",
                        contract["total_amount"],
                        contract["amount_due"],
                        str(contract["signed"]),
                        str(contract["created_date"]),
                        str(contract["updated_date"]),
                    )
                draw_title(auth_data["email"])
                self.console.print(table)
            elif response.status_code == status.HTTP_404_NOT_FOUND:
                logging.warning("Not found")
                self.console.print(
                    f"{response.text}",
                    style="warning",
                )
            else:
                logging.warning("Something went wrong.")

                self.console.print(
                    f"{response.text}",
                    style="warning",
                )

        elif options["signed"]:
            response, auth_data = request_response_data(
                CONTRACTS_URL, "read", filter="signed"
            )

            if status.is_success(response.status_code):
                table = table_with_title_nd_id_column("Signed contracts list")
                table.add_column("Client", style="orchid1")
                table.add_column("Sales contact", style="green1")
                table.add_column("Total amount", style="yellow1")
                table.add_column("Amount due", style="cyan1")
                table.add_column("Signed", style="red1")
                table.add_column("Created date", no_wrap=True, style="yellow2")
                table.add_column("Updated date", no_wrap=True, style="royal_blue1")

                response_dict = response.json()

                for contract in response_dict:

                    table.add_row(
                        str(contract["id"]),
                        f"{contract['client_name']}\n"
                        + f"[red1]{contract['client_email']}[/red1]",
                        f"{contract['sales_contact_name']}\n"
                        + f"[cyan1]{contract['sales_contact_email']}[/cyan1]",
                        contract["total_amount"],
                        contract["amount_due"],
                        str(contract["signed"]),
                        str(contract["created_date"]),
                        str(contract["updated_date"]),
                    )
                draw_title(auth_data["email"])
                self.console.print(table)
            elif response.status_code == status.HTTP_404_NOT_FOUND:
                logging.warning("Not found")
                self.console.print(
                    f"{response.text}",
                    style="warning",
                )
            else:
                logging.warning("Something went wrong.")

                self.console.print(
                    f"{response.text}",
                    style="warning",
                )

        elif options["withoutevent"]:
            response, auth_data = request_response_data(
                CONTRACTS_URL, "read", filter="without_event"
            )

            if response.status_code == status.HTTP_200_OK:
                table = table_with_title_nd_id_column("Signed contracts without events")
                table.add_column("Client", style="orchid1")
                table.add_column("Sales contact", style="green1")
                table.add_column("Total amount", style="yellow1")
                table.add_column("Amount due", style="cyan1")
                table.add_column("Signed", style="red1")
                table.add_column("Created date", no_wrap=True, style="yellow2")
                table.add_column("Updated date", no_wrap=True, style="royal_blue1")

                response_dict = response.json()

                for contract in response_dict:

                    table.add_row(
                        str(contract["id"]),
                        f"{contract['client_name']}\n"
                        + f"[red1]{contract['client_email']}[/red1]",
                        f"{contract['sales_contact_name']}\n"
                        + f"[cyan1]{contract['sales_contact_email']}[/cyan1]",
                        contract["total_amount"],
                        contract["amount_due"],
                        str(contract["signed"]),
                        str(contract["created_date"]),
                        str(contract["updated_date"]),
                    )
                draw_title(auth_data["email"])
                self.console.print(table)
            elif response.status_code == status.HTTP_204_NO_CONTENT:
                self.console.print(
                    "All the signed contracts have associated events.",
                    style="success",
                )
            elif response.status_code == status.HTTP_404_NOT_FOUND:
                logging.warning("Not found")
                self.console.print(
                    f"{response.text}",
                    style="warning",
                )
            else:
                logging.warning("Something went wrong.")
                self.console.print(
                    f"{response.text}",
                    style="warning",
                )

        else:
            exit()
