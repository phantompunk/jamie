from collections import defaultdict
from functools import partial, reduce
import json
import os
from glob import glob
from pathlib import Path
from typing import Dict, List, Optional

from jamie.model import Quote 


def read_json_quotes(filepath: str) -> List[Quote]:
    with open(filepath, "r", encoding="utf-8") as infile:
        data = json.load(infile)

    return list(map(Quote.from_dict, data))


def write_json_quotes(filepath, quotes: List[Quote]):
    with open(filepath, "w", encoding="utf-8") as outfile:
        outfile.write(Quote.serialize_list(quotes))


def merge_runoff(transcriptions: List[Quote]) -> List[Quote]:
    if not transcriptions:
        return []

    def combine(items: List[Quote], current: Quote):
        if items and items[-1].speaker == current.speaker:
            items[-1].quote += " " + current.quote
        else:
            items.append(current)
        return items

    return reduce(combine, transcriptions, [])


def merge(filepath: str):
    quotes = read_json_quotes(filepath)
    quotes = merge_runoff(quotes)
    write_json_quotes(filepath, quotes)


def combine_quotes(pattern: str, output_dir: str = "./"):
    if "*" not in pattern:
        pattern += "*"

    combined = []
    files = glob(pattern)
    files.sort()
    for filename in files:
        basename = Path(os.path.basename(filename)).stem
        with open(filename, "r") as infile:
            data = json.load(infile)
            combined.extend(data)

    basename = Path(os.path.basename(pattern)).stem
    basename = basename.replace("*", "") + ".json"
    with open(os.path.join(output_dir, basename), "w") as output:
        json.dump(combined, output, indent=4)


def combine(quotes: List[Quote], pattern: str, output_dir: str = "./"):
    if "*" not in pattern:
        pattern += "*"

    combined = []
    files = glob(pattern)
    files.sort()
    for filename in files:
        basename = Path(os.path.basename(filename)).stem
        with open(filename, "r") as infile:
            data = json.load(infile)
            combined.extend(data)

    basename = Path(os.path.basename(pattern)).stem
    basename = basename.replace("*", "") + ".json"
    with open(os.path.join(output_dir, basename), "w") as output:
        json.dump(combined, output, indent=4)


def enhance_quotes(
    filename: str,
    link: Optional[str] = None,
    episode: Optional[str] = None,
    speaker0: Optional[str] = None,
    speaker1: Optional[str] = None,
    speaker2: Optional[str] = None,
):
    quotes = read_json_quotes(filename)
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
            if speaker == "SPEAKER_00" and speaker0:
                # print(f'Replacing {speaker} with {speaker0}')
                quote.update(episode=episode, link=link, speaker=speaker0)
            elif speaker == "SPEAKER_01" and speaker1:
                # print(f'Replacing {speaker} with {speaker1}')
                quote.update(episode=episode, link=link, speaker=speaker1)
            elif speaker == "SPEAKER_02" and speaker2:
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


def update_quotes(
    quotes: List[Quote],
    speakers: Dict,
    link: Optional[str],
    episode: Optional[str],
):
    speaker_update = partial(
        Quote.update_speaker, speaker_map=speakers, episode=episode, link=link
    )
    return list(map(speaker_update, quotes))


def create_speakers_map(x: Optional[str], y: Optional[str], z: Optional[str]):
    return {
        "SPEAKER_00": x or "SPEAKER_00",
        "SPEAKER_01": y or "SPEAKER_01",
        "SPEAKER_02": z or "SPEAKER_02",
    }


def enhance(
    filename: str,
    link: Optional[str] = None,
    episode: Optional[str] = None,
    speaker0: Optional[str] = None,
    speaker1: Optional[str] = None,
    speaker2: Optional[str] = None,
):
    quotes = read_json_quotes(filename)
    speakers_map = create_speakers_map(speaker0, speaker1, speaker2)
    quotes = update_quotes(quotes, speakers_map, link, episode)
    write_json_quotes(filename, quotes)
