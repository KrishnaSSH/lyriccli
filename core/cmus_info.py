import subprocess

from rich.console import Console

from core.models import Song

console = Console(color_system="truecolor")


def cmus_query() -> str | None:
    cmus_command = ["cmus-remote", "-Q"]
    output = subprocess.run(cmus_command, capture_output=True, text=True)
    if output.returncode == 0:
        metadata = output.stdout
        return metadata
    else:
        return None


def parse_cmus(lines: list[str]) -> dict:
    prefixes = {
        "file ": ("file_name", str),
        "tag title ": ("title", str),
        "duration ": ("song_duration", int),
        "tag artist ": ("artist", str),
        "tag albumartist ": ("album_artist", str),
        "tag album ": ("album_name", str),
        "tag genre ": ("genre", str),
    }
    song_data = {}
    for line in lines:
        for prefix, (key, cast) in prefixes.items():
            if line.startswith(prefix):
                song_data[key] = cast(line.removeprefix(prefix))
                break
    return song_data


def cmus_current_song(metadata: str | None) -> Song | None:
    if not metadata:
        return None
    song_data = parse_cmus(metadata.splitlines())
    return Song(
        file_name=song_data.get("file_name"),
        title=song_data.get("title"),
        artist=song_data.get("artist"),
        album_artist=song_data.get("album_artist"),
        album_name=song_data.get("album_name"),
        genre=song_data.get("genre"),
        song_duration=song_data.get("song_duration"),
    )


def cmus_current_position(metadata: str | None) -> int | None:
    if not metadata:
        return None
    for line in metadata.splitlines():
        if line.startswith("position"):
            position = int(line.removeprefix("position "))
            return position
