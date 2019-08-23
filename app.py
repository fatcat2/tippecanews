import os

import atoma
from dotenv import load_dotenv
from flask import Flask
from google.cloud import firestore 
import requests

from info_getters import get_pngs, xml_urls

app = Flask(__name__)

load_dotenv()

@app.route("/")
def hello_world():
    target = os.environ.get("TARGET", "World")
    return "Hello {}!\n".format(target)


@app.route("/newsfetch")
def newsfetch():
    db = firestore.Client()
    news_ref = db.collection(u"news")
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
                news_ref.where(u"title", u"==", u"{}".format(post.title))
                .where(u"link", u"==", u"{}".format(post.link))
                .get()
            )
            docs_list = [doc for doc in docs]
            if len(docs_list) == 0:
                news_ref.add(
                    {
                        u"title": u"{}".format(post.title),
                        u"link": u"{}".format(post.link),
                    }
                )
                sendSlack(post.title, post.link, post.pub_date.strftime("(%Y/%m/%d)"))
    png_ref = db.collection(u"png")
    for row in get_pngs():
        doc_id = row[0]+row[2]
        try:
            png_ref.add(
                    {
                        u"name": row[0],
                        u"location": row[1],
                        u"date issued": row[2],
                    },
                    document_id=doc_id
            )
            sendSlack(f"PNG issued to {row[0]} on {row[2]}. Banned from {row[1]}", "", "")
        except Exception:
            pass
            
    return "Done"


def sendSlack(title: str, link: str, date: str):
    if "http" not in link:
        link = "http://{}".format(link)

    headers = {
        "Authorization": "Bearer {}".format(
            os.getenv("SLACK_TOKEN")
        )
    }
    payload = {
        "channel": os.getenv("SLACK_CHANNEL"),
        "attachments": [
            {
                "fallback": title,
                "color": "#36a64f",
                "author_name": "Tippecanews",
                "title": title,
                "title_link": link,
                "footer": "tippecanews by ryan chen",
                "footer_icon": "https://github.com/fatcat2/tippecanews/raw/master/DSC_6043.jpg",
            }
        ],
    }
    print(payload)
    r = requests.post(
        "https://slack.com/api/chat.postMessage", headers=headers, json=payload
    )
    r.raise_for_status()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
