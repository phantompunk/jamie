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
    """Downloads audio from a YouTube video URL and returns the filename and length in seconds."""
    return download_audio(url, output, format)


def download_audio_with_filename(
    url: str,
    output: Optional[str],
    format: Optional[str],
):
    """Downloads audio from a YouTube video URL and returns the filename."""
    return download_audio(url, output, format)[0]


def create_ydl_options(output: str, format: str, loglevel: str = "ERROR"):
    return {
        "format": get_audio_format(format),
        "cookiefile": "cookies.txt",
        "restrictfilenames": True,
        "noplaylists": True,
        "outtmpl": output,
        "verbose": True,
        "loglevel": loglevel,
        "postprocessors": [
            {  # Extract audio using ffmpeg
                "key": "FFmpegExtractAudio",
                "preferredcodec": format,
            }
        ],
    }


def download_audio(
    url: str,
    output: Optional[str],
    format: Optional[str],
):
    """Downloads audio from a YouTube video URL and returns the filename."""

    # TODO validate name output does not contain an extension
    if not output:
        output = FILENAME_TEMPLATE

    # TODO validate format is supported
    if not format:
        format = "mp3"

    format = format.replace(".", "").lower()
    ydl_opts = create_ydl_options(output, format)

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # If output is the default template then get filename info
        info_dict = ydl.extract_info(url, download=False)
        info = ydl.sanitize_info(info_dict)
        filename = ydl.prepare_filename(info)
        if ".mp3" not in filename or ".m4a" not in filename:
            filename = f"{filename}.{format}"
        ydl.download([url])

        length: float = 0.0
        if info and type(info) is dict:
            length = info.get("duration", None)
        return filename, length
