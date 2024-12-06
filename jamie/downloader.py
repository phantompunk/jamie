import os
import yt_dlp


def download_audio(urls: list[str], filename: str, output_dir: str = "./audio"):
    if not output_dir:
        print("No output")

    templ = os.path.join(output_dir, "%(title)s.%(ext)s")
    if filename:
        templ = os.path.join(output_dir, f"{filename}.%(ext)s")

    ydl_opts = {
        "format": "mp3/bestaudio/best",
        "outtmpl": templ, 
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
