import copy
from datetime import datetime, timedelta
import json
import os
import random

from google.cloud import firestore
import requests


def send_matches() -> int:
    """Helper function to send the matches out to all members of the workspace.

    Returns:
        An int representing the number of users matching messages were sent to.
    """
    # get list of all users
    list_users_url = "https://slack.com/api/users.list"

    params = {"token": os.getenv("SLACK_TOKEN")}

    r = requests.get(list_users_url, params=params)

    data = r.json()

    user_ids = [member["id"] for member in data["members"] if member["is_bot"] is False]

    counter = 0

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

        r = requests.post(
            "https://slack.com/api/chat.postMessage", params=send_msg_params
        )

def match_people() -> int:
    """A helper function to match pair people from the previous day together and create group chats.

    Returns:
        The number of pairs created.
    """
    db = firestore.Client()

    today = datetime.now() - timedelta(days=datetime.now().weekday() + 1)

    print(day)

    week_doc = (
        db.collection("meetings")
        .document(f"{today.month}_{today.day}_{today.year}")
        .get()
    )

    if week_doc.exists:
        members = week_doc.to_dict()["uids"]

        members = random.shuffle(members)

        tmp = []
        pairs_list = []

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

        return len(pairs_list)

    return 0


def check_matches() -> int:
    """Helper function to send the matches out to all members of the workspace.

    Returns:
        An int representing the number of users matching messages were sent to.
    """
    db = firestore.Client()

    today = datetime.now() - timedelta(days=datetime.now().weekday() + 1)

    week_doc = (
        db.collection("meetings")
        .document(f"{today.month}_{today.day}_{today.year}")
        .get()
    )

    if week_doc.exists:
        members = week_doc.to_dict()["uids"]

        tmp = []
        pairs_list = []

        counter = 0

        for uid in members:
            send_msg_params = {
                "token": os.getenv("SLACK_TOKEN"),
                "channel": uid,
                "text": "Hey! Did you meet the person you were paired up with this week?",
            }

            blocks = {
                "type": "home",
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "Hey! Did you meet the person you were paired up with this week?",
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
                                "value": "yes_meet",
                            },
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "no !",
                                },
                                "value": "no_meet",
                            },
                        ],
                    },
                ],
            }

            send_msg_params["blocks"] = json.dumps(blocks["blocks"])

            r = requests.post(
                "https://slack.com/api/chat.postMessage", params=send_msg_params
            )

            if r.json()["ok"]:
                counter += 1
            else:
                raise Exception

    return counter


if __name__ == "__main__":
    match_people()
