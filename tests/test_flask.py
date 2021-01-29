import pytest

from tippecanews.app import app


@pytest.fixture
def client():
    client = app.test_client()
    yield client


# def test_tcms(client):
#     with patch("tippecanews.utils.influxdb_logger.log_request") as mock_log:
#         mock_log.return_value = True
#         resp = client.post("/tcms")
#         assert resp.status == "200 OK"


# def test_email(client):
#     resp = client.post("/email")
#     assert resp.status == "200 OK"
