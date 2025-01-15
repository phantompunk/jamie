from dataclasses import dataclass, replace
import json
from datetime import datetime
import hashlib
from typing import Dict, Optional


@dataclass
class Quote:
    def __init__(
        self,
        quote: str,
        speaker: str,
        id: str,
        created: str,
        episode: str = "",
        link: str = "",
        start: int = 0,
    ):
        self.quote = quote
        self.speaker = speaker
        self.episode = episode
        self.link = link
        self.id = id if id else hashlib.md5(quote.encode()).hexdigest()[:6]
        self.created = created if created else datetime.now().isoformat()
        self.start = start

    def update(self, speakers: dict, **kwargs):
        speaker = speakers.get(self.speaker)
        return replace(self, speaker=speaker, **kwargs)

    def to_dict(self):
        return {
            "quote": self.quote,
            "speaker": self.speaker,
            "episode": self.episode,
            "link": self.link,
            "id": self.id,
            "start": self.start,
            "created": self.created,
        }

    @classmethod
    def from_dict(cls, item: Dict) -> "Quote":
        return cls(
            quote=item["quote"],
            speaker=item["speaker"],
            episode=item["episode"],
            link=item["link"],
            id=item["id"],
            created=item["created"],
        )

    @staticmethod
    def serialize_list(quotes: list["Quote"]) -> str:
        return json.dumps([quote.to_dict() for quote in quotes], indent=4)

    @staticmethod
    def update_speaker(
        quote: "Quote",
        speaker_map: dict,
        episode: Optional[str],
        link: Optional[str],
    ) -> "Quote":
        speaker = speaker_map.get(quote.speaker)
        data = quote.__dict__.copy()
        data.update(speaker=speaker)
        if episode:
            data.update(episode=episode)
        if link:
            data.update(link=link)
        return Quote(**data)


def parse_quote(item: dict) -> Quote:
    return Quote(
        quote=item["quote"],
        speaker=item["speaker"],
        episode=item["episode"],
        link=item["link"],
        id=item["id"],
        created=item["created"],
    )
