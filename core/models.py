from dataclasses import dataclass


@dataclass
class Song:
    file_name: str
    title: str
    album_name: str
    artist: str
    album_artist: str
    genre: str
    song_duration: int
