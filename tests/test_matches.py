import pytest

from tippecanews.utils.matches import (
    process_match_request,
    send_matches,
    match_people,
    User,
)
from tippecanews.utils.database import get_database_connection
from unittest.mock import patch


class MockResponse:
    def __init__(self):
        pass

    def raise_for_status(self):
        return ""


def test_process_match_request():
    with patch("tippecanews.app.requests.post") as mock_post:
        mock_post.return_value = MockResponse()
        test_request_data = {
            "actions": [{"value": "yes"}],
            "user": "slack_id",
            "response_url": "",
        }

        conn = get_database_connection()

        conn.run("drop table if exists meeting_requests")

        conn.run("create table meeting_requests (slack_uid text, day date)")

        conn.commit()

        process_match_request(test_request_data)

        rows = conn.run(
            "select slack_uid from meeting_requests where day = current_date"
        )

        members = [User(*row) for row in rows]

        assert len(members) == 1
        assert members[0].slack_uid == test_request_data["user"]
