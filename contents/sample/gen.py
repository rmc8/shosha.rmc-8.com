import re
import json

import spacy
import requests as r
from bs4 import BeautifulSoup


nlp = spacy.load("ja_core_news_sm")


def get_url_list():
    url_text = "contents/sample/urls.txt"
    with open(url_text, "r") as f:
        return f.read().splitlines()


def get_sentence(text):
    contents = []
    for sent in nlp(text).sents:
        if len(sent) <= 15 or 80 < len(sent):
            continue
        contents.append(str(sent).strip())
    return contents


def main():
    db = []
    urls = get_url_list()
    for url in urls:
        res = r.get(url)
        res.encoding = res.apparent_encoding
        bs = BeautifulSoup(res.text, "xml")
        title = bs.select_one(".title").text
        author = bs.select_one(".author").text
        raw_data = bs.select_one(".main_text").text
        contents = re.sub(r"（[ぁ-んァ-ヶ]+）", "", raw_data)
        try:
            data = get_sentence(contents)
        except Exception:
            continue
        rec = {
            "title": title,
            "author": author,
            "url": url,
            "contents": data,
        }
        db.append(rec)
    output = {"data": db}
    with open("data.json", "w", encoding="utf-8") as f:
        print(json.dumps(output, ensure_ascii=False), file=f)

if __name__ == "__main__":
    main()
