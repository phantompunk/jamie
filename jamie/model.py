from dataclasses import dataclass, field, replace
import json
from datetime import datetime
import hashlib
from typing import Dict, Optional


@dataclass
class Quote:
    id: str = field(default="", init=False)
    quote: str
    speaker: str
    start: int
    link: str = ""
    episode: str = ""
    created: datetime = field(default_factory=datetime.now) 

    def __post_init__(self):
        if not self.id:
            self.id = hashlib.md5(self.quote.encode()).hexdigest()[:6]

    def to_dict(self):
        return {
            "quote": self.quote,
            "speaker": self.speaker,
            "episode": self.episode,
            "link": self.link,
            "id": self.id,
            "start": self.start,
            "created": self.created.isoformat(),
        }

    @classmethod
    def from_dict(cls, item: Dict) -> "Quote":
        # created = datetime.fromisoformat(item.get("created", None))
        # return cls(**item, created=created)
        return cls(
            quote=item["quote"],
            speaker=item["speaker"],
            episode=item["episode"],
            link=item["link"],
            start=item["start"],
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
        # up = {
        #     "quote":item.quote,
        #     "speaker":speaker,
        #     "start":item.start,
        #     "created":item.created,
        #     "episode": episode if episode else item.episode,
        #     "link": link if link else item.link,
        # }
        updated = {
            **item.to_dict(),
            "speaker": speaker,
            **({"episode": episode} if episode else {}),
            **({"link": link} if link else {}),
        }
        return Quote(**updated)
