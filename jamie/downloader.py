import os
import yt_dlp


def download_audio(urls: list[str], filename: str, output_dir: str = "./audio"):
    if not output_dir:
        print("No output")
    # cookies = browser_cookie3.brave(domain_name='youtube.com')
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
    # with open('cookies.txt', 'w') as f:
    #     for cookie in cookies:
    #         f.write(f'{cookie.domain}\tTRUE\t{cookie.path}\t{cookie.secure}\t'
    #                 f'{cookie.expires}\t{cookie.name}\t{cookie.value}\n')
    #
    # Add cookie file to yt-dlp options
    ydl_opts["cookiefile"] = "cookies.txt"
    # if cookiefile:
    #     ydl_opts.update(cookiefile=cookiefile)

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        _ = ydl.download(urls)
