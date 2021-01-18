import os

import atoma
from datetime import datetime
from atoma import rss
from flask import Flask, request, jsonify, render_template, send_from_directory


import json
from google.cloud import firestore
import requests
from tippecanews.utils.retrievers import (
    directory_search,
    get_pngs, rss_reader,
    send_slack,
    xml_urls,
    get_bylines,
    get_quote,
    # crime_scrape,
)

from tippecanews.utils.news import newsfeed
from tippecanews.utils.matches import send_matches, match_people, process_match_request


from .utils.influxdb_logger import log_request, log_agree_to_match

app = Flask(__name__, template_folder="build", static_folder="build/static")
# logging.basicConfig(level=10)


@app.route("/")
def serve():
    """Renders the instruction page.

    Returns:
        The template for the instruction page.
    """
    # log_request(endpoint="/")
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
    rss_reader()

    # get_quote()
    return jsonify(200)


@app.route("/interactive", methods=["POST"])
def interactive():
    """A route to handle interactions with press release messages."""
    response = json.loads(request.form.get("payload"))

    print(response)

    if response["channel"]["name"] != "tippecanews":
        process_match_request(response)
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
    elif datetime.now().weekday() == 6:
        match_people()

    get_quote_result = get_quote()
    newsfeed_result = newsfeed()

    return jsonify([get_quote_result, newsfeed_result])


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
    print("fetching news")
    # logging.debug("Fetching news")
    rss_reader()

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
