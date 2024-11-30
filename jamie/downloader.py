import os
import yt_dlp
import json


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

    with yt_dlp.YoutubeDL(None) as ydl:
        info = ydl.extract_info(urls[0], download=False)
        # ydl.sanitize_info makes the info json-serializable
        print(json.dumps(ydl.sanitize_info(info)))

    # with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    #     error_code = ydl.download(urls)
