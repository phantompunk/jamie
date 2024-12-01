import os
import subprocess
from pathlib import Path
from jamie.logger import logger


DURATION_5_MIN = "300"


def split_audio(
    filename,
    output_dir: str = "./audio",
    duration: str = DURATION_5_MIN,
    extension: str = ".mp3",
):
    basename = Path(os.path.basename(filename)).stem
    # filename += ".mp3"
    command = [
        "ffmpeg",
        "-i",
        os.path.join(output_dir, filename+extension),
        "-f",
        "segment",
        "-segment_time",
        duration,
        "-c",
        "copy",
        os.path.join("./splits/", basename) + "-%03d.mp3",
    ]

    subprocess.run(command, check=True)
