import subprocess
from pathlib import Path
from typing import List, Optional, Tuple
from mutagen.mp3 import MP3
from mutagen.m4a import M4A


SPLITNAME_TEMPLATE = "-%03d"
DEFAULT_DURATION_SECONDS = 300


def get_audio_length(path: Path) -> int:
    if path.suffix == ".mp3":
        audio = MP3(path.as_posix())
    elif path.suffix == ".m4a":
        audio = M4A(path.as_posix())
    else:
        raise ValueError("Unsupported file format. Only mp3 and m4a are supported.")
    return audio.info.length if audio.info else 0


def split_audio(
    filename: str,
    output: str = SPLITNAME_TEMPLATE,
    output_dir: str = ".",
    duration: Optional[int] = DEFAULT_DURATION_SECONDS,
    length: Optional[float] = None,
) -> Tuple[List[str], int]:
    """
    Split an audio file into segments of a given duration using FFMPEG
    """

    # TODO Validate that FFMPEG is available
    # TODO Validate duration input
    path = Path(filename)
    if not path.exists():
        raise FileNotFoundError(f"File '{filename}' not found.")

    if not path.is_file():
        raise IsADirectoryError(f"File '{filename}' is not a file.")

    extension = path.suffix
    if extension not in [".mp3", ".m4a"]:
        raise ValueError("Unsupported file format. Only mp3 and m4a are supported.")

    if duration is None:
        duration = DEFAULT_DURATION_SECONDS

    if length is None:
        length = get_audio_length(path)

    chunks = int(length // duration) + 1
    names = [f"{output_dir}/{path.stem}-{i:03d}{extension}" for i in range(chunks)]
    globname = f"{output_dir}/{path.stem}-*{extension}" 

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
        f"{output_dir}/{path.stem}{SPLITNAME_TEMPLATE}{extension}",
    ]

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as cpe:
        raise RuntimeError(f"FFMPEG command failed: {cpe}") from cpe

    return names, chunks
