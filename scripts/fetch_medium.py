import feedparser
import os
import re
from datetime import datetime

MEDIUM_RSS = "https://medium.com/feed/@hegdeshresta"
OUTPUT_DIR = "content/posts"

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s]+', '-', text.strip())
    return text

def fetch():
    feed = feedparser.parse(MEDIUM_RSS)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for entry in feed.entries:
        slug = slugify(entry.title)
        filename = f"{OUTPUT_DIR}/medium-{slug}.md"

        if os.path.exists(filename):
            continue

        date = datetime(*entry.published_parsed[:6]).strftime("%Y-%m-%dT%H:%M:%S+00:00")
        tags = [tag.term for tag in getattr(entry, 'tags', [])]
        tags_str = ", ".join(f'"{t}"' for t in tags)

        content = f"""+++
title = "{entry.title.replace('"', "'")}"
date = "{date}"
draft = false
tags = [{tags_str}]
externalUrl = "{entry.link}"
showSummary = true
summary = "Originally published on Medium. Click to read the full article."
+++

Originally published on [Medium]({entry.link}).
"""
        with open(filename, 'w') as f:
            f.write(content)
        print(f"Created: {filename}")

if __name__ == "__main__":
    fetch()