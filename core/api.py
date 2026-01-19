import requests

from core.models import Song


def fetch_lyrics(song: Song) -> dict:
    url = "https://lrclib.net/api/get?"

    parameters = {
        "artist_name": song.artist,
        "track_name": song.title,
        "album_name": song.album_name,
        "duration": song.song_duration,
    }

    try:
        response = requests.get(url, params=parameters)
        response.raise_for_status()
        lyrics_data = response.json()
        return {
            "plainLyrics": lyrics_data.get("plainLyrics"),
            "syncedLyrics": lyrics_data.get("syncedLyrics"),
        }
    except requests.RequestException as err:
        return {"plainLyrics": f"Error: {err}", "syncedLyrics": f"Error: {err}"}
