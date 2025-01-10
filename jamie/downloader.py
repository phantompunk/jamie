from typing import Optional
import yt_dlp

EXTENSION_MP3 = "mp3/bestaudio/best"
EXTENSION_M4A = "m4a/bestaudio/best"
FILENAME_TEMPLATE = "%(title)s.%(ext)s"


def get_audio_format(format: str):
    ext = {
        "mp3": "mp3/bestaudio/best",
        "m4a": "m4a/bestaudio/best",
    }
    return ext.get(format)


def yt_dlp_monitor(d):
    return d.get("info_dict").get("_filename")


def download_audio_with_duration(
    url: str,
    output: Optional[str],
    format: Optional[str],
):
    """Downloads audio from a YouTube video URL and returns the filename and duration in seconds."""
    return download_audio(url, output, format, True)


def download_audio(
    url: str,
    output: Optional[str],
    format: Optional[str],
    return_duration: bool = False,
):
    """Downloads audio from a YouTube video URL and returns the filename."""

    # TODO validate output does not contain an extension
    if not output:
        output = FILENAME_TEMPLATE

    # TODO validate format
    if not format:
        format = "mp3"

    format = format.replace(".", "").lower()
    ydl_opts = {
        "format": get_audio_format(format),
        "cookiefile": "cookies.txt",
        "restrictfilenames": True,
        "noplaylists": True,
        "outtmpl": output,
        "verbose": True,
        "postprocessors": [
            {  # Extract audio using ffmpeg
                "key": "FFmpegExtractAudio",
                "preferredcodec": format,
            }
        ],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        info = ydl.sanitize_info(info_dict)
        filename = ydl.prepare_filename(info)
        ydl.download([url])
        if return_duration and info_dict:
            duration: int = info_dict.get("duration", None)
            return filename, duration
        return filename
