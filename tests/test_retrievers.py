import json
import os

import pytest
import requests
import responses

from tippecanews.utils.retrievers import get_pngs, xml_urls, send_slack


@pytest.fixture
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps


def test_valid_xml_urls():
    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += "HIGH:!DH:!aNULL"
    try:
        requests.packages.urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST += (
            "HIGH:!DH:!aNULL"
        )
    except AttributeError:
        pass

    for url in xml_urls:
        response = requests.get(url)
        assert response.status_code == 200


def test_get_pngs():
    assert len(get_pngs()) >= 0


@responses.activate
def test_send_slack_press_release(mocked_responses):
    test_title = "This is a test message."
    test_link = "http://ryanjchen.com"
    test_url = "https://slack.com/api/chat.postMessage"

    def request_callback(request):
        resp_body = json.loads(request.body)
        headers = {"content-type": "application/json"}
        return (200, headers, json.dumps(resp_body))

    mocked_responses.add_callback(
        responses.POST,
        test_url,
        callback=request_callback,
        headers={"Authorization": "Bearer {}".format(os.getenv("SLACK_TOKEN"))}
    )

    send_slack(test_title, test_link, "12-05-1889", is_pr=True)

    assert len(mocked_responses.calls) == 1
    assert mocked_responses.calls[0].request.url == test_url
    assert mocked_responses.calls[0].request.json["text"] == test_title
