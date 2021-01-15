import copy
from datetime import datetime
import json
import os
import random
from typing import Dict

from google.cloud import firestore
import requests

from .influxdb_logger import log
from .database import get_database_connection
from .influxdb_logger import log_agree_to_match

class User:
    def __init__(self, slack_uid: str):
        self.slack_uid = slack_uid
    
    def to_dict(self):
        return {"slack_uid": self.slack_uid}

def process_match_request(response: Dict):
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
            log_agree_to_match()

        else:
            payload = {"text": "ok ! maybe next week ..."}

        r = requests.post(response["response_url"], json=payload)
        r.raise_for_status()

def send_matches():
    # get list of all users
    list_users_url = "https://slack.com/api/users.list"

    params = {"token": os.getenv("SLACK_TOKEN")}

    r = requests.get(list_users_url, params=params)

    data = r.json()

    user_ids = [member["id"] for member in data["members"] if member["is_bot"] is False]

    for uid in user_ids:
        send_msg_params = {
            "token": os.getenv("SLACK_TOKEN"),
            "channel": uid,
            "text": "Hey! Do you wanna meet someone new at The Exponent this week?",
        }

        blocks = {
            "type": "home",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Hey! Do you wanna meet someone new at The Exponent this week?",
                    },
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
                        },
                    ],
                },
            ],
        }

        send_msg_params["blocks"] = json.dumps(blocks["blocks"])

        try:
            r = requests.post(
                "https://slack.com/api/chat.postMessage", params=send_msg_params
            )
            r.raise_for_status()
        except Exception as e:
            log(e)


def match_people():
    db = firestore.Client()
    today = datetime.now()
    day = today.day - 1

    print(day)

    week_doc = (
        db.collection("meetings").document(f"{today.month}_{day}_{today.year}").get()
    )
    if week_doc.exists:
        members = week_doc.to_dict()["uids"]
        random.shuffle(members)

        pairs_list = []
        tmp = []
        for member in members:
            tmp.append(member)
            if len(tmp) >= 2:
                users_str = f"{tmp[0]},{tmp[1]}"
                params = {"token": os.getenv("SLACK_TOKEN"), "users": users_str}
                r = requests.post(
                    "https://slack.com/api/conversations.open", params=params
                )

                data = r.json()

                if data["ok"]:
                    welcome_params = {
                        "token": os.getenv("SLACK_TOKEN"),
                        "channel": data["channel"]["id"],
                        "text": "y'all got matched! pls find a time to meet up with each other! maybe try zoom?",
                    }
                    r = requests.post(
                        "https://slack.com/api/chat.postMessage", params=welcome_params
                    )
                pairs_list.append(json.dumps(copy.copy(tmp)))
                tmp.clear()

        db.collection("meetings").document(
            f"{today.month}_{today.day}_{today.year}"
        ).update({"pairs": pairs_list})

        log(f"Matched {len(pairs_list)} people in this matching session.")
    else:
        log(f"ERROR: Could not find the document in the database.")


if __name__ == "__main__":
    match_people()
