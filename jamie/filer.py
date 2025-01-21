from functools import partial, reduce
import json
import os
from glob import glob
from pathlib import Path
from typing import Dict, List, Optional

from jamie.model import Quote


def read_json_quotes(filepath: str) -> List[Quote]:
    """
    Reads a list of JSON quotes from a file and returns them as a list of Quote objects.

    Args:
        filepath (str): The path to the file containing the JSON data.

    Returns:
        List[Quote]: A list of Quote objects parsed from the JSON data.
    """
    with open(filepath, "r", encoding="utf-8") as infile:
        data = json.load(infile)

    return list(map(Quote.from_dict, data))


def write_json_quotes(filepath: str, quotes: List[Quote]) -> None:
    """
    Writes a list of Quote objects to a JSON file.

    Args:
        filepath (str): The path to the file where the data will be written.
        quotes (List[Quote]): A list of Quote objects to be serialized and written.

    Returns:
        None
    """
    with open(filepath, "w", encoding="utf-8") as outfile:
        outfile.write(Quote.serialize_list(quotes))


def merge_runoff(transcriptions: List[Quote]) -> List[Quote]:
    """
    Merges a list of Quote objects into a single combined object.

    Args:
        transcriptions (List[Quote]): A list of Quote objects to be merged.

    Returns:
        List[Quote]: The merged list of Quote objects.
    """

    if not transcriptions:
        return []

    return reduce(Quote.combine, transcriptions, [])


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
    speakers_map = create_speakers_map(speaker0, speaker1, speaker2)
    quotes = read_json_quotes(filename)
    quotes = update_quotes(quotes, speakers_map, link, episode)
    write_json_quotes(filename, quotes)
