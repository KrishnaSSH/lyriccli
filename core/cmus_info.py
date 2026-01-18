import subprocess

from rich.console import Console

from core.models import Song

console = Console(color_system="truecolor")


def parse_cmus(lines: list[str]) -> dict:
    song_data = {}
    for line in lines:
        if line.startswith("file "):
            song_data["file_name"] = line[len("file ") :]
        elif line.startswith("tag title "):
            song_data["title"] = line[len("tag title ") :]
        elif line.startswith("duration "):
            song_data["song_duration"] = int(line[len("duration ") :])
        elif line.startswith("tag artist "):
            song_data["artist"] = line[len("tag artist ") :]
        elif line.startswith("tag albumartist "):
            song_data["album_artist"] = line[len("tag albumartist ") :]
        elif line.startswith("tag album "):
            song_data["album_name"] = line[len("tag album ") :]
        elif line.startswith("tag genre "):
            song_data["genre"] = line[len("tag genre ") :]

    return song_data


def cmus_current_song() -> Song | None:
    cmus_command = ["cmus-remote", "-Q"]
    try:
        output = subprocess.run(cmus_command, capture_output=True, text=True)
        if output.returncode != 0:
            console.print("[red bold]Error", output.stderr)
            return None
        else:
            metadata = output.stdout
            lines = metadata.splitlines()

            song_data = parse_cmus(lines)

            return Song(
                file_name=song_data.get("file_name"),
                title=song_data.get("title"),
                artist=song_data.get("artist"),
                album_artist=song_data.get("album_artist"),
                album_name=song_data.get("album_name"),
                genre=song_data.get("genre"),
                song_duration=song_data.get("song_duration"),
            )

    except FileNotFoundError:
        console.print(
            "[red bold]Alert! [white bold]cmus isn't installed in your system install it from [blue underline]https://cmus.github.io/#download"
        )


def cmus_current_position() -> int | None:
    cmus_command = ["cmus-remote", "-Q"]
    try:
        output = subprocess.run(cmus_command, capture_output=True, text=True)
        if output.returncode == 0:
            metadata = output.stdout
            lines = metadata.splitlines()
            for line in lines:
                if line.startswith("position"):
                    position = int(line[len("position ") :])
                    return position
        else:
            console.print("[red bold]Error", output.stderr)
            return None

    except FileNotFoundError:
        console.print(
            "[red bold]Alert! [white bold]cmus isn't installed in your system install it from [blue underline]https://cmus.github.io/#download"
        )
