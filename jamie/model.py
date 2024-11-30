from datetime import datetime
import hashlib


class Quote:
    def __init__(self, quote:str, speaker:str, episode:str="", link:str=""):
        self.quote = quote
        self.speaker = speaker
        self.episode = episode
        self.link = link
        self.id = hashlib.md5(quote.encode()).hexdigest()[:6]
        self.date = datetime.now().isoformat()
