import feedparser
import json
from datetime import datetime
import os

RSS_URL = "https://feeds.bbci.co.uk/news/rss.xml"


def fetch_news():
    feed = feedparser.parse(RSS_URL)

    articles = []
    for entry in feed.entries:
        articles.append({
            "title": entry.title,
            "link": entry.link,
            "published": entry.published if "published" in entry else "",
            "summary": entry.summary if "summary" in entry else ""
        })

    return articles


def save_news(articles):
    os.makedirs("data", exist_ok=True)

    filename = f"data/news_{datetime.utcnow().timestamp()}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(articles)} articles to {filename}")


if __name__ == "__main__":
    news = fetch_news()
    save_news(news)
