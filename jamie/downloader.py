import os
import yt_dlp


def download_audio(urls: list[str], output: str, output_dir: str = "./audio"):
    ydl_opts = {
        "format": "mp3/bestaudio/best",
        "outtmpl": os.path.join(output_dir, f"{output}.%(ext)s"),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
            }
        ],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(urls)
