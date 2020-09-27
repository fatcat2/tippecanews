import copy
from datetime import datetime, timedelta
import json
import os
import random

from google.cloud import firestore
import requests


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

        r = requests.post(
            "https://slack.com/api/chat.postMessage", params=send_msg_params
        )


def match_people():
    db = firestore.Client()
    today = datetime.now()
    day = datetime.now() - timedelta(days=datetime.now().weekday()+1)

    week_doc = (
        db.collection("meetings").document(f"{today.month}_{day}_{today.year}").get()
    )
    if week_doc.exists:
        members = week_doc.to_dict()["uids"]
        random.shuffle(members)

        pairs_list = []
        tmp = []
        for uid in user_ids:
            send_msg_params = {
                "token": os.getenv("SLACK_TOKEN"),
                "channel": uid,
                "text": "Hey! Did you meet your assigned matched person this week?",
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
                                "value": "met_the_person",
                            },
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "no !",
                                },
                                "value": "didnt_meet_the_person",
                            },
                        ],
                    },
                ],
            }

            send_msg_params["blocks"] = json.dumps(blocks["blocks"])

            r = requests.post(
                "https://slack.com/api/chat.postMessage", params=send_msg_params
            )


        db.collection("meetings").document(
            f"{today.month}_{today.day}_{today.year}"
        ).update({"pairs": pairs_list})


def check_matches():
    if datetime.now() > 0:
        day = datetime.now() - timedelta(days=datetime.now().weekday()+1)
    else:
        day = datetime.now()

    week_doc = (
        db.collection("meetings").document(f"{today.month}_{day}_{today.year}").get()
    )
    if week_doc.exists:
        members = week_doc.to_dict()["uids"]

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

def get_match_data(user, token):
    db = firestore.Client()

    docs = db.collection("meetings").stream()

    ret_dict = {matches: []}

    for doc in docs:
        data = doc.to_dict()
        print(doc.id)

        if "pairs" in data:
            pair = [pair for pair in data["pairs"] if user in pair]
            if len(pair) > 0:
                for partner in json.loads(pair[0]):
                    if partner != user:
                        params = {
                                "token": token,
                                "user": partner
                        }
                        response = requests.get("https://slack.com/api/users.info", params=params)

                        response_json = response.json()

                        if response_json["ok"]:
                            ret_dict["matches"].append(
                                {
                                        "name": response_json["user"]["real_name"],
                                        "week": doc.id,
                                        "profilePicUrl": response_json["user"]["profile"]["image_original"]
                                }
                            )

                        else:
                            print(response_json["error"])

    return ret_dict



if __name__ == "__main__":
    get_match_data(os.getenv("test_user"), os.getenv("SLACK_TOKEN"))
