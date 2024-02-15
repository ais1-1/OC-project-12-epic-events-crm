from functools import partial
from django_rich.management import RichCommand
from rich.console import Console
from rest_framework import status
from rich.prompt import Prompt
from django.conf import settings

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
    prompt_for_event_id,
    prompt_for_date,
    prompt_for_positive_integer,
    prompt_for_event_contract_id,
    prompt_for_support_contract_id,
    prompt_for_event_status,
    prompt_for_required_string,
)

EVENTS_URL = get_absolute_url("events-list")


class Command(RichCommand):
    make_rich_console = partial(Console, theme=custom_theme)

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            "-l", "--list", action="store_true", help="Show list of all the events."
        )
        parser.add_argument(
            "-det",
            "--detail",
            action="store_true",
            help="Read detailed info for a event.",
        )
        parser.add_argument(
            "-c", "--create", action="store_true", help="Create a new event."
        )
        parser.add_argument(
            "-u",
            "--update",
            action="store_true",
            help="Update certain information of a event.",
        )
        parser.add_argument(
            "--delete", action="store_true", help="Delete a event from the database."
        )
        parser.add_argument(
            "--own",
            action="store_true",
            help="Show list of all the events in which you are a contact.",
        )
        parser.add_argument(
            "--withoutsupport",
            action="store_true",
            help="Show list of all the events in which a support team contact is not assigned.",
        )

    def handle(self, *args, **options):
        """Handles 'event' command"""
        connected_user = get_connected_user()
        connected_user_role = connected_user.role
        permitted_to_edit = False
        permitted_to_create = False
        permitted_to_delete = False

        if connected_user_role == Team.get_management_team():
            permitted_to_edit = True
            permitted_to_create = False
            permitted_to_delete = False
            self.console.print(
                f"[bold]Note that a {connected_user_role} team member does not have permission"
                + " to create or delete an event in this interface.[/bold] [success]However,"
                + " you can read events and edit them. If you want to create and delete events,"
                + f" go to the admin page [link]{settings.BASE_URL}epiccrmadmin/[/link][/success]",
                style="warning",
            )
        elif connected_user_role == Team.get_sales_team():
            permitted_to_edit = False
            permitted_to_create = True
            permitted_to_delete = False
            self.console.print(
                f"[bold]Note that a {connected_user_role} team member does not have permission"
                + " to edit or delete an event.[/bold] [success]However, "
                + "you can read events and create for your clients.[/success]",
                style="warning",
            )
        else:
            permitted_to_edit = True
            permitted_to_create = False
            permitted_to_delete = False
            self.console.print(
                f"[bold]Note that a {connected_user_role} team member does not have permission"
                + " to create or delete an event.[/bold] [success]However, "
                + "you can read events and edit them.[/success]",
                style="warning",
            )

        if options["list"]:
            response, auth_data = request_response_data(EVENTS_URL, "read")
            response_dict = response.json()

            if status.is_success(response.status_code):
                table = table_with_title_nd_id_column("Events list")
                table.add_column("Name", style="orchid1")
                table.add_column("Contract ID", style="royal_blue1")
                table.add_column("Client name", style="red1")
                table.add_column("Client contact", no_wrap=True, style="magenta1")
                table.add_column("Start", style="green1")
                table.add_column("End", style="yellow1")
                table.add_column("Support contact", style="red1")
                table.add_column("Location", style="cyan1")
                table.add_column("Attendees", style="red1")
                table.add_column("Status", style="honeydew2")

                for event in response_dict["results"]:
                    table.add_row(
                        str(event["id"]),
                        event["name"],
                        str(event["contract"]),
                        event["client_name"],
                        event["client_contact"],
                        str(event["start_date"]),
                        str(event["end_date"]),
                        f"{event['support_contact_name']}\n"
                        + f"{event['support_contact_email']}",
                        event["location"],
                        str(event["number_of_attendees"]),
                        event["status"],
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

            event = prompt_for_event_id()

            response, auth_data = request_response_data(
                EVENTS_URL, "read", object_id=int(event.id)
            )
            response_dict = response.json()

            if status.is_success(response.status_code):
                table = table_with_title_nd_id_column("Events list")
                table.add_column("Name", style="orchid1")
                table.add_column("Client name", style="red1")
                table.add_column("Client contact", no_wrap=True, style="magenta1")
                table.add_column("Start", no_wrap=True, style="green1")
                table.add_column("End", no_wrap=True, style="yellow1")
                table.add_column("Support contact", no_wrap=True, style="red1")
                table.add_column("Location", style="cyan1")
                table.add_column("Attendees", style="red1")
                table.add_column("Status", style="honeydew2")

                table.add_row(
                    str(response_dict["id"]),
                    response_dict["name"],
                    response_dict["client_name"],
                    response_dict["client_contact"],
                    str(response_dict["start_date"]),
                    str(response_dict["end_date"]),
                    f"{response_dict['support_contact_name']}\n"
                    + f"{response_dict['support_contact_email']}",
                    response_dict["location"],
                    str(response_dict["number_of_attendees"]),
                    response_dict["status"],
                )

                draw_title(auth_data["email"])
                self.console.print(table)
                self.console.print(
                    f"Contract ID: {response_dict['contract']}", style="success"
                )
                self.console.print(f"Notes: {response_dict['notes']}", style="blue1")
                self.console.print(
                    f"Created date: {response_dict['created_date']}",
                    style="green_yellow",
                )
                self.console.print(
                    f"Updated date: {response_dict['updated_date']}",
                    style="medium_purple1",
                )
            elif response.status_code == status.HTTP_403_FORBIDDEN:
                self.console.print(response_dict["detail"], style="forbidden")
            else:
                for data in response_dict:
                    self.console.print(
                        f"[red1]{data}[/red1]: {response_dict[data]}",
                        style="warning",
                    )

        elif options["create"] and permitted_to_create:

            name = prompt_for_required_string(field_name="event name")
            start_date = prompt_for_date(
                field_name="start date", include_time=True, required=True
            )
            end_date = prompt_for_date(
                field_name="end date", include_time=True, required=True
            )
            location = Prompt.ask("[green]Enter event's location[/green]")
            number_of_attendees = prompt_for_positive_integer(
                field_name="number of attendees"
            )
            notes = Prompt.ask("[green]Notes[/green]")
            contract = prompt_for_event_contract_id()
            if connected_user_role == Team.get_management_team():
                support_contact = prompt_for_support_contract_id()
            else:
                support_contact = None
            event_status = prompt_for_event_status()

            event_dict = {
                "name": name,
                "start_date": start_date,
                "end_date": end_date,
                "location": location,
                "number_of_attendees": int(number_of_attendees),
                "notes": notes,
                "contract": contract,
                "status": event_status,
                "support_contact": support_contact,
            }

            response, auth_data = request_response_data(
                EVENTS_URL, "create", request_data=event_dict
            )
            response_dict = response.json()

            if status.is_success(response.status_code):

                table = table_with_title_nd_id_column("Events list")
                table.add_column("Name", style="orchid1")
                table.add_column("Client name", style="red1")
                table.add_column("Client contact", no_wrap=True, style="magenta1")
                table.add_column("Start", no_wrap=True, style="green1")
                table.add_column("End", no_wrap=True, style="yellow1")
                table.add_column("Support contact", no_wrap=True, style="red1")
                table.add_column("Location", style="cyan1")
                table.add_column("Attendees", style="red1")
                table.add_column("Status", style="honeydew2")

                table.add_row(
                    str(response_dict["id"]),
                    response_dict["name"],
                    response_dict["client_name"],
                    response_dict["client_contact"],
                    str(response_dict["start_date"]),
                    str(response_dict["end_date"]),
                    f"{response_dict['support_contact_name']}\n"
                    + f"{response_dict['support_contact_email']}",
                    response_dict["location"],
                    str(response_dict["number_of_attendees"]),
                    response_dict["status"],
                )

                draw_title(auth_data["email"])
                self.console.print(table)
                self.console.print(
                    f"Contract ID: {response_dict['contract']}", style="success"
                )
                self.console.print(f"Notes: {response_dict['notes']}", style="blue1")
                self.console.print(
                    f"Created date: {response_dict['created_date']}",
                    style="green_yellow",
                )
                self.console.print(
                    f"Updated date: {response_dict['updated_date']}",
                    style="medium_purple1",
                )
            elif response.status_code == status.HTTP_403_FORBIDDEN:
                self.console.print(response_dict, style="forbidden")
            else:
                for data in response_dict:
                    self.console.print(
                        f"[red1]{data}[/red1]: {response_dict[data][0]}",
                        style="warning",
                    )

        elif options["delete"] and permitted_to_delete:

            event = prompt_for_event_id()

            response, auth_data = request_response_data(
                EVENTS_URL, "delete", object_id=int(event.id)
            )

            if status.is_success(response.status_code):
                draw_title(auth_data["email"])
                self.console.print(
                    "The event is successfully deleted from the database.",
                    style="success",
                )
            elif response.status_code == status.HTTP_403_FORBIDDEN:
                response_dict = response.json()
                self.console.print(response_dict["detail"], style="forbidden")
            else:
                response_dict = response.json()
                for data in response_dict:
                    self.console.print(
                        f"[red1]{data}[/red1]: {response_dict[data]}",
                        style="warning",
                    )

        elif options["update"] and permitted_to_edit:
            event = prompt_for_event_id()

            name = prompt_for_required_string(
                field_name="event name", update_data=True, current_text=str(event.name)
            )
            start_date = prompt_for_date(
                field_name="start date",
                include_time=True,
                required=True,
                update_data=True,
                current_date=event.start_date,
            )
            end_date = prompt_for_date(
                field_name="end date",
                include_time=True,
                required=True,
                update_data=True,
                current_date=event.end_date,
            )
            location = prompt_for_required_string(
                field_name="location", current_text=event.location, update_data=True
            )
            number_of_attendees = prompt_for_positive_integer(
                field_name="number of attendees",
                current_value=int(event.number_of_attendees),
                update_data=True,
            )
            notes = prompt_for_required_string(
                field_name="notes", current_text=event.notes, update_data=True
            )
            if connected_user_role == Team.get_management_team():
                support_contact = prompt_for_support_contract_id(
                    update_data=True, current_id=event.support_contact.id
                )
            elif event.support_contact:
                support_contact = event.support_contact.id
            else:
                support_contact = None
            event_status = prompt_for_event_status(
                current_status=event.status, update_data=True
            )

            event_dict = {
                "name": name,
                "start_date": start_date,
                "end_date": end_date,
                "location": location,
                "number_of_attendees": int(number_of_attendees),
                "notes": notes,
                "status": event_status,
                "support_contact": support_contact,
            }

            response, auth_data = request_response_data(
                EVENTS_URL, "update", request_data=event_dict, object_id=int(event.id)
            )
            response_dict = response.json()

            if status.is_success(response.status_code):

                table = table_with_title_nd_id_column("Events list")
                table.add_column("Name", style="orchid1")
                table.add_column("Client name", style="red1")
                table.add_column("Client contact", no_wrap=True, style="magenta1")
                table.add_column("Start", no_wrap=True, style="green1")
                table.add_column("End", no_wrap=True, style="yellow1")
                table.add_column("Support contact", no_wrap=True, style="red1")
                table.add_column("Location", style="cyan1")
                table.add_column("Attendees", style="red1")
                table.add_column("Status", style="honeydew2")

                table.add_row(
                    str(response_dict["id"]),
                    response_dict["name"],
                    response_dict["client_name"],
                    response_dict["client_contact"],
                    str(response_dict["start_date"]),
                    str(response_dict["end_date"]),
                    f"{response_dict['support_contact_name']}\n"
                    + f"{response_dict['support_contact_email']}",
                    response_dict["location"],
                    str(response_dict["number_of_attendees"]),
                    response_dict["status"],
                )

                draw_title(auth_data["email"])
                self.console.print(table)
                self.console.print(
                    f"Contract ID: {response_dict['contract']}", style="success"
                )
                self.console.print(f"Notes: {response_dict['notes']}", style="blue1")
                self.console.print(
                    f"Created date: {response_dict['created_date']}",
                    style="green_yellow",
                )
                self.console.print(
                    f"Updated date: {response_dict['updated_date']}",
                    style="medium_purple1",
                )
            elif response.status_code == status.HTTP_403_FORBIDDEN:
                self.console.print(response_dict["detail"], style="forbidden")
            else:
                for data in response_dict:
                    self.console.print(
                        f"[red1]{data}[/red1]: {response_dict[data]}",
                        style="warning",
                    )

        elif options["withoutsupport"]:
            response, auth_data = request_response_data(
                EVENTS_URL, "read", filter="without_support"
            )

            if status.is_success(response.status_code):
                table = table_with_title_nd_id_column("Events list")
                table.add_column("Name", style="orchid1")
                table.add_column("Contract ID", style="royal_blue1")
                table.add_column("Client name", style="red1")
                table.add_column("Client contact", no_wrap=True, style="magenta1")
                table.add_column("Start", style="green1")
                table.add_column("End", style="yellow1")
                table.add_column("Support contact", style="red1")
                table.add_column("Location", style="cyan1")
                table.add_column("Attendees", style="red1")
                table.add_column("Status", style="honeydew2")

                response_dict = response.json()
                for event in response_dict:
                    table.add_row(
                        str(event["id"]),
                        event["name"],
                        str(event["contract"]),
                        event["client_name"],
                        event["client_contact"],
                        str(event["start_date"]),
                        str(event["end_date"]),
                        f"{event['support_contact_name']}\n"
                        + f"{event['support_contact_email']}",
                        event["location"],
                        str(event["number_of_attendees"]),
                        event["status"],
                    )
                draw_title(auth_data["email"])
                self.console.print(table)
            elif response.status_code == status.HTTP_404_NOT_FOUND:
                self.console.print(
                    f"[reverse bold]{response.text}[/reverse bold]",
                    style="warning",
                )
            else:

                self.console.print(
                    f"{response.text}",
                    style="warning",
                )

        elif options["own"]:
            response, auth_data = request_response_data(
                EVENTS_URL, "read", filter="my_events"
            )

            if status.is_success(response.status_code):
                table = table_with_title_nd_id_column("Events list")
                table.add_column("Name", style="orchid1")
                table.add_column("Contract ID", style="royal_blue1")
                table.add_column("Client name", style="red1")
                table.add_column("Client contact", no_wrap=True, style="magenta1")
                table.add_column("Start", style="green1")
                table.add_column("End", style="yellow1")
                table.add_column("Support contact", style="red1")
                table.add_column("Location", style="cyan1")
                table.add_column("Attendees", style="red1")
                table.add_column("Status", style="honeydew2")

                response_dict = response.json()
                for event in response_dict:
                    table.add_row(
                        str(event["id"]),
                        event["name"],
                        str(event["contract"]),
                        event["client_name"],
                        event["client_contact"],
                        str(event["start_date"]),
                        str(event["end_date"]),
                        f"{event['support_contact_name']}\n"
                        + f"{event['support_contact_email']}",
                        event["location"],
                        str(event["number_of_attendees"]),
                        event["status"],
                    )
                draw_title(auth_data["email"])
                self.console.print(table)
            elif response.status_code == status.HTTP_404_NOT_FOUND:
                self.console.print(
                    f"[reverse bold]{response.text}[/reverse bold]",
                    style="warning",
                )
            else:

                self.console.print(
                    f"{response.text}",
                    style="warning",
                )

        else:
            exit()
