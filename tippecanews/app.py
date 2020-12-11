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
    get_quote,
    # crime_scrape,
)

from tippecanews.utils.matches import send_matches, match_people

from .utils.logging import log_request

app = Flask(__name__, template_folder="build", static_folder="build/static")
logging.basicConfig(level=10)


@app.route("/")
def serve():
    """Renders the instruction page.

    Returns:
        The template for the instruction page.
    """
    log_request(endpoint="/")
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
    log_request(endpoint="/directory")
    return jsonify(directory_search(request.form["text"]))


@app.route("/bylines", methods=["POST"])
def byline_route():
    """Returns the bylines in a Slack-compatible format.

    Returns:
        Bylines in a Slack-compatible format
    """
    log_request(endpoint="/bylines")
    return jsonify(get_bylines(request.form["text"]))


@app.route("/cms", methods=["GET", "POST"])
def cms():
    """Returns the link to CMS in a Slack-compatible format.

    Returns:
        CMS in a Slack-compatible format
    """
    log_request(endpoint="/cms")
    return jsonify("https://admin-newyork1.bloxcms.com/")


@app.route("/tcms", methods=["GET", "POST"])
def tcms():
    """Returns the TCMS link in a Slack-compatible format.

    Returns:
        TCMS in a Slack-compatible format
    """
    log_request(endpoint="/tcms")
    return jsonify("https://192.168.168.128/desktop/#/purdueexponent.local")


@app.route("/email", methods=["GET", "POST"])
def email():
    """Returns the email link in a Slack-compatible format.

    Returns:
        Email link in a Slack-compatible format
    """
    log_request(endpoint="/email")
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

    # get_quote()
    return jsonify(200)


@app.route("/interactive", methods=["POST"])
def interactive():
    """A route to handle interactions with press release messages."""
    response = json.loads(request.form.get("payload"))

    if response["type"] == "block_actions":
        value = response["actions"][0]["value"]
        user = response["user"]
        db = firestore.Client()
        today = datetime.now()
        week_doc = (
            db.collection("meetings")
            .document(f"{today.month}_{today.day}_{today.year}")
            .get()
        )

        if not week_doc.exists:
            set_data = {"uids": []}
            db.collection("meetings").document(
                f"{today.month}_{today.day}_{today.year}"
            ).set(set_data)
            week_doc = (
                db.collection("meetings")
                .document(f"{today.month}_{today.day}_{today.year}")
                .get()
            )

        week_data = week_doc.to_dict()

        if value == "yes":
            payload = {
                "text": "ok ! thanks for responding. you will be matched with someone tomorrow morning."
            }
            week_data["uids"].append(user["id"])
            db.collection(os.getenv("MEETINGS_DB")).document(
                f"{today.month}_{today.day}_{today.year}"
            ).update(week_data)
        else:
            payload = {"text": "ok ! maybe next week ..."}

        r = requests.post(response["response_url"], json=payload)
        r.raise_for_status()

        return ""

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
    if datetime.now().weekday() == 6:
        send_matches()

    return jsonify(get_quote())


@app.route("/sendmatches")
def send_match_route():
    send_matches()
    return "sent matching messages"


@app.route("/makematches")
def match_route():
    match_people()
    return "matched with people"


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
        if response.status_code == 404:
            continue
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

    # crimes = crime_scrape()
    # crime_ref = db.collection("crimes")

    # for day in crimes.keys():
    #     docs = (
    #             crime_ref.where("date", "==", "{}".format(day))
    #             .get()
    #         )

    #     if len(docs) == 0:
    #         insert_obj = {
    #             "date": day,
    #             "crimes": crimes[day]
    #         }

    #         crime_ref.add(insert_obj)

    return "Done"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
