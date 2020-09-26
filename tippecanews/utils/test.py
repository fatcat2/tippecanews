import requests
import os


def send_slack(title: str, link: str, date: str, is_pr: bool = False):
    if "http" not in link:
        link = "http://{}".format(link)

    headers = {
        "content-type": "application/json",
        "Authorization": "Bearer {}".format(os.getenv("SLACK_TOKEN")),
    }
    payload = {
        "channel": "tippecanews",
        "text": title,
        "token": "xoxb-566562418550-1332232032288-QJmR7RDQlWGwayZ8L71osWCj",
        # "blocks": [
        #     {"type": "section", "text": {"type": "mrkdwn", "text": f"{title}"}},
        #     {
        #         "type": "context",
        #         "elements": [{"type": "mrkdwn", "text": f"Posted on {date}"}],
        #     },
        # ],
    }

    # if is_pr:
    #     payload["blocks"][0]["text"] = {"type": "mrkdwn", "text": f"<{link}|{title}>"}
    #     payload["blocks"][0]["accessory"] = {
    #         "type": "button",
    #         "text": {"type": "plain_text", "text": "Take Me!"},
    #         "value": "take",
    #         "action_id": "button",
    #     }

    # logging.debug(payload)
    r = requests.post(
        "https://slack.com/api/chat.postMessage", params=payload
    )
    r.raise_for_status()
    print(r.text)


send_slack("test", "www.google.com", "test")
