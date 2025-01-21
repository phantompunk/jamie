from pathlib import Path
from typing import Optional

import ollama
import re
from tqdm import tqdm

from jamie.filer import read_json_quotes, write_json_quotes
from jamie.model import Quote

DESC_RANK = "Ranking quotes"
DESC_SCORE = "Scoring quotes"
DESC_PROCESS = "Processing quotes"


def extract_score(res: str):
    try:
        return int(res)
    except ValueError:
        return re.sub(r"<(score|\/score)>", "", res)


def extract_quote(res: str):
    res = res.strip('"')
    return res


def extract_best_quote(quote: Quote, model: str = "quote"):
    if len(quote.quote) <= 20:
        return quote

    if quote.score <= 7:
        return quote

    response = ollama.generate(model=model, prompt=quote.quote, stream=False)
    select = extract_quote(response.get("response"))
    if select != "SKIP":
        quote = quote.update(selected=select)
    return quote


def rank_quote(quote: Quote, model: str = "rank"):
    passage = quote.quote
    if quote.selected:
        passage = quote.selected

    if len(passage) <= 20:
        return quote

    response = ollama.generate(model=model, prompt=passage, stream=False)
    score = extract_score(response.get("response"))
    if score != "SKIP":
        quote = quote.update(score=score)
    return quote


def prepare_filename(filename, model):
    file = Path(filename)
    if model == "quote":
        model_suffix = "-selected"
    elif model == "rank":
        model_suffix = "-ranked"
    else:
        model_suffix = "-processed"
    return f"{file.stem}{model_suffix}{file.suffix}"


def process_quotes(quote, model):
    if model == "quote":
        return extract_best_quote(quote)
    elif model == "rank":
        return rank_quote(quote)
    else:
        return rank_quote(extract_best_quote(quote))


def filter_quotes(quotes):
    return Quote.filter_by_length(quotes)


def score_quotes(filename: str, model: Optional[str]):
    scored_filename = prepare_filename(filename, model)
    desc = DESC_PROCESS

    quotes = read_json_quotes(filename)
    quotes = filter_quotes(quotes)
    processed = [process_quotes(quote, model) for quote in tqdm(quotes, desc=desc)]

    write_json_quotes(scored_filename, processed)
