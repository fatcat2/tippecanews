from datetime import datetime
import json
import os

from google.cloud import firestore
import requests

def send_matches():
    # get list of all users
    list_users_url = "https://slack.com/api/users.list"

    params = {
        "token": os.getenv("SLACK_TOKEN")
    }

    r = requests.get(list_users_url, params=params)

    data = r.json()

    print(data)

    # user_ids = [member["id"] for member in data["members"] if member["is_bot"] is not False]

    user_ids = ["UGM3U17M0"]

    # ask if they want

    for uid in user_ids:
        send_msg_params = {
            "token": os.getenv("SLACK_TOKEN"),
            "channel": uid
        }

        blocks = {
	"type": "home",
	"blocks": [
                        {
                                "type": "section",
                                "text": {
                                        "type": "mrkdwn",
                                        "text": "Hey! Do you wanna meet someone new at the Exponent this week?"
                                }
                        },
                        {
                                "type": "actions",
                                "elements": [
                                        {
                                                "type": "button",
                                                "text": {
                                                        "type": "plain_text",
                                                        "text": "yes !",
                                                },
                                                "value": "yes",
                                        },
                                        {
                                                "type": "button",
                                                "text": {
                                                        "type": "plain_text",
                                                        "text": "no !",
                                                },
                                                "value": "no",
                                        }
                                ]
                        }
                ]
        }

        send_msg_params["blocks"] = json.dumps(blocks["blocks"])

        r = requests.post("https://slack.com/api/chat.postMessage", params=send_msg_params)

        print(r.json())

if __name__ == "__main__":
    send_matches()

