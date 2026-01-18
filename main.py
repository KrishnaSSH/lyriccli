import time

from rich.console import Console

from core.api import fetch_lyrics
from core.cmus_info import cmus_current_position, cmus_current_song
from core.formatter import format_timestamp

console = Console(color_system="truecolor")


song = cmus_current_song()
if not song:
    console.print("[bold red]No song currently playing!")
    exit()

lyrics = fetch_lyrics(song)
plain_lyrics = lyrics["plainLyrics"]
synced_lyrics = lyrics["syncedLyrics"]
lyrics_tuples = []
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
                continue

last_line = None
while True:
    try:
        position = cmus_current_position()
        current_line = ""
        for t, lyric in lyrics_tuples:
            if position >= t:
                current_line = lyric
            else:
                break

        if current_line != last_line:
            ts_formatted = format_timestamp(position)
            console.print(
                f"[bold yellow]{ts_formatted} [bold white]{current_line}", end="\r"
            )
            last_line = current_line
        time.sleep(1)
    except KeyboardInterrupt:
        console.print("\n[bold yellow] bye")
        exit()
