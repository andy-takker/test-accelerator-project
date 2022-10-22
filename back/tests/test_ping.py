import pytest


def test_get_ping(test_client):
    response = test_client.get("/ping/")
    assert response.status_code == 200
    assert response.json() == {"answer": "pong"}
