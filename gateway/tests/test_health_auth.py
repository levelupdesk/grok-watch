import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture()
def client():
    return TestClient(app)


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_relay_requires_auth(client):
    r = client.post("/v1/relay", json={"intent": "ping", "payload": {}})
    assert r.status_code == 401


def test_relay_with_token(client):
    tok = client.post("/v1/dev/token").json()["access_token"]
    r = client.post(
        "/v1/relay",
        json={"intent": "complication.refresh", "payload": {"face": "1"}},
        headers={"Authorization": f"Bearer {tok}"},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["accepted"] is True
    assert body["intent"] == "complication.refresh"
