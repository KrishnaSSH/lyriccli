# it formats seconds into MM:SS:XX
def format_timestamp(seconds):
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    hundredths = int((seconds - int(seconds)) * 100)
    return f"[{minutes:02d}:{secs:02d}.{hundredths:02d}]"
