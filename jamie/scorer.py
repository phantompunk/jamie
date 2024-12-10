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
    res = res.strip('"')
    # print(f"Quote {res}")
    return res
    # try:
    #     return str(json.loads(res))
    # except ValueError as e:
    #     print(f"Error parsing JSON: {e}")
    #     return re.sub(r"<(score|\/score)>", "", json.loads(res))


def score_quotes(filename: str, model: str="quote"):
    basepath = "./"
    if ".json" not in filename:
        filename += ".json"
        basepath = "./transcripts/"

    with open(os.path.join(basepath, filename), "r+", encoding="utf-8") as file:
        quotes = json.load(file)

    for quote in tqdm(quotes, desc="Scoring quotes"):
        response = ollama.generate(
            model=model, prompt=json.dumps(quote["quote"]), stream=False
        )
        score = extract_quote(response.get("response"))
        if score != "SKIP":
            quote.update(selected=score)

    with open(os.path.join(basepath, filename), "w") as output:
        json.dump(quotes, output, indent=4)
    # print(json.dumps(quotes, indent=4))
    return quotes
