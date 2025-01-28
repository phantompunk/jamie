import os
import subprocess
from pathlib import Path
from mutagen.mp3 import MP3
from mutagen.m4a import M4A
from mutagen.wave import WAVE


SPLITNAME_TEMPLATE = "-%03d"
DEFAULT_DURATION_SECONDS = 300


def check_ffmpeg_installation():
    """
    Checks if FFMPEG is installed and accessible.

    Raises:
      RuntimeError: If FFMPEG is not found or encountered an error.
    """
    try:
        subprocess.run(
            ["ffmpeg", "-version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
    except FileNotFoundError:
        raise RuntimeError("FFMPEG is not installed or not in your system's PATH.")
    except subprocess.CalledProcessError:
        raise RuntimeError("FFMPEG encountered an error during version check.")


def get_audio_length(path: Path) -> int:
    if path.suffix == ".mp3":
        audio = MP3(path.as_posix())
    elif path.suffix == ".m4a":
        audio = M4A(path.as_posix())
    elif path.suffix == ".wav":
        audio = WAVE(path.as_posix())
    else:
        raise ValueError("Unsupported file format. Only mp3 and m4a are supported.")
    return int(audio.info.length) if audio.info else 0


def split_audio(
    filename: str,
    duration: int = DEFAULT_DURATION_SECONDS,
) -> str:
    """
    Split an audio file into segments of a given duration using FFMPEG
    """

    path = Path(filename)
    if not path.exists():
        raise FileNotFoundError(f"File '{filename}' not found.")

    if not path.is_file():
        raise IsADirectoryError(f"File '{filename}' is not a file.")

    extension = path.suffix
    if extension not in [".mp3", ".m4a", ".wav"]:
        raise ValueError("Unsupported file format. Only mp3 and m4a are supported.")

    check_ffmpeg_installation()

    globname = f"{path.stem}/{path.stem}-*{extension}"
    if not os.path.exists(path.stem):
        os.makedirs(path.stem)

    command = [
        "ffmpeg",
        "-i",
        path.as_posix(),
        "-f",
        "segment",
        "-segment_time",
        str(duration),
        "-c",
        "copy",
        f"./{path.stem}/{path.stem}{SPLITNAME_TEMPLATE}{extension}",
    ]

    try:
        subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
    except subprocess.CalledProcessError as cpe:
        raise RuntimeError(f"FFMPEG command failed: {cpe}") from cpe

    return globname
