import json
import os

import requests

from .influxdb_logger import log_error


def newsfeed():
    try:
        r = requests.get(
            f"https://newsapi.org/v2/top-headlines?sources=associated-press&apiKey={os.getenv('NEWS_API_KEY')}"
        )
        r.raise_for_status()
    except Exception as e:
        log_error("newsfeed_get_news")

    data = r.json()
    payload = {
        "channel": os.getenv("SLACK_RANDOM"),
        "text": "Welcome to your daily news digest! Here are some of the top headlines at the Associate Press",
        "token": os.getenv("SLACK_TOKEN"),
        "blocks": [],
    }

    description_blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Welcome to your daily news digest! Here are some of the top headlines at the Associate Press",
            },
        },
        {"type": "divider"},
    ]

    payload["blocks"] += description_blocks

    counter = 0

    for article in data["articles"]:
        counter += 1
        if counter > int(os.getenv("DAILY_ARTICLE_COUNT")):
            break
        payload["blocks"].append(
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*<{article.get('url')}|{article.get('title')}>*\n{article.get('description')}\nPublished at {article.get('publishedAt')}",
                },
            }
        )

    payload["blocks"] = json.dumps(payload["blocks"])

    try:
        r = requests.post("https://slack.com/api/chat.postMessage", params=payload)
        r.raise_for_status
    except:
        log_error("newsfeed_post_slack")
