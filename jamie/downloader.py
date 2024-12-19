import os
from typing import Optional
import yt_dlp

EXTENSION_DEFAULT = "mp3"
EXTENSION_MP3 = "mp3/bestaudio/best"
FILENAME_TEMPLATE = "./audio/%(title)s.%(ext)s"


def extension(format: str):
    if format.lower() in [".mp3", "mp3"]:
        return EXTENSION_MP3
    return EXTENSION_MP3


def download_audio(
    url: str,
    output: Optional[str] = FILENAME_TEMPLATE,
    format: str = EXTENSION_DEFAULT,
):
    # templ = os.path.join(output_dir, "%(title)s.%(ext)s")
    # if filename:
    #     templ = os.path.join(output_dir, f"{filename}.%(ext)s")

    ydl_opts = {
        "format": extension(format),
        "outtmpl": output,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
            }
        ],
    }

    ydl_opts["cookiefile"] = "cookies.txt"

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        _ = ydl.download(url)
