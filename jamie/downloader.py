import os
from typing import Optional
import yt_dlp

EXTENSION_MP3 = "mp3/bestaudio/best"
EXTENSION_M4A = "m4a/bestaudio/best"
FILENAME_TEMPLATE = "%(title)s.%(ext)s"


def extension(format: str):
    ext = {
        "mp3": EXTENSION_MP3,
        "m4a": EXTENSION_M4A,
    }
    return ext.get(format)


def yt_dlp_monitor(d):
    return d.get("info_dict").get("_filename")


def download_audio(
    url: str,
    output: Optional[str] = FILENAME_TEMPLATE,
    format: str = "mp3",
):
    format = format.replace(".", "").lower()
    ydl_opts = {
        "format": extension(format),
        "outtmpl": output,
        "postprocessors": [
            {  # Extract audio using ffmpeg
                "key": "FFmpegExtractAudio",
                "preferredcodec": format,
            }
        ],
    }

    ydl_opts["cookiefile"] = "cookies.txt"

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(url)
