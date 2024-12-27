from datetime import datetime
import hashlib


class Quote:
    def __init__(self, quote: str, speaker: str, episode: str = "", link: str = "", start:int=0):
        self.quote = quote
        self.speaker = speaker
        self.episode = episode
        self.link = link
        self.id = hashlib.md5(quote.encode()).hexdigest()[:6]
        self.created = datetime.now().isoformat()
        self.start = start

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
