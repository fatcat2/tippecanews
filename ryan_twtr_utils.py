import os
from dateutil import parser
from datetime import datetime, timezone, timedelta
import twitter


class ryan_twtr_utils:
    def __init__():
        consumer_key = os.getenv("twtr_consumer_key")
        consumer_secret = os.getenv("twtr_consumer_secret")
        access_token_key = os.getenv("twtr_access_token_key")
        access_token_secret = os.getenv("twtr_access_token_secret")

    def get_past_fifteen_mins(account):
        statuses = api.GetUserTimeline(screen_name=account)
        li = [
            (s.text, parser.parse(s.created_at), statuses[0].urls[0].expanded_url)
            for s in statuses
        ]
        list2 = [
            item
            for item in li
            if ((datetime.now(timezone.utc) - item[1]) < timedelta(minutes=15))
        ]
        return list2
