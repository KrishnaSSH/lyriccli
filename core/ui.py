from rich.console import Console
from rich.prompt import Prompt
from contextlib import contextmanager

ui_console = Console(color_system="truecolor")


def ui_retry_handler() -> None:
    while True:
        ui_console.print("[dim]Press [bold]r[/bold] and Enter to retry[/dim]")
        Prompt.ask("Press r and Enter to retry\n[bold cyan]>[/cyan bold]")
        while True:
            user_input = input("> ").strip().lower()
            if user_input == "r":
                ui_console.clear()


def ui_bye_handler() -> None:
    ui_console.print("\n[bold yellow] :wave: bye")


def ui_now_playing_render(
    title: str | None,
    artist: str | None,
    album_name: str | None,
    genre: str | None,
    duration: str | None,
) -> None:
    ui_console.print(
        f"[bold green]Now playing: [/]{title} by {artist}\n"
        f"[bold green]Album:[/] {album_name}\n"
        f"[bold green]Genre:[/] {genre}\n"
        f"[bold green]Duration:[/] {duration}\n"
    )


@contextmanager
def ui_scraping_render() -> None:
    with ui_console.status("[bold yellow]Scraping"):
        yield


def ui_plain_lyrics_render(plain_lyrics):
    ui_console.print(f"[bold]{plain_lyrics}[/bold]")
    ui_console.print(
        "[bold blue]Synced lyrics aren't available for this one :face_with_head-bandage:[/bold blue]"
    )


def ui_no_lyrics_render():
    ui_console.print(
        "[bold blue]You would have to guess lyrics yourself for this one :face_with_head-bandage:[/bold blue]"
    )
