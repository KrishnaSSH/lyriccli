import time
import sys
from core.ui import (
    ui_bye_handler,
    ui_no_lyrics_render,
    ui_console,
    ui_now_playing_render,
    ui_plain_lyrics_render,
    ui_retry_handler,
    # migrate later to  ui_scraping_render,
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
    last_line = None
    last_song_id = None
    lyrics_tuples = []
    while True:
        try:
            if cmus_query():
                global metadata
                metadata = cmus_query()
            else:
                closed_cmus_handler()
        except FileNotFoundError:
            not_installed_cmus_handler()
            sys.exit(1)

        try:
            song = cmus_current_song(metadata)
            position = cmus_current_position(metadata)
            if not song:
                time.sleep(2)
                continue
            song_id = (song.artist, song.title)

            song_track(
                song_id=song_id,
                last_song_id=last_song_id,
                lyrics_tuples=lyrics_tuples,
                last_line=last_line,
            )

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
                ui_retry_handler()
                continue

            with ui_console.status("[bold yellow]Scraping"):
                lyrics = fetch_lyrics(song)
                synced_lyrics = lyrics["syncedLyrics"]
                plain_lyrics = lyrics["plainLyrics"]

            if synced_lyrics:
                try:
                    lyrics_tuples = parse_synced_lyrics(
                        synced_lyrics=synced_lyrics, lyrics_tuples=lyrics_tuples
                    )
                except ValueError:
                    pass

            if not synced_lyrics:
                if plain_lyrics:
                    ui_plain_lyrics_render(plain_lyrics)
                else:
                    ui_no_lyrics_render()

            last_song_id = song_id
            position = cmus_current_position(cmus_query())
            current_line = ""
            for t, lyric in lyrics_tuples:
                if position >= t:
                    current_line = lyric
                else:
                    break

            if current_line != last_line:
                ui_console.print(
                    f"[bold yellow]{format_timestamp(position)} [bold white]{current_line}"
                )
        except KeyboardInterrupt:
            ui_bye_handler()
            sys.exit(0)


def song_track(song_id, last_song_id, lyrics_tuples, last_line):
    if song_id != last_song_id:
        ui_console.clear()
        lyrics_tuples.clear()
        last_line = None
    return last_line
