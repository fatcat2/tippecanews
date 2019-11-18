import pytest

from tippecanews.app import app


@pytest.fixture
def client():
    client = app.test_client()
    yield client


def test_tcms(client):
    resp = client.post("/tcms")
    assert resp.status == "200 OK"


def test_email(client):
    resp = client.post("/email")
    assert resp.status == "200 OK"