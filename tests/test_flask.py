import pytest

from tippecanews.app import app


@pytest.fixture
def client():
    client = app.test_client()
    yield client


def test_hello_world(client):
    resp = client.get("/")
    assert resp.status == "200 OK"

def test_cms(client):
    resp = client.post("/cms")
    assert resp.status == "200 OK"
