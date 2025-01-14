import json
import os
from glob import glob
from pathlib import Path
from typing import Optional


def combine_quotes(pattern: str, output_dir: str = "./"):
    if "*" not in pattern:
        pattern += "*"

    combined = []
    files = glob(pattern)
    files.sort()
    for filename in files:
        basename = Path(os.path.basename(filename)).stem
        print("found", basename)
        with open(filename, "r") as infile:
            data = json.load(infile)
            combined.extend(data)

    basename = Path(os.path.basename(pattern)).stem
    basename = basename.replace("*", "") + ".json"
    with open(os.path.join(output_dir, basename), "w") as output:
        json.dump(combined, output, indent=4)


def enhance_quotes(
    filename: str,
    link: Optional[str]=None,
    episode: Optional[str]=None,
    speaker0: Optional[str] = None,
    speaker1: Optional[str] = None,
    speaker2: Optional[str]=None,
):
    try:
        with open(filename, "r+", encoding="utf-8") as infile:
            quotes = json.load(infile)

        first = quotes[0]
        if not link:
            link = first.get("link", "")
        if not episode:
            episode = first.get("episode", "")

        for quote in quotes:
            speaker = quote.get("speaker")
            if speaker=="SPEAKER_00" and speaker0:
                # print(f'Replacing {speaker} with {speaker0}')
                quote.update(episode=episode, link=link, speaker=speaker0) 
            elif speaker=="SPEAKER_01" and speaker1:
                # print(f'Replacing {speaker} with {speaker1}')
                quote.update(episode=episode, link=link, speaker=speaker1) 
            elif speaker=="SPEAKER_02" and speaker2:
                # print(f'Replacing {speaker} with {speaker2}')
                quote.update(episode=episode, link=link, speaker=speaker2) 
            else:
                # print(f'EP:{episode}, LINK:{link}')
                quote.update(episode=episode, link=link) 

        with open(filename, "w") as outfile:
            json.dump(quotes, outfile, indent=4)

    except FileNotFoundError:
        raise
    except json.JSONDecodeError:
        raise

    # if ".json" not in filename:
    #     filename += ".json"
    #
    # with open(os.path.join("./", filename), "w+") as file:
    #     quotes = json.load(file)
    #
    #     file.seek(0)
    #     json.dump(quotes, file, indent=4)
    #     # Truncate the file to remove any extra data
    #     file.truncate()
