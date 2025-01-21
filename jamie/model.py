from dataclasses import dataclass, field, replace
import json
from datetime import datetime
import hashlib
from typing import Dict, Optional


@dataclass
class Quote:
    id: str = field(default="", init=False)
    start: int
    quote: str
    speaker: str
    link: str = ""
    score: int = 0
    episode: str = ""
    selected: str = ""
    created: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if not self.id:
            self.id = hashlib.md5(self.quote.encode()).hexdigest()[:6]

    def update(self, **changes) -> "Quote":
        return replace(self, **changes)

    def to_dict(self):
        return {
            "quote": self.quote,
            "speaker": self.speaker,
            "episode": self.episode,
            "link": self.link,
            "id": self.id,
            "start": self.start,
            "score": self.score,
            "selected": self.selected,
            "created": self.created.isoformat(),
        }

    @classmethod
    def from_dict(cls, item: Dict) -> "Quote":
        return cls(
            quote=item["quote"],
            speaker=item["speaker"],
            episode=item["episode"],
            link=item["link"],
            start=item["start"],
            score=item.get("score", 0),
            selected=item.get("selected", ""),
            created=datetime.fromisoformat(item.get("created", None)),
        )

    @staticmethod
    def serialize_list(quotes: list["Quote"]) -> str:
        return json.dumps([quote.to_dict() for quote in quotes], indent=4)

    @staticmethod
    def combine(quotes: list["Quote"], current: "Quote") -> list["Quote"]:
        if quotes and quotes[-1].speaker == current.speaker:
            quotes[-1].quote += " " + current.quote
        else:
            quotes.append(current)
        return quotes

    @staticmethod
    def update_speaker(
        item: "Quote", speaker_map: dict, episode: Optional[str], link: Optional[str]
    ) -> "Quote":
        speaker = speaker_map.get(item.speaker, item.speaker)
        updated = {
            "quote": item.quote,
            "speaker": speaker,
            "start": item.start,
            "created": item.created,
            "episode": episode if episode else item.episode,
            "link": link if link else item.link,
        }
        return Quote(**updated)
