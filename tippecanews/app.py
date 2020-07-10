import os

import atoma
from datetime import datetime
from flask import Flask, request, jsonify, render_template, send_from_directory


import json
from google.cloud import firestore
import requests
from tippecanews.utils.retrievers import (
    directory_search,
    get_pngs,
    send_slack,
    xml_urls,
    get_bylines,
    get_quote
)
import logging

app = Flask(__name__, template_folder="static", static_folder="static/static")
logging.basicConfig(level=10)


@app.route("/")
def serve():
    """Renders the instruction page.

    Returns:
        The template for the instruction page.
    """
    return render_template("index.html")


@app.route("/favicon.ico")
def favicon():
    """Returns the favicon.

    Returns:
        The favicon file
    """
    return send_from_directory("static", "favicon.ico")


@app.route("/directory", methods=["POST"])
def directory_search_route():
    """Takes in a username and searches it through the Purdue Directory.

    Returns:
        Information found by querying the Purdue Directory in JSON form.
    """
    return jsonify(directory_search(request.form["text"]))


@app.route("/bylines", methods=["POST"])
def byline_route():
    """Returns the bylines in a Slack-compatible format.

    Returns:
        Bylines in a Slack-compatible format
    """
    return jsonify(get_bylines())


@app.route("/cms", methods=["GET", "POST"])
def cms():
    """Returns the link to CMS in a Slack-compatible format.

    Returns:
        CMS in a Slack-compatible format
    """
    return jsonify("https://admin-newyork1.bloxcms.com/")


@app.route("/tcms", methods=["GET", "POST"])
def tcms():
    """Returns the TCMS link in a Slack-compatible format.

    Returns:
        TCMS in a Slack-compatible format
    """
    return jsonify("https://192.168.168.128/desktop/#/purdueexponent.local")


@app.route("/email", methods=["GET", "POST"])
def email():
    """Returns the email link in a Slack-compatible format.

    Returns:
        Email link in a Slack-compatible format
    """
    return jsonify("https://webmail.tn-cloud.net/src/login.php")


@app.route("/test")
def test_me():
    """ Test function to ensure things are working. """
    send_slack(
        f"This is a test message. It is currently {datetime.now()}",
        "github.com/fatcat2/tippecanews",
        "asdf",
    )
    send_slack(
        f"This is an interactive test message. It is currently {datetime.now()}",
        "github.com/fatcat2/tippecanews",
        "asdf",
        is_pr=True,
    )

    get_quote()
    return jsonify(200)


@app.route("/interactive", methods=["POST"])
def interactive():
    """A route to handle interactions with press release messages.
    """
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

@app.route("/daily")
def daily_route():
    return jsonify(get_quote())


@app.route("/newsfetch")
def newsfetch():
    """Function that scans through various Purdue news channels in order to find information within 15 minutes of it happening.
    News sources being scanned:
    * PUPD logs
    * Some of the RSS feeds from Purdue news
    """
    logging.debug("Fetching news")
    db = firestore.Client()
    news_ref = db.collection("news_releases_test")
    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += "HIGH:!DH:!aNULL"
    try:
        requests.packages.urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST += (
            "HIGH:!DH:!aNULL"
        )
    except AttributeError:
        # no pyopenssl support used / needed / available
        pass

    status_log = ""

    logging.debug("Going through XML urls")

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
                status_log = status_log + f"<p>Added: {post.title}</p>"
                logging.debug(f"Added: {post.title}</p>")

    png_ref = db.collection("png")
    for row in get_pngs():
        doc_id = row[0] + row[2]
        try:
            png_ref.add(
                {"name": row[0], "location": row[1], "date issued": row[2]},
                document_id=doc_id,
            )
            send_slack(
                f"PNG issued to {row[0]} on {row[2]}. Banned from {row[1]}", "", ""
            )
        except Exception:
            pass

    return "Done"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
