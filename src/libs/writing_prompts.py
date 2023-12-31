import random
from typing import List


class WritingPromptProvider:
    def __init__(self):
        with open("assets/data/data.json", "r", encoding="utf-8") as f:
            raw = f.read()
            self.raw: dict = eval(raw)

    def choice(self):
        data: List[dict] = self.raw["data"]
        book = random.choice(data)
        return {
            "script": random.choice(book["contents"]),
            "url": book.get("url"),
            "title": book.get("title"),
            "author": book.get("author"),
        }
