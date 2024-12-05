import os
import yt_dlp


def download_audio(urls: list[str], filename: str, output_dir: str = "./audio"):
    if not output_dir:
        print("No output")

    ydl_opts = {
        "format": "mp3/bestaudio/best",
        "outtmpl": os.path.join(output_dir, f"{filename}.%(ext)s"),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
            }
        ],
    }

    ydl_opts["cookiefile"] = "cookies.txt"

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        _ = ydl.download(urls)
