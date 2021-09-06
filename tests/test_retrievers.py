# import json
import os

import responses

from tippecanews.utils.retrievers import get_pngs, send_slack


def test_get_pngs():
    assert len(get_pngs()) >= 0


@responses.activate
def test_send_slack_press_release():
    test_title = "This is a test message."
    test_link = "http://ryanjchen.com"
    test_url = "https://slack.com/api/chat.postMessage"

    responses.add(
        responses.POST, test_url, body="{}", status=200, content_type="application/json"
    )

    os.environ["SEND_SLACK"] = "True"

    send_slack(test_title, test_link, "12-05-1889", is_pr=True)

    os.environ["SEND_SLACK"]= "False"

    assert len(responses.calls) == 1
    # assert responses.calls[0].request.url == test_url
    # assert json.loads(responses.calls[0].request.body)["text"] == test_title

@responses.activate
def test_send_slack_press_release_no():
    test_title = "This is a test message."
    test_link = "http://ryanjchen.com"
    test_url = "https://slack.com/api/chat.postMessage"

    responses.add(
        responses.POST, test_url, body="{}", status=200, content_type="application/json"
    )

    send_slack(test_title, test_link, "12-05-1889", is_pr=True)

    assert len(responses.calls) == 0
    # assert responses.calls[0].request.url == test_url
 
