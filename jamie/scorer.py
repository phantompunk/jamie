import json

import ollama


def score_quotes(quotes: list[dict]):
    for quote in quotes[0:100]:
        response = ollama.generate(
            model="score", prompt=json.dumps(quote["quote"]), stream=False
        )
        quote.update(score=int(response.get("response", "0")))
        # print(f'Response: {response["response"]}')
    return quotes
