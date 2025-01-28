import os
import re
from typing import Optional
import yt_dlp

from jamie.logger import logger


EXTENSION_MP3 = "mp3/bestaudio/best"
EXTENSION_M4A = "m4a/bestaudio/best"
FILENAME_TEMPLATE = "%(title)s/%(title)s.%(ext)s"


def is_valid_url(url):
    youtube_regex = r"^(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/)(?:(?:watch\?v=|embed\/)([A-Za-z0-9_-]{11})|(?:user\/[A-Za-z0-9_-]+)|(?:playlist\?list=)([A-Za-z0-9_-]{34})|(?:channel\/)([A-Za-z0-9_-]+))"
    pattern = re.compile(youtube_regex)
    match = pattern.match(url)
    return bool(match)


def is_supported_format(format: str):
    supported = ["mp3", "m4a", "wav"]
    format = format.lower().lstrip(".")
    return format in supported


def get_audio_format(format: str):
    ext = {
        "mp3": "mp3/bestaudio/best",
        "m4a": "m4a/bestaudio/best",
        "wav": "wav/bestaudio/best",
    }
    return ext.get(format.lower().lstrip("."))


def create_ydl_options(output: str, format: str, loglevel: str = "INFO"):
    if output != FILENAME_TEMPLATE:
        output = output.split(".")[0]

    return {
        "format": get_audio_format(format),
        "cookiefile": "cookies.txt",
        "restrictfilenames": True,
        "noplaylists": True,
        "outtmpl": output,
        "verbose": True,
        "loglevel": loglevel,
        "logger": logger,
        "postprocessors": [
            {  # Extract audio using ffmpeg
                "key": "FFmpegExtractAudio",
                "preferredcodec": format,
            }
        ],
    }


def get_video_name(filename, format, url, ydl) -> str:
    if filename == FILENAME_TEMPLATE:
        try:
            info_dict = ydl.extract_info(url, download=False)
            info = ydl.sanitize_info(info_dict)
            filename = ydl.prepare_filename(info).split(".")[0]
            return f"{filename or 'unknown'}.{format}"
        except Exception:
            return f"unknown.{format}"
    return f"{filename}.{format}"


def download_audio(
    video_url: str,
    output: Optional[str],
    format: Optional[str],
):
    """Downloads audio from a YouTube video URL and returns the filename."""

    if not is_valid_url(video_url):
        raise ValueError(f"Invalid Youtube URL: {video_url}")

    if not output:
        filename = FILENAME_TEMPLATE
    else:
        name = output.split(".")[0]
        filename = os.path.join(name, name)

    if not format or not is_supported_format(format):
        logger.info(f"Unsupported format: {format} using default 'mp3'")
        format = "mp3"

    ydl_opts = create_ydl_options(filename, format)

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        filename = get_video_name(filename, format, video_url, ydl)
        ydl.download([video_url])
        return filename
