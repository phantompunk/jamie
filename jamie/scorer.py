import json

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
    try:
        return str(json.loads(res))
    except ValueError:
        return re.sub(r"<(score|\/score)>", "", json.loads(res))


def score_quotes(filename: str):
    if ".json" not in filename:
        filename += ".json"

    with open(os.path.join("./transcripts", filename), "r+") as file:
        quotes = json.load(file)

    for quote in tqdm(quotes, desc="Scoring quotes"):
        response = ollama.generate(
            model="edit", prompt=json.dumps(quote["quote"]), stream=False
        )
        score = extract_quote(response.get("response"))
        quote.update(selected=score)

    with open(os.path.join("./scored", filename), "w") as output:
        json.dump(quotes, output, indent=4)
    return quotes
