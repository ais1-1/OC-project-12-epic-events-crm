from rich.console import Console
from rich.theme import Theme

custom_theme = Theme(
    {
        "info": "cyan",
        "warning": "bright_yellow",
        "danger": "bold red on white",
        "title": "bold red",
        "title-line": "spring_green4",
        "subtitle-line": "spring_green2",
        "error": "bold italic bright_red",
        "success": "bold green4",
    }
)
console = Console(theme=custom_theme)


def draw_title():
    console.rule("[bold red]Epic Events CRM[/bold red]", style="title-line")
    console.print(
        "[bright_cyan]You are using Epic Events' "
        + "Customer Relationship Management application![/bright_cyan]",
        justify="center",
    )


def draw_subtitle(text: str):
    console.rule(f"[bold deep_pink4]{text}[/bold deep_pink4]", style="subtitle-line")
