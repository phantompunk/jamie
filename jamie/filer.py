import json
import os
from glob import glob
from pathlib import Path
from datetime import datetime

from jamie.model import Quote


def combine_quotes(pattern: str, output_dir: str = "./transcripts"):
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


def enhance_quotes(filename: str, episode: str = "", link: str = ""):
    if ".json" not in filename:
        filename += ".json"

    with open(os.path.join("./transcripts", filename), "r+") as file:
        quotes = json.load(file)
        for quote in quotes:
            quote.update(episode=episode, link=link, created=datetime.now().isoformat())

        file.seek(0)
        json.dump(quotes, file, indent=4)
        # Truncate the file to remove any extra data
        file.truncate()
