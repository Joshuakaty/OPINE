"""Tests for the OPINE API."""

from fastapi.testclient import TestClient

from kraken.api.main import app

client = TestClient(app)


def test_root_endpoint() -> None:
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "OPINE API"
    assert data["status"] == "running"
    assert data["engine"] == "Kraken"