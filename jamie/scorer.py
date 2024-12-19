import json
from pathlib import Path

import ollama
import os
import re
from tqdm import tqdm


def extract_score(res: str):
    try:
        return int(res)
    except ValueError:
        return re.sub(r"<(score|\/score)>", "", res)


def extract_quote(res: str):
    res = res.strip('"')
    # print(f"Quote {res}")
    return res
    # try:
    #     return str(json.loads(res))
    # except ValueError as e:
    #     print(f"Error parsing JSON: {e}")
    #     return re.sub(r"<(score|\/score)>", "", json.loads(res))


def extract_best_quote(quote: dict, model: str = "quote"):
    response = ollama.generate(
        model=model, prompt=json.dumps(quote["quote"]), stream=False
    )
    score = extract_quote(response.get("response"))
    if score != "SKIP":
        quote.update(selected=score)
    return quote

def rank_quote(quote: dict, model: str = "rank"):
    if not quote.get("selected",""):
        return quote

    response = ollama.generate(
        model=model, prompt=json.dumps(quote["selected"]), stream=False
    )
    score = extract_score(response.get("response"))
    if score != "SKIP":
        quote.update(score=score)
    return quote


def score_quotes(filename: str, model: str = "quote"):
    file = Path(filename)
    if not file.exists():
        raise FileNotFoundError(f"File '{filename}' not found.")

    if not file.is_file():
        raise IsADirectoryError(f"File '{filename}' is not a file.")

    suffix = "-score" if model=="quote" else "-ranked"
    new_filename = file.stem + suffix + file.suffix

    # basepath = "./"
    # if ".json" not in filename:
    #     filename += ".json"
    #     basepath = "./transcripts/"

    with open(filename, "r+", encoding="utf-8") as file:
        quotes = json.load(file)

    for quote in tqdm(quotes, desc="Scoring quotes"):
        if model == "quote":
            quote = extract_best_quote(quote)
        if model == "rank":
            quote = rank_quote(quote)
            # quote.update(selected=extract_quote(quote["quote"]))
        # if model == "rank":
        #     quote = rank_quote(quote.get("selected", ""))
        # quote.update(score=rank_quote(quote["selected"]))
        # response = ollama.generate(
        #     model=model, prompt=json.dumps(quote["quote"]), stream=False
        # )
        # score = extract_quote(response.get("response"))
        # if score != "SKIP":
        #     quote.update(selected=score)

    with open(new_filename, "w") as output:
        json.dump(quotes, output, indent=4)
    # print(json.dumps(quotes, indent=4))
    return quotes
