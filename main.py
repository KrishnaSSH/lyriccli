import sys
import time
from datetime import timedelta

from rich.console import Console

from core.api import fetch_lyrics
from core.cmus_info import cmus_current_position, cmus_current_song
from core.formatter import format_timestamp

console = Console(color_system="truecolor")


last_line = None
last_song_id = None
lyrics_tuples = []

while True:
    try:
        song = cmus_current_song()
        if not song:
            console.print("[bold red]No song currently playing!")
            exit()
        song_id = (song.artist, song.title)

        # song change
        if song_id != last_song_id:
            console.clear()
            lyrics_tuples = []
            last_line = None

            lyrics = fetch_lyrics(song)
            try:
                synced_lyrics = lyrics["syncedLyrics"]
            except KeyError:
                console.print("\n[bold cyan]cmus closed")
                sys.exit()

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
                console.print(
                    "[bold blue]You would have to guess lyrics yourself for this one :face_with_head-bandage:[/bold blue]"
                )
        last_song_id = song_id
        position = cmus_current_position()
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
        sys.exit()
