import os
from dateutil import parser
from datetime import datetime, timezone, timedelta
import twitter
import requests


class ryan_twtr_utils:
    account_list = [
        "WLFI",
        "davebangert",
        "JCOnline",
        "TippecanoeCoSh1",
        "AnnaDarlingTV",
        "TrevorPetersTV",
    ]

    def __init__(self):
        # Not assigning the following to this since we just want them once
        consumer_key = os.getenv("twtr_consumer_key")
        consumer_secret = os.getenv("twtr_consumer_secret")
        access_token_key = os.getenv("twtr_access_token_key")
        access_token_secret = os.getenv("twtr_access_token_secret")

        # Creating the python-twitter API object
        self.api = twitter.Api(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token_key=access_token_key,
            access_token_secret=access_token_secret,
        )

    def get_past_fifteen_mins(self, account: str):
        """Function to get tweets from the past 15 minutes

        :type account: str
        :param account: A string representing a Twitter user's username.

        """
        statuses = self.api.GetUserTimeline(screen_name=account)

        ret_list = [
            status
            for status in statuses
            if (
                datetime.now(timezone.utc) - parser.parse(status.created_at)
                < timedelta(minutes=15)
            )
        ]
        return ret_list

    def send_slack_twt(self, tweet):
        headers = {"Authorization": "Bearer {}".format(os.getenv("SLACK_TOKEN"))}
        payload = {
            "channel": os.getenv("SLACK_CHANNEL"),
            "text": tweet.text,
            "blocks": [
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": f"{tweet.text}"},
                    "accessory": {
                        "type": "image",
                        "image_url": f"{tweet.user.profile_image_url}",
                        "alt_text": "alt text for image",
                    },
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": f"Posted on {tweet.created_at} by @{tweet.user.screen_name}",
                        },
                        {
                            "type": "image",
                            "image_url": "https://i.imgur.com/clhAX9Y.png",
                            "alt_text": "images",
                        },
                    ],
                },
            ],
        }

        print(headers, payload)
        r = requests.post(
            "https://slack.com/api/chat.postMessage", headers=headers, json=payload
        )
        print(r)
        r.raise_for_status()

    def get_new_tweets(self):
        for username in self.account_list:
            for tweet in self.get_past_fifteen_mins(username):
                self.send_slack_twt(tweet)
