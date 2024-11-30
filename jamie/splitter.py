import os
import subprocess
from pathlib import Path
from jamie.logger import logger

DURATION_5_MIN = "300"


def split_audio(filename, duration: str = DURATION_5_MIN):
    basename = Path(os.path.basename(filename)).stem
    command = [
        "ffmpeg",
        "-i",
        filename,
        "-f",
        "segment",
        "-segment_time",
        duration,
        "-c",
        "copy",
        os.path.join("./splits/", basename) + "-%03d.mp3",
    ]

    subprocess.run(command, check=True)
