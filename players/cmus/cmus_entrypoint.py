import sys
import time
from datetime import timedelta

from rich.console import Console

from core.api import fetch_lyrics
from players.cmus.cmus_info import (
    cmus_current_position,
    cmus_current_song,
    cmus_metadata_check,
    cmus_query,
)
from players.cmus.formatter import format_timestamp

console = Console(color_system="truecolor")


def cmus_entrypoint():
    last_line = None
    last_song_id = None
    lyrics_tuples = []
    while True:
        try:
            cmus_result = cmus_query()
        except FileNotFoundError:
            console.print(
                "[red bold]Alert! [white bold]cmus isn't installed in your system install it from [blue underline]https://cmus.github.io/#download"
            )
            sys.exit(1)

        try:
            if not cmus_metadata_check(cmus_result):
                closed_cmus_handler()
                continue

            song = cmus_current_song(cmus_result)
            if not song:
                time.sleep(2)
                continue
            song_id = (song.artist, song.title)

            # song change
            if song_id != last_song_id:
                console.clear()
                lyrics_tuples.clear()
                last_line = None

                if song.song_duration is not None:
                    duration = str(timedelta(seconds=song.song_duration))
                    console.print(
                        f"[bold green]Now playing: [/]{song.title} by {song.artist}\n"
                        f"[bold green]Album:[/] {song.album_name}\n"
                        f"[bold green]Genre:[/] {song.genre}\n"
                        f"[bold green]Duration:[/] {duration}\n"
                    )
                else:
                    console.print(
                        "\n[bold cyan]cmus is not playing anything right now[/bold cyan]"
                    )
                    console.print("[dim]Press [bold]r[/bold] and Enter to retry[/dim]")

                    while True:
                        user_input = input("> ").strip().lower()
                        if user_input == "r":
                            break
                    continue

                with console.status("[bold yellow]Scraping"):
                    lyrics = fetch_lyrics(song)
                try:
                    synced_lyrics = lyrics["syncedLyrics"]
                    plain_lyrics = lyrics["plainLyrics"]
                except KeyError:
                    closed_cmus_handler()
                    continue

                if synced_lyrics:
                    for line in synced_lyrics.splitlines():
                        if line.startswith("[") and "]" in line:
                            timestamp, lyric = (
                                line[1 : line.find("]")],
                                line[line.find("]") + 1 :].strip(),
                            )
                            try:
                                minutes, seconds = timestamp.split(":")
                                total_seconds = int(minutes) * 60 + float(seconds)
                                lyrics_tuples.append((total_seconds, lyric))
                            except ValueError:
                                pass

                if not synced_lyrics:
                    if plain_lyrics:
                        console.print(f"[bold]{plain_lyrics}[/bold]")
                        console.print(
                            "[bold blue]Synced lyrics aren't available for this one :face_with_head-bandage:[/bold blue]"
                        )
                    else:
                        console.print(
                            "[bold blue]You would have to guess lyrics yourself for this one :face_with_head-bandage:[/bold blue]"
                        )
            last_song_id = song_id
            position = cmus_current_position(cmus_result)
            current_line = ""
            for t, lyric in lyrics_tuples:
                if position >= t:
                    current_line = lyric
                else:
                    break

            if current_line != last_line:
                console.print(
                    f"[bold yellow]{format_timestamp(position)} [bold white]{current_line}"
                )
                last_line = current_line
            time.sleep(0.2)
        except KeyboardInterrupt:
            console.print("\n[bold yellow] :wave: bye")
            sys.exit(0)


def closed_cmus_handler():
    console.print("\n[bold cyan]cmus closed[/cyan bold]")
    console.print("[dim]Press [bold]r[/bold] and Enter to retry[/dim]")

    while True:
        user_input = input("> ").strip().lower()
        if user_input == "r":
            console.clear()
            cmus_entrypoint()
            return
