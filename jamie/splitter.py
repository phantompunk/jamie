import subprocess
from pathlib import Path

SPLITNAME_TEMPLATE = "-%03d"
DURATION_5_MIN = "300"


def split_audio(
    filename: str,
    output: str = SPLITNAME_TEMPLATE,
    output_dir: str = "./audio/splits",
    duration: str = DURATION_5_MIN,
    extension: str = ".mp3",
):
    """
    Split an audio file into segments of a given duration using FFMPEG
    """

    # TODO Validate duration input
    # Check existence of file
    path = Path(filename)
    if not path.exists():
        raise FileNotFoundError(f"File '{filename}' not found.")

    if not path.is_file():
        raise IsADirectoryError(f"File '{filename}' is not a file.")

    # TODO Define output location

    command = [
        "ffmpeg",
        "-i",
        path.as_posix(),
        "-f",
        "segment",
        "-segment_time",
        duration,
        "-c",
        "copy",
        f"{path.stem}{SPLITNAME_TEMPLATE}{extension}",
    ]

    subprocess.run(command, check=True)
