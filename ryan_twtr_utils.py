import os
from dateutil import parser
from datetime import datetime, timezone, timedelta
import twitter


class ryan_twtr_utils:
    def __init__():
        # Not assigning the following to this since we just want them once
        consumer_key = os.getenv("twtr_consumer_key")
        consumer_secret = os.getenv("twtr_consumer_secret")
        access_token_key = os.getenv("twtr_access_token_key")
        access_token_secret = os.getenv("twtr_access_token_secret")

        # Creating the python-twitter API object
        this.api = twitter.Api(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token_key=access_token_key,
            access_token_secret=access_token_secret,
        )

    def get_past_fifteen_mins(account: str):
        """Function to get tweets from the past 15 minutes

        :type account: str
        :param account: A string representing a Twitter user's username.

        """
        statuses = this.api.GetUserTimeline(screen_name=account)

        ret_list = [
            status
            for status in statuses
            if (
                datetime.now(timezone.utc) - parser.parse(status.created_at)
                < timedelta(minutes=15)
            )
        ]
        return ret_list

    def send_slack_twt(tweet):
        if "http" not in link:
            link = "http://{}".format(link)

        headers = {"Authorization": "Bearer {}".format(os.getenv("SLACK_TOKEN"))}
        payload = {
            "channel": os.getenv("SLACK_CHANNEL"),
            "text": tweet.text,
            "blocks": [
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": f"{tweet.text}"},
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": f"Posted on {tweet.created_at} by @{tweet.user.screen_name}",
                        }
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
