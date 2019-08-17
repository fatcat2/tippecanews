import requests
import os
import atoma
from dotenv import load_dotenv



def sendSlack(title: str, link: str, date: str):
    if "http" not in link:
        link = "http://{}".format(link)

    headers = {"Authorization": "Bearer {}".format(os.getenv("SLACK_TOKEN"))}
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
    print(r)

load_dotenv()

sendSlack("one", "two", "three")
