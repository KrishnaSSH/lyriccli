def parse_synced_lyrics(synced_lyrics, lyrics_tuples):
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
    return lyrics_tuples
