# This is the file containing most of the logic.
# TODO(fatcat2): organize all helper methods into separate modules

import os

import atoma
from dotenv import load_dotenv
from flask import Flask, request


from google.cloud import firestore
import requests
import json  # TODO REMOVE
from info_getters import get_pngs, xml_urls

# Import local modules
from ryan_twtr_utils import ryan_twtr_utils

app = Flask(__name__)

load_dotenv()


@app.route("/")
def hello_world():
    target = os.environ.get("TARGET", "World")
    return "Hello {}!\n".format(target)


@app.route("/test")
def test_me():
    return "This tests things. Please turn back."


@app.route("/interactive", methods=["POST"])
def test_funct():
    response = json.loads(request.form.get("payload"))
    resp_url = response["response_url"]
    blocks = response["message"]["blocks"]


    if blocks[0]["accessory"]["value"] == "cancel":
        blocks[0]["accessory"]["value"] = "take"
        blocks[0]["accessory"]["text"]["text"] = "Take me!"
        blocks.pop(len(blocks) - 1)
    else:
        blocks[0]["accessory"]["value"] = "cancel"
        blocks[0]["accessory"]["text"]["text"] = "Cancel!"
        blocks.append(
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": f"Taken by @{response['user']['username']}",
                    }
                ],
            }
        )
    payload = {"replace_original": "true", "blocks": blocks}

    requests.post(resp_url, json=payload)
    return ""


@app.route("/newsfetch")
def newsfetch():
    db = firestore.Client()
    news_ref = db.collection("news")
    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += "HIGH:!DH:!aNULL"
    try:
        requests.packages.urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST += (
            "HIGH:!DH:!aNULL"
        )
    except AttributeError:
        # no pyopenssl support used / needed / available
        pass
    for url in xml_urls:
        response = requests.get(url)
        feed = atoma.parse_rss_bytes(response.content)
        for post in feed.items:
            docs = (
                news_ref.where("title", "==", "{}".format(post.title))
                .where("link", "==", "{}".format(post.link))
                .get()
            )
            docs_list = [doc for doc in docs]
            if len(docs_list) == 0:
                news_ref.add(
                    {"title": "{}".format(post.title), "link": "{}".format(post.link)}
                )
                send_slack(
                    post.title,
                    post.link,
                    post.pub_date.strftime("(%Y/%m/%d)"),
                    is_pr=True,
                )
    # PNG section
    png_ref = db.collection("png")
    for row in get_pngs():
        doc_id = row[0] + row[2]
        try:
            png_ref.add(
                {"name": row[0], "location": row[1], "date issued": row[2]},
                document_id=doc_id,
            )
            sendSlack(
                f"PNG issued to {row[0]} on {row[2]}. Banned from {row[1]}", "", ""
            )
        except Exception:
            pass


    # Twitter section
    twtr_helper = ryan_twtr_utils()
    twtr_helper.get_new_tweets()
    return "Done"


def send_slack(title: str, link: str, date: str, is_pr: bool = False):
    if "http" not in link:
        link = "http://{}".format(link)

    headers = {"Authorization": "Bearer {}".format(os.getenv("SLACK_TOKEN"))}
    payload = {
        "channel": os.getenv("SLACK_CHANNEL"),
        "text": title,
        "blocks": [
            {"type": "section", "text": {"type": "mrkdwn", "text": f"{title}"}},
            {
                "type": "context",
                "elements": [{"type": "mrkdwn", "text": f"Posted on {date}"}],
            },
        ],
    }

    if is_pr:
        payload["blocks"][0]["text"] = {"type": "mrkdwn", "text": f"<{link}|{title}>"}
        payload["blocks"][0]["accessory"] = {
            "type": "button",
            "text": {"type": "plain_text", "text": "Take Me!"},
            "value": "take",
            "action_id": "button",
        }

    r = requests.post(
        "https://slack.com/api/chat.postMessage", headers=headers, json=payload
    )
    r.raise_for_status()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
