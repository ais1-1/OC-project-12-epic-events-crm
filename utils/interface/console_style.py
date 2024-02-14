from rich.console import Console
from rich.theme import Theme
from rich.table import Table
from rich import box
from rich.padding import Padding


custom_theme = Theme(
    {
        "info": "cyan1",
        "warning": "bright_yellow",
        "danger": "bold red on white",
        "title": "bold red",
        "title-line": "spring_green4",
        "subtitle-line": "spring_green2",
        "error": "bold italic bright_red",
        "success": "bold green4",
        "forbidden": "dark_orange",
        "prompt": "green",
    }
)
console = Console(theme=custom_theme)


def draw_title(auth_email: str = None):
    console.rule("[bold red]Epic Events CRM[/bold red]", style="title-line")
    console.print(
        "[bright_cyan]You are using Epic Events' "
        + "Customer Relationship Management application![/bright_cyan]",
        justify="center",
    )
    if auth_email:
        console.print(
            "You have logged in using",
            f"[red1]{auth_email}[/red1]",
            style="info",
            justify="center",
        )


def draw_subtitle(text: str):
    console.rule(f"[bold deep_pink4]{text}[/bold deep_pink4]", style="subtitle-line")


def table_with_title_nd_id_column(title: str):
    table = Table(
        title=Padding(title, (1, 1, 0, 1), style="bold"),
        box=box.ROUNDED,
        show_lines=True,
    )
    table.add_column("ID", justify="right", style="cyan1", no_wrap=True)
    return table
