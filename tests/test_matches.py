import json
import os

from mockfirestore import MockFirestore
import responses


from tippecanews.utils.matches import send_matches, make_matches, check_matches


@responses.activate
def test_send_messages():
    list_members_response_data = {
        "ok": True,
        "members": [
            {"id": "Adrian", "is_bot": True},
            {"id": "Sydney", "is_bot": False},
            {"id": "Alisa", "is_bot": False},
            {"id": "Julia", "is_bot": False},
        ],
    }

    os.environ["SLACK_TOKEN"] = "TEST_TOKEN"

    test_url = f"https://slack.com/api/users.list?token={os.environ['SLACK_TOKEN']}"

    responses.add(
        responses.GET,
        test_url,
        body=json.dumps(list_members_response_data),
        status=200,
        content_type="application/json",
    )

    post_user_return_data = {
        "ok": True,
    }

    post_message_url = f"https://slack.com/api/chat.postMessage"

    responses.add(
        responses.POST,
        post_message_url,
        body=json.dumps(post_user_return_data),
        status=200,
        content_type="application/json",
    )

    matches = send_matches()

    assert matches == len(
        [user for user in list_members_response_data["members"] if not user["is_bot"]]
    )


@responses.activate
def test_make_matches():
    list_members_response_data = {
        "ok": True,
        "members": [
            {"id": "Adrian", "is_bot": False},
            {"id": "Sydney", "is_bot": False},
            {"id": "Alisa", "is_bot": False},
            {"id": "Julia", "is_bot": False},
        ],
    }

    os.environ["SLACK_TOKEN"] = "TEST_TOKEN"

    test_url = f"https://slack.com/api/users.list?token={os.environ['SLACK_TOKEN']}"

    responses.add(
        responses.GET,
        test_url,
        body=json.dumps(list_members_response_data),
        status=200,
        content_type="application/json",
    )

    post_user_return_data = {
        "ok": True,
    }

    post_message_url = f"https://slack.com/api/chat.postMessage"

    responses.add(
        responses.POST,
        post_message_url,
        body=json.dumps(post_user_return_data),
        status=200,
        content_type="application/json",
    )

    matches = send_matches()

    assert matches == len(
        [user for user in list_members_response_data["members"] if not user["is_bot"]]
    )