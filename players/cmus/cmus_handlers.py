from core.ui import ui_console, ui_retry_handler


def closed_cmus_handler() -> None:
    ui_console.print("[bold cyan]cmus closed[/cyan bold]")
    ui_retry_handler()


def not_installed_cmus_handler() -> None:
    ui_console.print(
        "[red bold]Alert![/bold red][white bold]cmus isn't installed in your system install it from[/bold white][blue underline]https://cmus.github.io/#download"
    )


def not_playing_cmus_handler() -> None:
    ui_console.print("\n[bold cyan]cmus is not playing anything right now[/bold cyan]")
    ui_retry_handler()
