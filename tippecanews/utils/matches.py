import json
import os
import random
from typing import Dict

import requests

from .influxdb_logger import log
from .database import get_database_connection


class User:
    def __init__(self, slack_uid: str):
        self.slack_uid = slack_uid

    def to_dict(self):
        return {"slack_uid": self.slack_uid}


def process_match_request(response: Dict):
    meet_request = True if response["actions"][0]["value"] == "yes" else False
    slack_uid = response["user"]["id"]
    conn = get_database_connection()

    if meet_request:
        conn.run(
            "insert into meeting_requests values (:slack_uid, current_date)",
            slack_uid=slack_uid,
        )
        conn.commit()
        conn.close()

        payload = {
            "text": "ok ! thanks for responding. you will be matched with someone tomorrow morning."
        }
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
    """Helper function to match people, send the messages and store the results in the DB."""
    conn = get_database_connection()

    rows = conn.run(
        "select slack_uid, day from meeting_requests where day = current_date - 1"
    )

    members = [User(*row) for row in rows]
    random.shuffle(members)

    tmp = []
    for member in members:
        tmp.append(member)
        if len(tmp) >= 2:
            params = {
                "token": os.getenv("SLACK_TOKEN"),
                "users": f"{tmp[0].slack_uid},{tmp[1].slack_uid}",
            }
            r = requests.post("https://slack.com/api/conversations.open", params=params)

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

            conn.run(
                "insert into matches (user_1, user_2, date) values (:user_1, :user_2, current_date)",
                user_1=tmp[0],
                user_2=tmp[1],
            )

            tmp.clear()

    conn.commit()
    conn.close()


if __name__ == "__main__":
    match_people()
