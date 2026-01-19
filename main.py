import sys
import time
from datetime import timedelta

from rich.console import Console

from core.api import fetch_lyrics
from core.cmus_info import cmus_current_position, cmus_current_song, cmus_query
from core.formatter import format_timestamp

console = Console(color_system="truecolor")


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
        song = cmus_current_song(cmus_result)
        if not song:
            console.print("[bold red]No song currently playing!")
            sys.exit(0)
        song_id = (song.artist, song.title)

        # song change
        if song_id != last_song_id:
            console.clear()
            lyrics_tuples.clear()
            last_line = None
            with console.status("[bold yellow]Scraping") as status:
                lyrics = fetch_lyrics(song)
            try:
                synced_lyrics = lyrics["syncedLyrics"]
                plain_lyrics = lyrics["plainLyrics"]
            except KeyError:
                console.print("\n[bold cyan]cmus closed")
                sys.exit(1)

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
            console.print(
                f"[bold green]Now playing: [/bold green]{song.title} by {song.artist}\n"
                f"[bold green]Album:[/bold green] {song.album_name}\n"
                f"[bold green]Genre:[/bold green] {song.genre}\n"
                f"[bold green]Duration:[/bold green] {str(timedelta(seconds=song.song_duration))}"
            )
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
