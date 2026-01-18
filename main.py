from rich.console import Console

from core.api import fetch_lyrics
from core.cmus_info import cmus_current_song

console = Console(color_system="truecolor")

song = cmus_current_song()
if song:
    lyrics = fetch_lyrics(song)
    console.print(f"[bold blue]Plain Lyrics:\n [bold white]{lyrics['plainLyrics']}")
    console.print(f"[bold green]Synced Lyrics:\n [bold white]{lyrics['syncedLyrics']}")
