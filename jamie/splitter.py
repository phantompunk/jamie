import os
import subprocess
from pathlib import Path
from jamie.logger import logger


DURATION_5_MIN = "300"


def split_audio(
    filename,
    output_dir: str = "./audio/splits",
    duration: str = DURATION_5_MIN,
    extension: str = ".mp3",
):
    if not duration:
        duration = DURATION_5_MIN

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    basename = Path(os.path.basename(filename)).stem
    command = [
        "ffmpeg",
        "-i",
        os.path.join("./audio", filename + extension),
        "-f",
        "segment",
        "-segment_time",
        duration,
        "-c",
        "copy",
        os.path.join(output_dir, basename) + "-%03d.mp3",
    ]

    subprocess.run(command, check=True)
