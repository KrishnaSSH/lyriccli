from dataclasses import dataclass


@dataclass(frozen=True)
class Song:
    file_name: str | None
    title: str | None
    album_name: str | None
    artist: str | None
    album_artist: str | None
    genre: str | None
    song_duration: int | None
