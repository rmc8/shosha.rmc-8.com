import random
from typing import List

import pandas as pd
import requests as r


path = "rmc8/bsky_random_shosha_data/main/contents/{author_id}/{contents_id}"
BASE_URL = "https://raw.githubusercontent.com/{path}".format(path=path)


class WritingPromptProvider:
    def __init__(self):
        self.df = pd.read_csv(
            "contents/contents_table.tsv",
            sep="\t",
            dtype={"author_id": str, "content_id": str},
        )

    def choice(self):
        author_id = random.choice(list(self.df["author_id"].unique()))
        df = self.df[self.df["author_id"] == author_id]
        contents_id = random.choice(list(df["content_id"].unique()))
        url = BASE_URL.format(author_id=author_id, contents_id=contents_id)
        book = r.get(url).json()
        return {
            "script": random.choice(book["contents"]),
            "url": book.get("url"),
            "title": book.get("title"),
            "author": book.get("author"),
        }
