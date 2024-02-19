import logging
from django_rich.management import RichCommand
from functools import partial
from rich.console import Console
from rest_framework import status
from rich.prompt import Prompt

from teams.models import Team
from utils.common import (
    get_absolute_url,
    request_response_data,
    validate_user_email_input,
    get_connected_user,
)
from utils.interface.console_style import (
    custom_theme,
    table_with_title_nd_id_column,
    draw_title,
)
from utils.interface.message import (
    prompt_for_email_with_validation,
    prompt_for_bool,
    prompt_for_date,
    prompt_for_password_with_validation,
    prompt_for_role_id,
    prompt_for_required_string,
)

USERS_URL = get_absolute_url("users-list")


class Command(RichCommand):
    make_rich_console = partial(Console, theme=custom_theme)

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            "-l", "--list", action="store_true", help="Show list of all the users."
        )
        parser.add_argument(
            "-det",
            "--detail",
            action="store_true",
            help="Read detailed info for a user.",
        )
        parser.add_argument(
            "-c", "--create", action="store_true", help="Create a new user."
        )
        parser.add_argument(
            "-u",
            "--update",
            action="store_true",
            help="Update certain information of a user.",
        )
        parser.add_argument(
            "--delete", action="store_true", help="Delete a user from the database."
        )

    def handle(self, *args, **options):
        """Handles 'user' command"""
        connected_user = get_connected_user()
        connected_user_role = connected_user.role

        if connected_user_role != Team.get_management_team():
            self.console.print(
                f"Sorry, a {connected_user_role} team member "
                + "does not have permission to do any of the actions related a user.",
                style="warning",
            )
            exit()

        if options["list"]:
            response, auth_data = request_response_data(USERS_URL, "read")
            response_dict = response.json()

            if status.is_success(response.status_code):
                table = table_with_title_nd_id_column("Users list")
                table.add_column("Full name", style="orchid1")
                table.add_column("Email", no_wrap=True, style="green1")
                table.add_column("Role", style="yellow1")
                for user in response_dict["results"]:
                    full_name = user["full_name"]
                    if not full_name:
                        full_name = "Unknown"
                    table.add_row(
                        str(user["id"]), full_name, user["email"], user["team_name"]
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
            user_input_invalid = True

            while user_input_invalid:
                user_email = Prompt.ask("[green]Email of the user[/green]")
                user, user_input_invalid = validate_user_email_input(user_email)

            response, auth_data = request_response_data(
                USERS_URL, "read", object_id=int(user.id)
            )
            response_dict = response.json()

            if status.is_success(response.status_code):
                table = table_with_title_nd_id_column("User detail")
                table.add_column("Full name", style="orchid1")
                table.add_column("Email", no_wrap=True, style="green1")
                table.add_column("Role", style="yellow1")
                table.add_column("Staff", style="cyan1")
                table.add_column("Active", style="red1")
                table.add_column("Joined date", no_wrap=True, style="yellow2")
                table.add_column("Created date", no_wrap=True, style="royal_blue1")

                full_name = response_dict["full_name"]
                if not full_name:
                    full_name = "Unknown"
                table.add_row(
                    str(response_dict["id"]),
                    full_name,
                    response_dict["email"],
                    response_dict["team_name"],
                    str(response_dict["is_staff"]),
                    str(response_dict["is_active"]),
                    str(response_dict["joined_date"]),
                    str(response_dict["created_date"]),
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

        elif options["create"]:

            user_email = prompt_for_email_with_validation()
            user_password = prompt_for_password_with_validation()
            user_last_name = prompt_for_required_string("last name").upper()
            user_first_name = prompt_for_required_string("first name").capitalize()
            user_role_id = prompt_for_role_id()
            user_is_staff = prompt_for_bool("Is user a staff?")
            user_is_active = prompt_for_bool("Is user active?")
            user_joined_date = prompt_for_date("joined date")

            user_dict = {
                "email": user_email,
                "password": user_password,
                "last_name": user_last_name,
                "first_name": user_first_name,
                "role": user_role_id,
                "is_staff": user_is_staff,
                "is_active": user_is_active,
                "joined_date": user_joined_date,
            }

            response, auth_data = request_response_data(
                USERS_URL, "create", request_data=user_dict
            )
            response_dict = response.json()

            if status.is_success(response.status_code):
                logging.info(
                    f"User creation, email: {response_dict['email']}",
                    extra={"action by": auth_data["email"]},
                )
                table = table_with_title_nd_id_column("New user's detail")
                table.add_column("Full name", style="orchid1")
                table.add_column("Email", no_wrap=True, style="green1")
                table.add_column("Role", style="yellow1")
                table.add_column("Staff", style="cyan1")
                table.add_column("Active", style="red1")
                table.add_column("Joined date", no_wrap=True, style="yellow2")
                table.add_column("Created date", no_wrap=True, style="royal_blue1")

                full_name = response_dict["full_name"]
                if not full_name:
                    full_name = "Unknown"
                table.add_row(
                    str(response_dict["id"]),
                    full_name,
                    response_dict["email"],
                    response_dict["team_name"],
                    str(response_dict["is_staff"]),
                    str(response_dict["is_active"]),
                    str(response_dict["joined_date"]),
                    str(response_dict["created_date"]),
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

        elif options["delete"]:

            user_input_invalid = True

            while user_input_invalid:
                user_email = Prompt.ask("[green]Email of the user[/green]")
                user, user_input_invalid = validate_user_email_input(user_email)

            response, auth_data = request_response_data(
                USERS_URL, "delete", object_id=int(user.id)
            )

            if status.is_success(response.status_code):
                logging.warning(
                    f"User deleted: {user.email}",
                    extra={"action by": auth_data["email"]},
                )
                draw_title(auth_data["email"])
                self.console.print(
                    "The user is successfully deleted from the database.",
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

        elif options["update"]:
            user_input_invalid = True

            while user_input_invalid:
                user_email = Prompt.ask(
                    "[green]Current email of the user to be modified[/green]"
                )
                user, user_input_invalid = validate_user_email_input(user_email)
            user_email = prompt_for_email_with_validation(
                current_email=user_email, update_data=True
            )
            user_password = prompt_for_password_with_validation(
                current_password=user.password, update_data=True
            )
            user_last_name = prompt_for_required_string(
                "last name", current_text=user.last_name, update_data=True
            ).upper()
            user_first_name = prompt_for_required_string(
                "first name", current_text=user.first_name, update_data=True
            ).capitalize()
            user_team_id = prompt_for_role_id(
                current_team=user.role.id, update_data=True
            )
            user_is_staff = prompt_for_bool("Is user a staff?")
            user_is_active = prompt_for_bool("Is user active?")
            user_joined_date = prompt_for_date(
                "joined date", current_date=user.joined_date, update_data=True
            )

            user_dict = {
                "email": user_email,
                "password": user_password,
                "last_name": user_last_name,
                "first_name": user_first_name,
                "role": user_team_id,
                "is_staff": user_is_staff,
                "is_active": user_is_active,
                "joined_date": user_joined_date,
            }

            response, auth_data = request_response_data(
                USERS_URL, "update", request_data=user_dict, object_id=user.id
            )
            response_dict = response.json()

            if status.is_success(response.status_code):
                logging.info(
                    f"User updated: {response_dict['email']}.",
                    extra={"action by": auth_data["email"]},
                )
                table = table_with_title_nd_id_column("Updated user info")
                table.add_column("Full name", style="orchid1")
                table.add_column("Email", no_wrap=True, style="green1")
                table.add_column("Role", style="yellow1")
                table.add_column("Staff", style="cyan1")
                table.add_column("Active", style="red1")
                table.add_column("Joined date", no_wrap=True, style="yellow2")
                table.add_column("Created date", no_wrap=True, style="royal_blue1")

                full_name = response_dict["full_name"]
                if not full_name:
                    full_name = "Unknown"
                table.add_row(
                    str(response_dict["id"]),
                    full_name,
                    response_dict["email"],
                    response_dict["team_name"],
                    str(response_dict["is_staff"]),
                    str(response_dict["is_active"]),
                    str(response_dict["joined_date"]),
                    str(response_dict["created_date"]),
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
