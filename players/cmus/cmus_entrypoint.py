import time
import sys
from core.ui import (
    ui_bye_handler,
    ui_no_lyrics_render,
    ui_console,
    ui_now_playing_render,
    ui_plain_lyrics_render,
    ui_retry_handler,
    ui_scraping_render,
)
from core.api import fetch_lyrics
from datetime import timedelta
from players.cmus.cmus_handlers import (
    closed_cmus_handler,
    not_installed_cmus_handler,
    not_playing_cmus_handler,
)
from players.cmus.cmus_info import (
    cmus_current_position,
    cmus_current_song,
    cmus_query,
)
from players.cmus.formatter import format_timestamp

from players.cmus.parser import parse_synced_lyrics


"""
entrypoint

"""


def cmus_entrypoint():
    last_song_id = None
    last_line = None
    lyrics_tuples: list[tuple[float, str]] = []

    while True:
        try:
            metadata = cmus_query()
            if not metadata:
                closed_cmus_handler()
                ui_retry_handler()
                continue
        except FileNotFoundError:
            not_installed_cmus_handler()
            sys.exit(1)

        try:
            song = cmus_current_song(metadata)
            position = cmus_current_position(metadata)

            if not song or not song.title:
                not_playing_cmus_handler()
                continue

            song_id = (song.artist, song.title)

            if song_id != last_song_id:
                ui_console.clear()
                lyrics_tuples.clear()
                last_line = None
                last_song_id = song_id

                if song.song_duration:
                    duration = str(timedelta(seconds=song.song_duration))
                    ui_now_playing_render(
                        song.title,
                        song.artist,
                        song.album_artist,
                        song.genre,
                        duration,
                    )
                else:
                    not_playing_cmus_handler()
                    continue

                with ui_scraping_render():
                    lyrics = fetch_lyrics(song)

                synced = lyrics.get("syncedLyrics")
                plain = lyrics.get("plainLyrics")

                if synced:
                    lyrics_tuples = parse_synced_lyrics(
                        synced_lyrics=synced,
                        lyrics_tuples=[],
                    )
                elif plain:
                    ui_plain_lyrics_render(plain)
                else:
                    ui_no_lyrics_render()

            if position is None:
                time.sleep(0.3)
                continue

            current_line = ""
            for t, lyric in lyrics_tuples:
                if position >= t:
                    current_line = lyric
                else:
                    break

            if current_line and current_line != last_line:
                ui_console.print(
                    f"[bold yellow]{format_timestamp(position)} "
                    f"[bold white]{current_line}"
                )
                last_line = current_line

            time.sleep(0.2)

        except KeyboardInterrupt:
            ui_bye_handler()
            sys.exit(0)
